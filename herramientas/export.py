# -*- coding: utf-8 -*-
import pickle, json, os, subprocess, base64, numpy as np, trimesh
from content import SYSTEMS, C
OUT = '/home/claude/cellsite/'; os.makedirs(OUT + 'models', exist_ok=True)
out = pickle.load(open('proc1.pkl', 'rb'))
if os.path.exists('proc_ves.pkl'): out.update(pickle.load(open('proc_ves.pkl', 'rb')))
COL = {'pm': '#a9cfe0', 'nuc': '#7a68c9', 'er': '#e6b54e', 'golgi': '#3fb393', 'mito': '#e2614d', 'endo': '#c56cb4', 'ves': '#d8cf62', 'mt': '#5cc4e2'}
allv = np.vstack([o['v'] for o in out['pm']])
lo, hi = allv.min(0), allv.max(0)
shift = np.array([-(lo[0] + hi[0]) / 2, -lo[1], -(lo[2] + hi[2]) / 2])
parts = []
def fmt(x, d=2): return f"{x:.{d}f}".replace('.', ',')
for cls in ['pm', 'nuc', 'er', 'golgi', 'mito', 'endo', 'ves', 'mt']:
    objs = out.get(cls, [])
    if cls == 'mito': objs = sorted(objs, key=lambda o: -o['facts']['length'])
    for k, o in enumerate(objs):
        pf = []; num = ''
        if cls == 'mito':
            m = trimesh.Trimesh(o['v'], o['f'], process=False)
            num = f'n.º {k+1}'
            pf = [["Esta mitocondria", f"{num} de {len(objs)} (ordenadas de mayor a menor longitud)"], ["Longitud", f"≈{fmt(o['facts']['length'])} µm"], ["Volumen", f"≈{fmt(abs(m.volume), 3)} µm³"]]
        if cls == 'nuc':
            e = sorted(o['facts']['ext'], reverse=True)
            pf = [["Tamaño en esta célula", f"≈{fmt(e[0],1)} × {fmt(e[1],1)} × {fmt(e[2],1)} µm"], ["Volumen medido", f"≈{round(o['facts']['vol'])} µm³"]]
        if cls in ('endo', 'mt', 'ves'):
            pf = [["Piezas en esta célula", f"{o['facts']['count']:,}".replace(',', '.')]]
        if cls == 'golgi':
            num = ''
        parts.append(dict(id=o['id'], k=cls, num=num, pf=pf, col=COL[cls], v=o['v'] + shift, f=o['f']))
ckeys = sorted({p['k'] for p in parts}); cidx = {k: i for i, k in enumerate(ckeys)}
sysmap = {s[0]: s for s in SYSTEMS}
data = {'systems': [{'k': k, 'n': n, 'c': c, 'layer': L, 'd': d} for k, n, c, L, d in SYSTEMS if k in {p['k'] for p in parts}],
        'concepts': [dict(C[k]) for k in ckeys], 'parts': [], 'files': {}}
bysys = {}
for p in parts:
    data['parts'].append({'id': p['id'], 'c': cidx[p['k']], 'sd': '', 'en': '', 'col': p['col'], 'num': p['num'], 'pf': p['pf']})
    bysys.setdefault(C[p['k']]['s'], []).append(p)
for s, lst in bysys.items():
    sc = trimesh.Scene()
    for p in lst: sc.add_geometry(trimesh.Trimesh(p['v'], p['f'], process=False), node_name=p['id'], geom_name=p['id'])
    raw = f'/home/claude/cell/raw_{s}.glb'; sc.export(raw)
    glb = OUT + f'models/{s}.glb'
    subprocess.run(['/home/claude/node_modules/.bin/gltfpack', '-i', raw, '-o', glb, '-cc', '-kn', '-vn', '10'], check=True, capture_output=True)
    b64 = base64.b64encode(open(glb, 'rb').read()); open(OUT + f'models/{s}.txt', 'wb').write(b64)
    data['files'][s] = {'bytes': len(b64), 'tris': int(sum(len(p['f']) for p in lst))}
    print(s, len(lst), data['files'][s])
data['meta'] = {'extent': (hi - lo).tolist(), 'mito': len(out.get('mito', [])), 'shift': shift.tolist()}
json.dump(data, open(OUT + 'anatomia.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('extent µm', (hi - lo).round(1), 'parts', len(data['parts']))
