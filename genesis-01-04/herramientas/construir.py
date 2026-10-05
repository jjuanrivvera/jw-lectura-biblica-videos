#!/usr/bin/env python3
"""Compone escenas independientes con movimientos anclados al VTT del audio real."""
import html
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / 'video'
SCENES = ROOT / 'escenas'
FONT = '''@font-face{font-family:Fraunces;src:url("assets/fonts/Fraunces.ttf");font-weight:100 900}
@font-face{font-family:Montserrat;src:url("assets/fonts/Montserrat.ttf");font-weight:100 900}
@font-face{font-family:Caveat;src:url("assets/fonts/Caveat.ttf");font-weight:400 700}'''

def norm(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()))

def ptime(scene, p):
    target = norm(re.split(r'[.?!]', scene['paragraphs'][int(p)], maxsplit=1)[0])[:65]
    for cue in scene['cues']:
        if target in norm(cue['text']):
            return cue['start']
    raise ValueError(f'No se encuentra el párrafo {p} de {scene["id"]}: {target}')

def cue_time(scene, phrase):
    matches = [c['start'] for c in scene['cues'] if norm(phrase) in norm(c['text'])]
    if len(matches) != 1:
        raise ValueError(f'Ancla ambigua o ausente {scene["id"]}: {phrase} ({len(matches)})')
    return matches[0]

def build():
    meta = json.loads((VIDEO / 'audio/escenas.json').read_text())
    base = (SCENES / 'base.css').read_text()
    lib = (SCENES / 'runtime.js').read_text()
    config = json.loads((SCENES / 'contenido.json').read_text())
    total = 0.0
    timeline = []
    storyboard = ['# Storyboard ejecutado\n\nCada movimiento se ancla al VTT de la misma escena.\n']
    hosts, audios = [], []
    for item in meta:
        n = item['id']
        cfg = config[n]
        ident = 'escena-' + n
        markup = (SCENES / (n + '.html')).read_text()
        markup = markup.replace('<!--ATLAS-->', (ROOT / 'mapas/atlas.svg').read_text())
        markup = markup.replace('<!--RIVERS-->', (ROOT / 'mapas/rios.svg').read_text())
        def replace_paragraph(m):
            return f'data-at="{ptime(item, m[1]):.3f}"'
        def replace_anchor(m):
            return f'data-at="{cue_time(item, html.unescape(m[1])):.3f}"'
        markup = re.sub(r'data-p="(\d+)"', replace_paragraph, markup)
        markup = re.sub(r'data-cue="([^"]+)"', replace_anchor, markup)
        markup = re.sub(r'data-until-p="(\d+)"', lambda m:f'data-until="{ptime(item,m[1]):.3f}"', markup)
        markup = re.sub(r'data-move-cue="([^"]+)"', lambda m:f'data-move-at="{cue_time(item,html.unescape(m[1])):.3f}"', markup)
        own = cfg.get('own')
        if own:
            markup += f'<div class="tag own">{own}</div>'
        element_index = 0
        def identify(match):
            nonlocal element_index
            element_index += 1
            tag = match[0]
            if re.search(r'\bid="', tag):
                return tag
            return re.sub(r'^(<[\w:-]+)', rf'\1 id="{ident}-el-{element_index}"', tag)
        markup = re.sub(r'<[A-Za-z][\w:-]*\b[^>]*>', identify, markup)
        chapter = cfg['chapter']
        duration = item['duration']
        content = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{item['title']}</title></head><body><template>
<style>{FONT}\n#{ident}{{position:absolute;inset:0;width:100%;height:100%;{base}}}</style>
<div id="{ident}" data-composition-id="{ident}" data-width="1920" data-height="1080" data-duration="{duration}" >
<div class="scene-content {'lesson' if int(n)>=36 else ''}"><div class="chapter">{chapter}</div><div class="scene-count">{int(n)+1:02d} / 42</div>
<h1 id="{ident}-title" class="title">{cfg.get('title',item['title'])}</h1><div class="header-line"></div>
<div class="stage">{markup}</div><div class="source">{cfg['source']}</div><div id="{ident}-progress" class="progress" aria-hidden="true"></div></div></div>
<script>(()=>{{const ID="{ident}";const DUR={duration};{lib}\nwindow.__timelines=window.__timelines||{{}};window.__timelines[ID]=tl;}})();</script>
</template></body></html>'''
        path = VIDEO / 'compositions' / f'{ident}.html'
        path.write_text(content)
        motion = {'duration':duration,'assertions':[{'kind':'appearsBy','selector':f'#{ident} .title','bySec':0.8},
                 {'kind':'staysInFrame','selector':f'#{ident} .title'}]}
        path.with_suffix('.motion.json').write_text(json.dumps(motion,indent=2))
        hosts.append(f'<div class="clip" id="host-{n}" data-composition-id="{ident}" data-composition-src="compositions/{ident}.html" data-start="{total:.3f}" data-duration="{duration:.3f}" data-track-index="1" data-width="1920" data-height="1080"></div>')
        audios.append(f'<audio class="clip" id="voz-{n}" src="audio/escena-{n}.mp3" data-start="{total:.3f}" data-duration="{duration:.3f}" data-track-index="{2+int(n)%2}" data-volume="1"></audio>')
        beats = sorted(set([float(x) for x in re.findall(r'data-at="([\d.]+)"',markup)]))
        timeline.append({'id':n,'title':item['title'],'start':round(total,3),'duration':duration,'beats':beats,
                         'source':cfg['source'],'chapter':chapter})
        storyboard.append(f'## Frame {int(n)+1}\nstatus: animated\nsrc: compositions/{ident}.html\nshape: {cfg["shape"]}\nrules: svg-path-draw, stat-bars-and-fills, asr-keyword-glow\nbeat: {item["title"]}\n')
        total += duration
    index = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=1920,height=1080"><title>Génesis 1 al 4</title>
<script src="assets/gsap.min.js"></script><style>{FONT}
*{{box-sizing:border-box;margin:0}}html,body{{width:1920px;height:1080px;overflow:hidden;background:#172c33}}#root{{position:relative;width:100%;height:100%;overflow:hidden;background:#172c33}}</style></head><body>
<div id="root" data-composition-id="genesis-01-04" data-width="1920" data-height="1080" data-duration="{total:.3f}">
{''.join(hosts)}{''.join(audios)}</div><script>const tl=gsap.timeline({{paused:true}});window.__timelines=window.__timelines||{{}};window.__timelines["genesis-01-04"]=tl;</script></body></html>'''
    (VIDEO / 'index.html').write_text(index)
    (VIDEO / 'timeline.json').write_text(json.dumps({'duration':round(total,3),'scenes':timeline},ensure_ascii=False,indent=2))
    assertions = [{'kind':'staysInFrame','selector':f'#escena-{s["id"]}-title'} for s in timeline]
    assertions += [{'kind':'before','a':f'#escena-{a["id"]}-title','b':f'#escena-{b["id"]}-title'}
                   for a,b in zip(timeline,timeline[1:])]
    (VIDEO / 'index.motion.json').write_text(json.dumps({'duration':round(total,3),'assertions':assertions},indent=2))
    (VIDEO / 'STORYBOARD.md').write_text('\n'.join(storyboard))
    (ROOT / 'trabajo/tiempos-check.txt').write_text(','.join(str(round(s['start']+s['duration']/2,3)) for s in timeline))
    print(f'{len(meta)} escenas · {total:.3f} s · {int(total//60)}:{total%60:05.2f}')

if __name__ == '__main__':
    build()
