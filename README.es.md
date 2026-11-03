# Célula humana en capas

🇬🇧 [English version](README.md)

Visor 3D interactivo de una célula humana real (línea HeLa) reconstruida por microscopía electrónica (FIB-SEM). Muestra la membrana plasmática, el núcleo, el retículo endoplasmático, el aparato de Golgi, 265 mitocondrias con sus medidas, endosomas, vesículas y microtúbulos. Incluye capas, opacidad, búsqueda y fichas. **Disponible en español e inglés**: el idioma se elige según el navegador y se cambia con el botón ES/EN (o con `?lang=es`). Las fichas en inglés son una traducción de las originales en español y no han sido revisadas por especialistas.

## Cómo usarlo

**Pruébalo en línea:** https://celula.alexisparron.com (la versión desplegada añade la analítica del sitio; el código de este repositorio no incluye ningún rastreador).

1. Clona el repositorio, o descárgalo como zip y descomprímelo.
2. Abre `index.html` con doble clic en cualquier navegador moderno (Chrome, Firefox, Edge, Safari).

Funciona sin conexión y sin instalar nada. Las tipografías van incluidas en `fonts/` (Newsreader e IBM Plex, licencia SIL OFL 1.1), así que no se contacta con ningún servidor externo.

Para modificar el visor, edita `src/visor.js` y regenera `app.js`:

```
npm ci
npm run build
```

Para publicarlo en la web basta con subir la carpeta tal cual a cualquier alojamiento estático (GitHub Pages, Netlify, Vercel…).

## Contenido del paquete

| Archivo | Qué es |
|---|---|
| `index.html` | Página del visor (estructura y estilos) |
| `src/visor.js` | **Código fuente** del visor (JavaScript legible, módulo ES) |
| `app.js` | El mismo código empaquetado con three.js, sin minificar (generado) |
| `package.json`, `package-lock.json` | Dependencias y comando para regenerar `app.js` |
| `fonts/` | Tipografías en local con sus licencias OFL |
| `herramientas/` | Scripts que prepararon las mallas y las fichas (ver `herramientas/LEEME.md`) |
| `src/i18n.js` | Textos de la interfaz por idioma |
| `data/anatomia.js` | Fichas, nombres y organización por orgánulos |
| `data/anatomia.en.js` | Capa de traducción al inglés de las fichas (se carga a demanda) |
| `models/*.js` | Mallas 3D (glTF binario comprimido con meshoptimizer, en base64) |
| `LICENSE`, `LICENSE-codigo.txt` | Licencia MIT del código |
| `LICENSE-contenido.md` | Licencia de las mallas y los textos |
| `LICENSE-three.js.txt` | Licencia MIT de three.js |

## Fuente de los datos y créditos

Conjunto de datos **jrc_hela-2** de OpenOrganelle (HHMI Janelia Research Campus, proyecto COSEM): https://openorganelle.janelia.org/datasets/jrc_hela-2
- Segmentaciones: https://doi.org/10.25378/janelia.13108343 (CC BY 4.0)
- Heinrich L. et al. (2021). *Whole-cell organelle segmentation in volume electron microscopy.* Nature 599: 141–146. https://doi.org/10.1038/s41586-021-03977-3
- Xu C.S. et al. (2021). *An open-access volume electron microscopy atlas of whole cells and tissues.* Nature 599: 147–151. https://doi.org/10.1038/s41586-021-03992-4

**Cambios realizados sobre los datos originales:**
- Se han usado niveles de detalle intermedios de las mallas multirresolución y se han simplificado.
- Se han conservado solo la membrana, el núcleo y los orgánulos de la célula central, separados por su posición.
- Las mitocondrias se han medido sobre las mallas simplificadas.
- Se han asignado colores convencionales y se han redactado fichas en español.

## Licencias

- **Código** (`index.html`, `src/`, `herramientas/` y `app.js`, salvo three.js): MIT. Ver `LICENSE-codigo.txt`.
- **Mallas y fichas** (`models/`, `data/`): CC BY 4.0. Ver `LICENSE-contenido.md`. Es obligatorio mantener la atribución a Janelia/COSEM.

## Limitaciones

No incluye ribosomas, filamentos de actina, filamentos intermedios, centrosoma, nucléolo ni poros nucleares, porque no forman parte de las mallas publicadas de este conjunto de datos. Los colores son convencionales: la microscopía electrónica no tiene color.

## Nota sobre las células HeLa

Las células HeLa proceden de un tumor de Henrietta Lacks extraído en 1951 sin su consentimiento. Desde 2013 existe un acuerdo entre su familia y los NIH sobre el uso de los datos genómicos de estas células. Este visor muestra únicamente la forma de la célula y no contiene información genética.

## Contribuir

Se agradecen correcciones de fichas, informes de errores y mejoras: ver [CONTRIBUTING.md](CONTRIBUTING.md) y el [código de conducta](CODE_OF_CONDUCT.md). Para vulnerabilidades, ver [SECURITY.md](SECURITY.md). Para citar este trabajo, usa [CITATION.cff](CITATION.cff).

## Autoría

Visor y fichas: Alexis Parrón, 2026. Desarrollado con ayuda de Claude (Anthropic).

Biblioteca 3D: [three.js](https://threejs.org) (MIT). Compresión de mallas: [meshoptimizer](https://github.com/zeux/meshoptimizer) (MIT, © Arseny Kapoulkine).
