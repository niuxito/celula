# Herramientas de preparación de datos

Scripts usados para generar `models/` y `data/` a partir del conjunto jrc_hela-2 de OpenOrganelle.
Dependencias de Python: `numpy`, `scipy`, `trimesh`, `DracoPy`, `pyfqmr`, `fast-simplification` y gltfpack (npm).

| Orden | Script | Qué hace |
|---|---|---|
| 1 | `00_descargar_openorganelle.js` | Se ejecuta en la consola del navegador en openorganelle.janelia.org. Descarga de cada orgánulo solo un nivel de detalle (peticiones HTTP Range) y lo empaqueta en `hela2_organulos.bin` y `hela2_vesiculas.bin` |
| 2 | `decode.py` | Lee esos paquetes y decodifica los fragmentos Draco a µm (vóxel de 4 × 4 × 5,24 nm) |
| 3 | `01_mascara_celula.py` | Delimita la célula central a partir de su membrana para descartar las células vecinas |
| 4 | `02_procesar.py hela2_organulos.bin proc1.pkl` | Recorta, une los fragmentos (simplificación con los bordes preservados) y simplifica cada clase de orgánulo; mide las mitocondrias y el núcleo |
| 5 | `03_vesiculas.py hela2_vesiculas.bin` | Lo mismo para las vesículas → `proc_ves.pkl` |
| 6 | `content.py` | Fichas en español |
| 7 | `export.py` | `proc1.pkl` + `proc_ves.pkl` → GLB por orgánulo, `models/*.txt` (base64) y `anatomia.json` |

> Nota: algunas rutas absolutas del entorno donde se generaron los datos (por ejemplo `/home/claude/...`) siguen en los scripts. Ajústalas a tu equipo antes de ejecutarlos.
