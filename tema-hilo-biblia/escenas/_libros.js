// Los 66 libros: abreviatura, capítulos y grupo (TNM de estudio, "Tabla de los libros de la Biblia" y "Pregunta 19").
// Los colores de grupo evitan el oro, que en este video es solo la línea de la descendencia.
const LIBROS = [["Gé",50,0],["Éx",40,0],["Le",27,0],["Nú",36,0],["Dt",34,0],["Jos",24,1],["Jue",21,1],["Rut",4,1],["1Sa",31,1],["2Sa",24,1],["1Re",22,1],["2Re",25,1],["1Cr",29,1],["2Cr",36,1],["Esd",10,1],["Ne",13,1],["Est",10,1],["Job",42,2],["Sl",150,2],["Pr",31,2],["Ec",12,2],["Can",8,2],["Is",66,3],["Jer",52,3],["Lam",5,3],["Eze",48,3],["Da",12,3],["Os",14,3],["Joe",3,3],["Am",9,3],["Abd",1,3],["Jon",4,3],["Miq",7,3],["Na",3,3],["Hab",3,3],["Sof",3,3],["Ag",2,3],["Zac",14,3],["Mal",4,3],["Mt",28,4],["Mr",16,4],["Lu",24,4],["Jn",21,4],["Hch",28,5],["Ro",16,6],["1Co",16,6],["2Co",13,6],["Gál",6,6],["Ef",6,6],["Flp",4,6],["Col",4,6],["1Te",5,6],["2Te",3,6],["1Ti",6,6],["2Ti",4,6],["Tit",3,6],["Flm",1,6],["Heb",13,6],["Snt",5,6],["1Pe",5,6],["2Pe",3,6],["1Jn",5,6],["2Jn",1,6],["3Jn",1,6],["Jud",1,6],["Ap",22,7]];
const GRUPOS = [
  { n: "Pentateuco", c: "#a7b8cc" }, { n: "Históricos", c: "#94b8a6" }, { n: "Poéticos", c: "#b3a1d9" },
  { n: "Proféticos", c: "#cfa6c8" }, { n: "Evangelios", c: "#8fcfc4" }, { n: "Hechos", c: "#7fb2d9" },
  { n: "Cartas", c: "#9fa6ee" }, { n: "Apocalipsis", c: "#d6d9e0" },
];
