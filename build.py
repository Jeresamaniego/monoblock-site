# Arma index.html desde index.template.html: pasa los colores de los atributos SVG a style (var() en
# atributos no anda igual en todos los navegadores) y mete las curvas de nivel de la gema del hero.
import re, pathlib
here = pathlib.Path(__file__).parent
s = (here / "index.template.html").read_text()
s = re.sub(r'\b(fill|stroke|opacity)="((?:var|color-mix)\([^"]*\))"', lambda m: f'style="{m.group(1)}:{m.group(2)}"', s)
def merge(tag):
    t = tag.group(0); styles = re.findall(r'style="([^"]*)"', t)
    if len(styles) <= 1: return t
    end = '/>' if t.endswith('/>') else '>'
    t = re.sub(r'\s*style="[^"]*"', '', t)
    return t[:-len(end)].rstrip() + ' style="' + ';'.join(styles) + '"' + end
s = re.sub(r'<[a-zA-Z][^<>]*>', merge, s)
contours = (here / "gem-contours.txt").read_text().split("\n")
s = s.replace("{{CONTOURS}}", "\n              ".join(f'<path d="{d}"/>' for d in contours))
(here / "index.html").write_text(s)
print("index.html listo")
