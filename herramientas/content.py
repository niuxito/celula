# -*- coding: utf-8 -*-
# Fichas de la célula HeLa (jrc_hela-2, OpenOrganelle). Datos cuantitativos de fuentes de referencia
# (Alberts, Molecular Biology of the Cell; Lodish; Heinrich et al. 2021) redondeados y marcados como aproximados.
SYSTEMS = [
  ("pm",   "Membrana plasmática", "#9fc6d9", 0, "Límite de la célula: una bicapa de lípidos con proteínas que separa el interior del medio y controla qué entra y qué sale."),
  ("nuc",  "Núcleo", "#7d6fc4", 3, "Compartimento que guarda el ADN, rodeado por una doble membrana (la envoltura nuclear)."),
  ("er",   "Retículo endoplasmático", "#e3b04b", 2, "Red continua de túbulos y cisternas aplanadas, unida a la envoltura nuclear. Es el sistema de membranas más extenso de la célula."),
  ("golgi","Aparato de Golgi", "#4fb39a", 2, "Pilas de cisternas aplanadas que modifican, clasifican y envían proteínas y lípidos."),
  ("mito", "Mitocondrias", "#e0604f", 2, "Orgánulos de doble membrana donde se produce la mayor parte del ATP de la célula. Cada pieza es una mitocondria real de esta célula."),
  ("endo", "Endosomas", "#c46fb0", 2, "Compartimentos que reciben y clasifican el material que entra en la célula por endocitosis."),
  ("ves",  "Vesículas", "#d9d36a", 2, "Pequeñas esferas de membrana que transportan carga entre orgánulos y hacia la membrana plasmática."),
  ("mt",   "Microtúbulos", "#7fd0e8", 1, "Tubos de proteína (tubulina) del citoesqueleto que dan forma a la célula y sirven de raíles para el transporte interno."),
]
C = {}
def add(k, n, s, g, d, f=None): C[k] = {"n": n, "s": s, "g": g, "d": d, "f": f or []}

add("pm", "Membrana plasmática", "pm", "Envoltura celular",
  "Bicapa de fosfolípidos de unos 5 nm de grosor con colesterol y proteínas intercaladas: canales, transportadores, receptores y proteínas de adhesión. Es semipermeable: deja pasar libremente agua y gases, pero los iones y las moléculas grandes necesitan proteínas transportadoras o procesos como la endocitosis. Su cara externa está cubierta de azúcares (glucocáliz) que intervienen en el reconocimiento entre células. En este modelo se ven los pliegues y prolongaciones reales de la superficie celular.",
  [["Grosor", "≈5 nm (bicapa lipídica)"], ["Modelo", "Mosaico fluido (Singer y Nicolson, 1972)"], ["Componentes", "Fosfolípidos, colesterol, proteínas, glúcidos"]])
add("pm_vecina", "Membrana plasmática de una célula vecina", "pm", "Células vecinas",
  "Fragmento de una célula contigua que quedó dentro del volumen escaneado. Se muestra porque aparece en los datos originales: las células HeLa crecen en contacto unas con otras.")
add("nuc", "Núcleo", "nuc", "Núcleo",
  "Orgánulo que contiene el ADN de la célula organizado en cromatina. Lo rodea la envoltura nuclear, una doble membrana atravesada por miles de poros nucleares que controlan el paso de ARN y proteínas entre el núcleo y el citoplasma. La membrana externa se continúa con el retículo endoplasmático. En su interior está el nucléolo, donde se fabrican los ribosomas. Las células HeLa tienen un número anómalo de cromosomas (unos 80, frente a los 46 de una célula humana normal), por lo que su núcleo es grande.",
  [["Envoltura", "Doble membrana con poros nucleares"], ["Contenido", "ADN (cromatina), nucléolo, nucleoplasma"], ["Cromosomas en HeLa", "≈80 (normal humano: 46)"]])
add("nuc_vecino", "Núcleo de una célula vecina", "nuc", "Células vecinas",
  "Parte del núcleo de una célula contigua que quedó dentro del volumen escaneado.")
