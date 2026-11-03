import numpy as np, pickle, sys, fast_simplification, DracoPy
from decode import load, BITS, T
h = 0.08
region = np.load('cell_region.npy')
def inside(P, M):
    i = np.clip(np.floor(P / h).astype(int), 0, np.array(M.shape) - 1)
    return M[i[:, 0], i[:, 1], i[:, 2]]
recs, data = load(sys.argv[1])
off = 0; vs, fs, n_off, count = [], [], 0, 0
for r in recs:
    o = off; off += r['n']
    if r['org'] != 'vesicle_seg': continue
    scale = 2 ** r['lod']; chunk = np.array(r['chunk']); origin = np.array(r['origin']); voff = np.array(r['voff'])
    V, F, nv = [], [], 0
    for px, py, pz, sz in r['frags']:
        m = DracoPy.decode(bytes(data[o:o + sz])); o += sz
        p = np.asarray(m.points, dtype=np.float64).reshape(-1, 3); f = np.asarray(m.faces, dtype=np.int64).reshape(-1, 3)
        if len(p) and len(f):
            V.append((origin + voff + chunk * scale * (np.array([px, py, pz]) + p / (2 ** BITS - 1))) * T / 1000.0); F.append(f + nv); nv += len(p)
    if not V: continue
    V = np.vstack(V); F = np.vstack(F)
    if inside(V, region).mean() < 0.5: continue
    vs.append(V.astype(np.float32)); fs.append(F + n_off); n_off += len(V); count += 1
V = np.vstack(vs); F = np.vstack(fs).astype(np.int32)
print('vesicles in cell', count, 'faces', len(F), flush=True)
budget = 300000
if len(F) > budget:
    V, F = fast_simplification.simplify(V, F, target_reduction=1 - budget / len(F), agg=6)
pickle.dump({'ves': [dict(id='VES', v=V, f=F, facts={'count': count})]}, open('proc_ves.pkl', 'wb'))
print('done', len(F))
