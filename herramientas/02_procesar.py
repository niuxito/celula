import pickle, numpy as np, trimesh, fast_simplification, pyfqmr, sys, gc, json, struct, DracoPy
from decode import load, BITS, T
h = 0.08
region = np.load('cell_region.npy'); shell = np.load('cell_shell.npy')
def inside(P, M):
    i = np.clip(np.floor(P / h).astype(int), 0, np.array(M.shape) - 1)
    return M[i[:, 0], i[:, 1], i[:, 2]]

def frags(r, data, off):
    """yield (V µm float64, F) per fragment"""
    scale = 2 ** r['lod']; chunk = np.array(r['chunk']); origin = np.array(r['origin']); voff = np.array(r['voff'])
    o = off
    for px, py, pz, sz in r['frags']:
        m = DracoPy.decode(bytes(data[o:o + sz])); o += sz
        p = np.asarray(m.points, dtype=np.float64).reshape(-1, 3); f = np.asarray(m.faces, dtype=np.int64).reshape(-1, 3)
        if len(p) and len(f):
            yield (origin + voff + chunk * scale * (np.array([px, py, pz]) + p / (2 ** BITS - 1))) * T / 1000.0, f

def weld_np(V, F, q=1e-4):
    key = np.round(V / q).astype(np.int64)
    _, idx, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    F2 = inv.ravel()[F]; ok = (F2[:, 0] != F2[:, 1]) & (F2[:, 1] != F2[:, 2]) & (F2[:, 0] != F2[:, 2])
    return V[idx].astype(np.float32), F2[ok].astype(np.int32)

def pre(V, F, ratio):
    """simplify one fragment, keeping its border so neighbouring fragments still match"""
    if len(F) < 200: return V, F
    s = pyfqmr.Simplify(); s.setMesh(V, F)
    s.simplify_mesh(target_count=max(100, int(len(F) * ratio)), aggressiveness=5, preserve_border=True, verbose=False)
    v, f, _ = s.getMesh(); return v, f

def final(V, F, t):
    if len(F) <= t: return V.astype(np.float32), F.astype(np.int32)
    v, f = fast_simplification.simplify(V.astype(np.float32), F.astype(np.int32), target_reduction=1 - t / len(F), agg=6)
    return v, f

def build(recs_iter, mask, ratio, crop=True):
    vs, fs, off = [], [], 0
    for V, F in recs_iter:
        if crop:
            k = inside(V[F].mean(1), mask)
            if not k.any(): continue
            F = F[k]
            used = np.unique(F); remap = -np.ones(len(V), np.int64); remap[used] = np.arange(len(used)); V = V[used]; F = remap[F]
        V, F = pre(V, F, ratio)
        vs.append(V); fs.append(F + off); off += len(V)
    if not vs: return None, None
    return weld_np(np.vstack(vs), np.vstack(fs))

recs, data = load(sys.argv[1])
offs = np.cumsum([0] + [r['n'] for r in recs])[:-1]
by = {}
for r, o in zip(recs, offs): by.setdefault(r['org'], []).append((r, o))
out = {}
def put(cls, oid, v, f, **facts): out.setdefault(cls, []).append(dict(id=oid, v=v, f=f, facts=facts))
def it(org, ids=None):
    for r, o in by.get(org, []):
        if ids is None or r['id'] in ids:
            yield from frags(r, data, o)

# membrana plasmática: solo la de esta célula
V, F = build(it('pm_seg', {2}), shell, 0.12)
m = trimesh.Trimesh(V, F, process=False); cc = [c for c in m.split(only_watertight=False) if len(c.faces) > 3000]
m = trimesh.util.concatenate(cc); print('pm', len(m.faces), 'comps', len(cc), flush=True)
put('pm', 'PM', *final(m.vertices, m.faces, 220000)); del V, F, m, cc; gc.collect()
# núcleo
V, F = build(it('nucleus_seg', {1}), region, 0.2, crop=False)
m = trimesh.Trimesh(V, F, process=False); vol = abs(m.volume); ext = (m.bounds[1] - m.bounds[0])
print('nuc', len(F), 'vol', round(vol, 1), 'wt', m.is_watertight, 'ext', ext.round(1), flush=True)
put('nuc', 'NUC', *final(V, F, 100000), vol=vol, ext=ext.tolist(), wt=m.is_watertight); gc.collect()
# retículo
V, F = build(it('er_seg'), region, 0.1)
print('er', len(F), flush=True); put('er', 'ER', *final(V, F, 380000)); del V, F; gc.collect()
# Golgi
for r, o in by['golgi_seg']:
    V, F = build(frags(r, data, o), region, 0.3, crop=False)
    if V is None or inside(V, region).mean() < 0.5: continue
    m = trimesh.Trimesh(V, F, process=False)
    put('golgi', f"G{r['id']}", *final(V, F, max(1500, min(45000, len(F) // 8))), vol=abs(m.volume) if m.is_watertight else None)
print('golgi', len(out.get('golgi', [])), flush=True)
# mitocondrias, una a una
for r, o in by['mito_seg']:
    V, F = build(frags(r, data, o), region, 0.5, crop=False)
    if V is None or inside(V, region).mean() < 0.5: continue
    m = trimesh.Trimesh(V, F, process=False)
    vol = abs(m.volume) if m.is_watertight else None
    ext = np.sort(m.bounding_box_oriented.primitive.extents)[::-1]
    put('mito', f"M{r['id']}", *final(V, F, max(300, min(4000, len(F) // 12))), vol=vol, length=float(ext[0]), wt=m.is_watertight)
print('mito', len(out['mito']), 'watertight', sum(1 for x in out['mito'] if x['facts']['wt']), flush=True)
# endosomas y microtúbulos, fusionados
for org, cls, budget in [('endo_seg', 'endo', 160000), ('mt-out_seg', 'mt', 180000)]:
    vs, fs, off, n = [], [], 0, 0
    for r, o in by[org]:
        V, F = build(frags(r, data, o), region, 0.6, crop=False)
        if V is None or inside(V, region).mean() < 0.5: continue
        vs.append(V); fs.append(F + off); off += len(V); n += 1
    V = np.vstack(vs); F = np.vstack(fs); print(cls, 'objs', n, 'faces', len(F), flush=True)
    put(cls, cls.upper(), *final(V, F, budget), count=n)
pickle.dump(out, open(sys.argv[2], 'wb'))
print('done', flush=True)