add("er", "Retículo endoplasmático", "er", "Sistema de endomembranas",
  "Red tridimensional y continua de túbulos y cisternas aplanadas que se extiende por todo el citoplasma y es continua con la envoltura nuclear. La parte con ribosomas adheridos (retículo rugoso) sintetiza proteínas de membrana y de secreción; la parte sin ribosomas (retículo liso) fabrica lípidos, almacena calcio y participa en la detoxificación. Este modelo permite ver lo que los dibujos simplifican: el retículo es una sola red que llega casi hasta la membrana plasmática y toca a muchos otros orgánulos.",
  [["Tipos", "Rugoso (con ribosomas) y liso"], ["Funciones", "Síntesis de proteínas y lípidos, plegamiento, reserva de Ca²⁺"], ["Continuidad", "Con la envoltura nuclear"]])
add("golgi", "Aparato de Golgi", "golgi", "Sistema de endomembranas",
  "Conjunto de pilas de cisternas aplanadas (dictiosomas), situado normalmente cerca del núcleo. Recibe proteínas y lípidos del retículo por su cara cis, los modifica (por ejemplo, añadiéndoles cadenas de azúcares) a medida que avanzan y los clasifica en su cara trans para enviarlos en vesículas a la membrana plasmática, a los lisosomas o al exterior. Lo describió Camillo Golgi en 1898.",
  [["Caras", "Cis (entrada) y trans (salida)"], ["Funciones", "Glicosilación, clasificación y envío de proteínas"]])
add("mito", "Mitocondria", "mito", "Mitocondrias",
  "Orgánulo con dos membranas: la externa es lisa y la interna forma pliegues (crestas) donde se sitúa la cadena respiratoria. Aquí se completa la respiración celular, que oxida los nutrientes con oxígeno y produce la mayor parte del ATP. Tiene su propio ADN circular (en humanos, 16 569 pares de bases y 37 genes), heredado por vía materna, y sus propios ribosomas, restos de su origen como bacteria (teoría endosimbiótica). Las mitocondrias se fusionan y se dividen continuamente: por eso en el modelo se ven con formas y tamaños muy distintos.",
  [["Membranas", "Externa e interna (con crestas)"], ["Función", "Respiración celular y síntesis de ATP"], ["ADN propio", "Circular, 16 569 pb, 37 genes"], ["Grosor típico", "≈0,5–1 µm"]])
add("endo", "Endosoma", "endo", "Sistema de endomembranas",
  "Compartimento membranoso que recibe el material incorporado por endocitosis. Los endosomas tempranos, cerca de la membrana, clasifican la carga: parte se recicla a la superficie y parte madura hacia endosomas tardíos, cuyo interior se acidifica y que acaban fusionándose con los lisosomas, donde se degrada. En este conjunto de datos la clase «endosomas» agrupa los distintos tipos de endosoma.",
  [["Tipos", "Tempranos, de reciclaje y tardíos"], ["pH interior", "≈6,5 (tempranos) a ≈5,5 (tardíos)"]])
add("ves", "Vesícula", "ves", "Sistema de endomembranas",
  "Pequeña esfera de membrana que transporta proteínas y lípidos entre compartimentos: del retículo al Golgi, del Golgi a la membrana plasmática o desde la membrana hacia dentro (endocitosis). En el modelo aparecen miles: dan idea del tráfico constante de membranas dentro de una célula.",
  [["Diámetro típico", "≈50–100 nm"], ["Cubiertas", "Clatrina, COPI, COPII (según su origen)"]])
add("mt", "Microtúbulo", "mt", "Citoesqueleto",
  "Tubo hueco de unos 25 nm de diámetro formado por 13 protofilamentos de la proteína tubulina (dímeros α y β). Crece y se acorta continuamente desde el centrosoma, cerca del núcleo, hacia la periferia. Sirve de raíl para proteínas motoras (cinesinas y dineínas) que transportan vesículas y orgánulos, y en la división celular forma el huso mitótico. Es la estructura más fina que se puede segmentar en este escáner, por lo que algunos tramos pueden aparecer cortados.",
  [["Diámetro", "≈25 nm"], ["Protofilamentos", "13"], ["Proteína", "Tubulina α/β"], ["Motores", "Cinesinas (hacia +), dineínas (hacia −)"]])
