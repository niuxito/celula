// Textos de la interfaz por idioma. Para añadir un idioma:
//  1. añade su código a LANGS y a LANG_NAMES, y un bloque en STR (lo que falte se toma del español);
//  2. crea data/anatomia.<código>.js con las fichas traducidas (ver CONTRIBUTING.md).
export const LANGS = ['es', 'en'];
export const LANG_NAMES = {es: 'Español', en: 'English'};

export function detectLang(){
  const q = new URLSearchParams(location.search).get('lang');
  if (LANGS.includes(q)) return q;
  try { const s = localStorage.getItem('lang'); if (LANGS.includes(s)) return s; } catch (e) {}
  const nav = (navigator.languages || [navigator.language || 'es']).map(l => l.slice(0, 2).toLowerCase());
  return nav.find(l => LANGS.includes(l)) || 'en';
}

const A = (href, txt) => `<a href="${href}" target="_blank" rel="noopener">${txt}</a>`;
const DS = 'https://openorganelle.janelia.org/datasets/jrc_hela-2';
const HEINRICH = 'https://doi.org/10.1038/s41586-021-03977-3', XU = 'https://doi.org/10.1038/s41586-021-03992-4';

export const STR = {
  es: {
    title: 'Célula humana en capas',
    metaDesc: 'Visor 3D interactivo de una célula HeLa real reconstruida por microscopía electrónica (OpenOrganelle): 265 mitocondrias, retículo, Golgi, núcleo y más, en capas. Disponible en español e inglés.',
    brand: 'Célula humana <em>en capas</em>',
    langLabel: 'Idioma',
    views: 'Vistas', top: 'Superior', bottom: 'Desde el sustrato', front: 'Frontal', right: 'Lateral',
    spin: 'Girar', reset: 'Restablecer',
    panelLayers: 'Capas y orgánulos', panelCard: 'Ficha de la estructura',
    tabs: 'Paneles', tabModel: 'Modelo', tabLayers: 'Capas', tabCard: 'Ficha',
    searchPh: 'Buscar orgánulo (p. ej. «mitocondria», «Golgi»)', search: 'Buscar estructura',
    peel: 'Pelar capas', peelAll: 'Todo', peelMembrane: 'Sin membrana', peelOrganelles: 'Orgánulos', peelNucleus: 'Núcleo',
    loading: 'Cargando modelo de la célula…',
    credit: `Datos: ${A(DS, 'OpenOrganelle jrc_hela-2')} · Heinrich et al. (2021), Xu et al. (2021), <i>Nature</i> · HHMI Janelia · ${A('https://creativecommons.org/licenses/by/4.0/deed.es', 'CC BY 4.0')} · simplificado para web · ${A('https://github.com/niuxito/celula', 'código en GitHub')}`,
    sideD: 'Lado derecho', sideI: 'Lado izquierdo', sideDs: 'dcho.', sideIs: 'izq.',
    stats: (mito, c) => `Célula HeLa · ${mito} mitocondrias · ${c} tipos de orgánulo · FIB-SEM`,
    systemReady: (name, d, total) => `${name} listo (${d}/${total})`,
    modelDone: 'Modelo completo',
    errSystem: name => `No se pudo cargar ${name}.`,
    errData: msg => `Error al cargar los datos: ${msg}`,
    toggleSys: name => `Mostrar u ocultar ${name}`, showGroup: name => `Mostrar ${name}`,
    opacity: 'Opacidad', noResults: 'Sin resultados',
    howTo: 'Cómo usarlo', selectAny: 'Selecciona cualquier orgánulo de la célula',
    how1: 'Arrastra para girar, rueda o pellizca para acercar y clic derecho para desplazar.',
    how2: 'Haz clic en un orgánulo para ver su nombre y su ficha. Cada mitocondria tiene sus propias medidas.',
    how3: 'Usa <b>Pelar capas</b> o el ojo de cada orgánulo para retirar la membrana y ver el interior; ajusta la opacidad para ver a través.',
    how4: 'Atajos: <kbd>Esc</kbd> deseleccionar · <kbd>F</kbd> enfocar · <kbd>H</kbd> ocultar · <kbd>I</kbd> aislar',
    systemsIncluded: 'Orgánulos incluidos',
    aboutTitle: 'Acerca del modelo y su rigor',
    about: `<p>No es un dibujo: es una célula real. Las formas proceden del conjunto de datos ${A(DS, 'jrc_hela-2 de OpenOrganelle')} (HHMI Janelia). Es una célula HeLa humana en interfase, congelada a alta presión y escaneada entera por microscopía electrónica de barrido con haz de iones focalizado (FIB-SEM), con vóxeles de 4 × 4 × 5,24 nm. Los orgánulos fueron segmentados con redes neuronales y revisados por el equipo COSEM: ${A(HEINRICH, 'Heinrich et al., <i>Nature</i> 2021')}; imagen: ${A(XU, 'Xu et al., <i>Nature</i> 2021')}.</p>
        <p><b>Qué se ha hecho para este visor.</b></p>
        <ul><li>Se han usado los niveles de detalle intermedios de las mallas originales y se han simplificado para la web. Las formas y posiciones son las reales; el detalle fino de las membranas es menor que en el original.</li>
        <li>El volumen escaneado incluye trozos de células vecinas. Aquí solo se muestran la membrana, el núcleo y los orgánulos de la célula central, separados automáticamente según su posición.</li>
        <li>Las medidas de cada mitocondria y del núcleo se han calculado sobre las mallas del visor y son aproximadas.</li>
        <li>Las 26.364 vesículas de la célula se muestran con su forma y posición reales, pero muy simplificadas por su número.</li>
        <li>Los colores son convencionales: en la microscopía electrónica no hay color.</li></ul>
        <p>Licencia de los datos: ${A('https://doi.org/10.25378/janelia.13108343', 'CC BY 4.0')} (Janelia Research Campus).</p>
        <p><b>Qué no aparece.</b> Ribosomas, filamentos de actina y filamentos intermedios, centrosoma, nucléolo, poros nucleares y lisosomas como clase aparte. Están en la célula, pero no forman parte de las mallas publicadas de este conjunto de datos. Por eso el citoplasma parece vacío, aunque en realidad está abarrotado de proteínas.</p>
        <p><b>Sobre las células HeLa.</b> Proceden de un tumor de cuello uterino de Henrietta Lacks, extraído en 1951 sin su consentimiento, como era habitual entonces. Son la primera línea celular humana inmortal y han sido clave en avances como la vacuna de la polio.</p>
        <p><b>Uso educativo.</b> Las fichas no han sido revisadas por especialistas; un docente debería revisarlas antes de usarlas en el aula.</p>`,
    focus: 'Enfocar', isolate: 'Aislar', showAll: 'Ver todo', hide: 'Ocultar',
    dimRest: 'Atenuar el resto de la célula',
    source: id => `Fuente: OpenOrganelle jrc_hela-2 (HHMI Janelia) · pieza ${id}`,
    factKey: k => k, factVal: v => v, num: n => n,
  },
  en: {
    title: 'Layered Human Cell',
    metaDesc: 'Interactive 3D viewer of a real HeLa cell reconstructed by electron microscopy (OpenOrganelle): 265 mitochondria, ER, Golgi, nucleus and more, in layers. Available in Spanish and English.',
    brand: 'Layered <em>human cell</em>',
    langLabel: 'Language',
    views: 'Views', top: 'Top', bottom: 'From the substrate', front: 'Front', right: 'Side',
    spin: 'Rotate', reset: 'Reset',
    panelLayers: 'Layers and organelles', panelCard: 'Structure card',
    tabs: 'Panels', tabModel: 'Model', tabLayers: 'Layers', tabCard: 'Card',
    searchPh: 'Search organelle (e.g. "mitochondrion", "Golgi")', search: 'Search structure',
    peel: 'Peel layers', peelAll: 'All', peelMembrane: 'No membrane', peelOrganelles: 'Organelles', peelNucleus: 'Nucleus',
    loading: 'Loading cell model…',
    credit: `Data: ${A(DS, 'OpenOrganelle jrc_hela-2')} · Heinrich et al. (2021), Xu et al. (2021), <i>Nature</i> · HHMI Janelia · ${A('https://creativecommons.org/licenses/by/4.0/deed.en', 'CC BY 4.0')} · simplified for the web · ${A('https://github.com/niuxito/celula', 'code on GitHub')}`,
    sideD: 'Right side', sideI: 'Left side', sideDs: 'R', sideIs: 'L',
    stats: (mito, c) => `HeLa cell · ${mito} mitochondria · ${c} organelle types · FIB-SEM`,
    systemReady: (name, d, total) => `${name} ready (${d}/${total})`,
    modelDone: 'Model complete',
    errSystem: name => `Could not load ${name}.`,
    errData: msg => `Error loading data: ${msg}`,
    toggleSys: name => `Show or hide ${name}`, showGroup: name => `Show ${name}`,
    opacity: 'Opacity', noResults: 'No results',
    howTo: 'How to use it', selectAny: 'Select any organelle of the cell',
    how1: 'Drag to rotate, scroll or pinch to zoom, and right-click to pan.',
    how2: 'Click an organelle to see its name and its card. Each mitochondrion has its own measurements.',
    how3: 'Use <b>Peel layers</b> or the eye on each organelle to remove the membrane and see inside; adjust opacity to see through.',
    how4: 'Shortcuts: <kbd>Esc</kbd> deselect · <kbd>F</kbd> focus · <kbd>H</kbd> hide · <kbd>I</kbd> isolate',
    systemsIncluded: 'Organelles included',
    aboutTitle: 'About the model and its rigor',
    about: `<p>This is not a drawing: it is a real cell. The shapes come from the ${A(DS, 'OpenOrganelle jrc_hela-2')} dataset (HHMI Janelia). It is a human HeLa cell in interphase, high-pressure frozen and scanned whole by focused ion beam scanning electron microscopy (FIB-SEM), with 4 × 4 × 5.24 nm voxels. The organelles were segmented with neural networks and reviewed by the COSEM team: ${A(HEINRICH, 'Heinrich et al., <i>Nature</i> 2021')}; imaging: ${A(XU, 'Xu et al., <i>Nature</i> 2021')}.</p>
        <p><b>What was done for this viewer.</b></p>
        <ul><li>Intermediate levels of detail of the original meshes were used and simplified for the web. Shapes and positions are real; the fine detail of the membranes is lower than in the original.</li>
        <li>The scanned volume includes pieces of neighboring cells. Only the membrane, nucleus and organelles of the central cell are shown here, separated automatically by position.</li>
        <li>The measurements of each mitochondrion and of the nucleus were computed on the viewer's meshes and are approximate.</li>
        <li>The cell's 26,364 vesicles are shown with their real shape and position, but heavily simplified because of their number.</li>
        <li>Colors are conventional: electron microscopy has no color.</li></ul>
        <p>Data license: ${A('https://doi.org/10.25378/janelia.13108343', 'CC BY 4.0')} (Janelia Research Campus).</p>
        <p><b>What is not shown.</b> Ribosomes, actin and intermediate filaments, centrosome, nucleolus, nuclear pores and lysosomes as a separate class. They are in the cell, but they are not part of the published meshes of this dataset. That is why the cytoplasm looks empty, although it is actually packed with proteins.</p>
        <p><b>About HeLa cells.</b> They come from a cervical tumor of Henrietta Lacks, removed in 1951 without her consent, as was common at the time. They are the first immortal human cell line and have been key to advances such as the polio vaccine.</p>
        <p><b>Educational use.</b> The cards have not been reviewed by specialists; a teacher should review them before classroom use. The cards were written in Spanish; the English cards are a translation.</p>`,
    focus: 'Focus', isolate: 'Isolate', showAll: 'Show all', hide: 'Hide',
    dimRest: 'Dim the rest of the cell',
    source: id => `Source: OpenOrganelle jrc_hela-2 (HHMI Janelia) · piece ${id}`,
    // Datos medidos que viajan en español en data/anatomia.js (campos y valores de cada pieza)
    factKey: k => ({'Tamaño en esta célula':'Size in this cell', 'Volumen medido':'Measured volume', 'Esta mitocondria':'This mitochondrion',
      'Longitud':'Length', 'Volumen':'Volume', 'Piezas en esta célula':'Pieces in this cell'}[k] ?? k),
    factVal: v => v.replace(/^n\.º (\d+) de (\d+) \(ordenadas de mayor a menor longitud\)$/, 'No. $1 of $2 (sorted longest to shortest)')
      .replace(/(\d),(\d)/g, '$1.$2').replace(/^\d{1,3}(\.\d{3})+$/, m => m.replace(/\./g, ',')),
    num: n => n.replace(/^n\.º\s*/, 'No. '),
  },
};
