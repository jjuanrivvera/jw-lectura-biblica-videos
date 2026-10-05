#!/usr/bin/env python3
"""Pasa fuente/investigacion.html a texto con marcas, para leerlo por secciones una sola vez.

Marcas: ## / ### / #### encabezados, [FIG n: src | pie], [OBS], [EXT], [PROPIA], [JSON clase] ...
"""
import html, json, re, sys
from html.parser import HTMLParser

MARCAS = {"obs": "OBS", "propia": "PROPIA", "idea": "IDEA", "conecta": "CONECTA", "pregunta": "PREGUNTA",
          "rd-nota": "NOTA", "glos": "GLOS", "imgnote": "IMGNOTA", "pcard": "TARJETA", "hoy": "HOY",
          "lecciones": "LECCIONES", "ext": "EXT", "exc": "EXC", "muj": "MUJ", "fn-responde": "RESPONDE",
          "cmt-verse": "VERS", "cmt-head": "CMT", "cmt-foot": "PIE", "racion": "RACION", "seat": "ASIENTO"}
BLOQUE = {"p", "div", "li", "h1", "h2", "h3", "h4", "figcaption", "blockquote", "tr", "section", "article",
          "figure", "details", "summary", "dt", "dd", "table", "ul", "ol", "aside"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.fig, self.pila = [], 0, 0, []
        self.json_clase = None
    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag in ("style",): self.skip += 1; return
        if tag == "svg": self.skip += 1; self.out.append(" [SVG] "); return
        if tag == "script":
            self.skip += 1
            if a.get("type") == "application/json": self.json_clase = a.get("class", "json"); self.skip -= 1
            return
        clases = (a.get("class") or "").split()
        if tag in BLOQUE: self.out.append("\n")
        if tag in ("h1", "h2", "h3", "h4"): self.out.append("#" * int(tag[1]) + " ")
        if tag == "li": self.out.append("- ")
        if tag == "blockquote": self.out.append("> ")
        if tag == "figure": self.fig += 1; self.out.append(f"[FIG {self.fig}] ")
        if tag == "img": self.out.append(f"[IMG {a.get('src','')} alt={a.get('alt','')!r}] ")
        if tag == "a" and a.get("href", "").startswith("http"): self.pila.append(a["href"])
        m = [MARCAS[c] for c in clases if c in MARCAS]
        if m and tag in BLOQUE | {"span"}: self.out.append("[" + "/".join(m) + "] ")
        if tag in ("td", "th"): self.out.append(" | ")
        if tag == "br": self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("style", "svg") and self.skip: self.skip -= 1; return
        if tag == "script":
            if self.json_clase: self.json_clase = None
            elif self.skip: self.skip -= 1
            return
        if tag == "a" and self.pila: self.out.append(f" <{self.pila.pop()}>")
        if tag in BLOQUE: self.out.append("\n")
    def handle_data(self, d):
        if self.json_clase:
            try: d = json.dumps(json.loads(d), ensure_ascii=False)
            except Exception: pass
            self.out.append(f"\n[JSON {self.json_clase}] {d}\n"); return
        if self.skip: return
        self.out.append(re.sub(r"\s+", " ", d))

s = open(sys.argv[1], encoding="utf-8").read()
p = P(); p.feed(s)
t = "".join(p.out)
t = re.sub(r"[ \t]+\n", "\n", t); t = re.sub(r"\n[ \t]+", "\n", t); t = re.sub(r"\n{3,}", "\n\n", t)
open(sys.argv[2], "w", encoding="utf-8").write(t)
print(len(t), "caracteres")
