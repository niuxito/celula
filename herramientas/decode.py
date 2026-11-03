import json, struct, sys, numpy as np, DracoPy, pickle
# Bundle: b'HCB1' | u32 headerLen | header JSON (list of recs) | concatenated fragment data (recs order)
BITS = 10
T = np.array([4.0, 4.0, 5.24])  # nm por vóxel (transform de info)

def load(path):
    raw = open(path, 'rb').read()
    assert raw[:4] == b'HCB1', raw[:4]
    hl = struct.unpack('<I', raw[4:8])[0]
    recs = json.loads(raw[8:8 + hl]); data = memoryview(raw)[8 + hl:]
    return recs, data

def decode_rec(r, data, off):
    lod = r['lod']; scale = 2 ** lod
    chunk = np.array(r['chunk']); origin = np.array(r['origin']); voff = np.array(r['voff'])
    V, F, nv = [], [], 0; o = off
    for px, py, pz, sz in r['frags']:
        blob = bytes(data[o:o + sz]); o += sz
        m = DracoPy.decode(blob)
        p = np.asarray(m.points, dtype=np.float64).reshape(-1, 3)
        f = np.asarray(m.faces, dtype=np.int64).reshape(-1, 3)
        if len(p) == 0 or len(f) == 0: continue
        pos = origin + voff + chunk * scale * (np.array([px, py, pz]) + p / (2 ** BITS - 1))
        V.append(pos * T / 1000.0)  # µm
        F.append(f + nv); nv += len(p)
    if not V: return None, None, o
    return np.vstack(V), np.vstack(F), o

if __name__ == '__main__':
    recs, data = load(sys.argv[1])
    out = {}; off = 0
    for r in recs:
        V, F, off2 = decode_rec(r, data, off)
        assert off2 - off == r['n'], (r['org'], r['id'], off2 - off, r['n'])
        off = off2
        if V is not None: out.setdefault(r['org'], []).append((r['id'], V.astype(np.float32), F.astype(np.int32)))
    for k, v in out.items():
        print(k, len(v), 'objs', sum(len(f) for _, _, f in v), 'tris')
    pickle.dump(out, open(sys.argv[2], 'wb'))
