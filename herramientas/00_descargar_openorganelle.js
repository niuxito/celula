// Se ejecuta en la consola del navegador en https://openorganelle.janelia.org (el bucket S3 permite CORS).
// Descarga de cada orgánulo de jrc_hela-2 solo el nivel de detalle indicado (peticiones HTTP Range sobre las
// mallas multirresolución de Neuroglancer) y lo empaqueta en un único archivo binario:
//   'HCB1' | uint32 longitud de cabecera | cabecera JSON (registros) | fragmentos Draco concatenados
const S3 = 'https://janelia-cosem-datasets.s3.amazonaws.com/';
const B = S3 + 'jrc_hela-2/neuroglancer/mesh/';
const PLAN = [['nucleus_seg',1],['pm_seg',2],['er_seg',2],['golgi_seg',1],['mito_seg',1],['endo_seg',1],['mt-out_seg',1],['vesicle_seg',2]];

async function listIds(org){ let tok=null, ids=[]; do {
  const r = await fetch(S3+'?list-type=2&max-keys=1000&prefix='+encodeURIComponent('jrc_hela-2/neuroglancer/mesh/'+org+'/')+(tok?'&continuation-token='+encodeURIComponent(tok):''));
  const t = await r.text(); for (const m of t.matchAll(/<Key>[^<]*\/(\d+)\.index<\/Key>/g)) ids.push(+m[1]);
  const mm = t.match(/<NextContinuationToken>([^<]+)</); tok = mm ? mm[1] : null; } while (tok); return ids; }

// Formato del manifiesto <id>.index (neuroglancer_multilod_draco)
function parseIndex(buf){ const dv=new DataView(buf); let o=0; const f=()=>{const x=dv.getFloat32(o,true); o+=4; return x}, u=()=>{const x=dv.getUint32(o,true); o+=4; return x};
  const chunk=[f(),f(),f()], origin=[f(),f(),f()], nl=u(); const scales=[...Array(nl)].map(f); const voff=[...Array(nl*3)].map(f); const nf=[...Array(nl)].map(u);
  const lods=[]; for (let l=0;l<nl;l++){ const n=nf[l]; const pos=[[],[],[]]; for(let a=0;a<3;a++) for(let i=0;i<n;i++) pos[a].push(u()); const sz=[...Array(n)].map(u); lods.push({pos,sz,bytes:sz.reduce((a,c)=>a+c,0)}); }
  return {chunk,origin,nl,scales,voff,nf,lods}; }

async function pool(items, n, fn){ let i=0; const w=async()=>{ while(i<items.length){ const k=i++; await fn(items[k]); } }; await Promise.all([...Array(n)].map(w)); }

async function descargar(orgs = PLAN, nombre = 'hela2_organulos.bin'){
  const recs = [], chunks = [];
  for (const [org, lodWant] of orgs) {
    const ids = await listIds(org); console.log(org, ids.length, 'objetos');
    await pool(ids, 48, async id => {
      const ix = parseIndex(await (await fetch(B+org+'/'+id+'.index')).arrayBuffer());
      const lod = Math.min(lodWant, ix.nl-1); let start = 0; for (let l=0; l<lod; l++) start += ix.lods[l].bytes;   // los LOD se guardan en orden 0,1,2…
      const L = ix.lods[lod]; if (!L.bytes) return;
      const buf = new Uint8Array(await (await fetch(B+org+'/'+id, {headers:{Range:`bytes=${start}-${start+L.bytes-1}`}})).arrayBuffer());
      const frags = []; for (let i=0;i<L.sz.length;i++) if (L.sz[i]>0) frags.push([L.pos[0][i],L.pos[1][i],L.pos[2][i],L.sz[i]]);
      recs.push({org, id, lod, chunk:ix.chunk, origin:ix.origin, voff:ix.voff.slice(lod*3, lod*3+3), frags, n:buf.length}); chunks.push(buf);
    });
  }
  const hdr = new TextEncoder().encode(JSON.stringify(recs));
  const head = new Uint8Array(8); head.set([72,67,66,49]); new DataView(head.buffer).setUint32(4, hdr.length, true);
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([head, hdr, ...chunks])); a.download = nombre; a.click();
}
// Uso:  await descargar(PLAN.filter(p => p[0] !== 'vesicle_seg'));
//       await descargar([['vesicle_seg', 2]], 'hela2_vesiculas.bin');
