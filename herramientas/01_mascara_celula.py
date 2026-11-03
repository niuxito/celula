"""Separa la célula central de sus vecinas: voxeliza la membrana plasmática (0,08 µm), cierra huecos dilatando
0,64 µm, rellena desde el centro del núcleo y vuelve a dilatar. -> cell_region.npy (interior) y cell_shell.npy (borde)."""
import pickle, numpy as np
from scipy import ndimage as ndi
from decode import load, decode_rec
recs, data = load('hela2_organulos.bin'); off = 0; PM = NUC = None
for r in recs:
    if r['org'] == 'pm_seg' and r['id'] == 2: PM = decode_rec(r, data, off)[0]
    if r['org'] == 'nucleus_seg' and r['id'] == 1: NUC = decode_rec(r, data, off)[0]
    off += r['n']
h = 0.08; shape = (np.array([48.1, 6.5, 33.5]) / h).astype(int) + 2
idx = np.floor(PM / h).astype(int); M = np.zeros(shape, bool); M[idx[:, 0], idx[:, 1], idx[:, 2]] = True
M = ndi.binary_dilation(M, iterations=1)
c = tuple((NUC.mean(0) / h).astype(int))
D = ndi.binary_dilation(M, iterations=8); lab, _ = ndi.label(~D); core = lab == lab[c]
np.save('cell_region.npy', ndi.binary_dilation(core, iterations=8))
np.save('cell_shell.npy', ndi.binary_dilation(core, iterations=11))
