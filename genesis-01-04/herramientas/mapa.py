"""Cartografía de Natural Earth con proyección equirectangular regional.

Los cauces vienen del conjunto cartográfico, no de puntos dibujados a ojo.
El óvalo de Edén comunica una referencia tradicional sin límites conocidos.
"""
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAP=ROOT/'mapas'
def xy(lon,lat):return 65+(lon-23)*49*math.cos(math.radians(36)), 704-(lat-28)*49
def path(points,closed=False):
    return ' '.join(('M' if i==0 else 'L')+f'{xy(*p[:2])[0]:.1f},{xy(*p[:2])[1]:.1f}' for i,p in enumerate(points))+('Z' if closed else '')
def label(lon,lat,t,size=29,anchor='middle',color='#425e61'):
    x,y=xy(lon,lat);return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="font-size:{size}px;fill:{color};font-weight:550">{t}</text>'
parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1768 728" width="1768" height="728" aria-label="Mapa real de Asia sudoccidental con los cursos actuales de los ríos">','<rect width="1768" height="728" fill="#c6dcdb"/>']
selected={'Turkey','Türkiye','Syria','Iraq','Iran','Armenia','Azerbaijan','Georgia','Lebanon','Jordan','Israel','Saudi Arabia','Kuwait','Cyprus','Palestine','Russia'}
for f in json.loads((MAP/'paises.geojson').read_text())['features']:
    props=f['properties'];name=props.get('ADMIN') or props.get('NAME')
    if name not in selected:continue
    geo=f['geometry'];polys=geo['coordinates'] if geo['type']=='MultiPolygon' else [geo['coordinates']]
    for poly in polys:
        d=' '.join(path(r,True) for r in poly)
        parts.append(f'<path d="{d}" fill="#f1e8d5" stroke="#b5b5a1" stroke-width="2" fill-rule="evenodd"/>')
for f in json.loads((MAP/'lagos.geojson').read_text())['features']:
    if f['properties'].get('name') not in ['Lake Van','Lake Urmia','Caspian Sea']:continue
    g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    for poly in polys:parts.append(f'<path d="{" ".join(path(r,True) for r in poly)}" fill="#91bec3" stroke="#58898f" stroke-width="2"/>')
rivers=[]
for f in json.loads((MAP/'rios.geojson').read_text())['features']:
    if f['properties'].get('name') not in ['Euphrates','Al Furat','Firat','Murat','Tigris']:continue
    g=f['geometry'];lines=g['coordinates'] if g['type']=='MultiLineString' else [g['coordinates']]
    for points in lines:
        d=path(points)
        parts.append(f'<path d="{d}" fill="none" stroke="#397b88" stroke-width="6" stroke-linecap="round"/>')
        rivers.append(f'<path d="{d}" fill="none" stroke="#bd8c30" stroke-width="4" data-p="0" data-motion="draw" data-draw-duration="2.2"/>')
for args in [(35.2,39.5,'TURQUÍA',32),(38.3,34.5,'SIRIA',30),(43.7,32.2,'IRAK',32),(49,36.6,'IRÁN',32),(29,34,'Mediterráneo',28),(30,42,'Mar Negro',28),(39,35.8,'Éufrates',30),(46.3,33.8,'Tigris',30),(44.7,38.8,'Lago Van',28)]:parts.append(label(*args))
x,y=xy(44.3,39.7);parts.append(f'<path d="M{x-11},{y+9} L{x},{y-13} L{x+11},{y+9}Z" fill="#755431"/>')
parts.append(label(44.7,40.25,'Ararat',29,'start','#755431'))
x,y=xy(42.4,38.05)
parts.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="60" ry="32" fill="#efbe66" fill-opacity=".25" stroke="#8c641e" stroke-width="4" stroke-dasharray="9 8"/>')
parts.append(label(40.7,37,'Zona tradicional',24,'middle','#775516'))
parts.append('</svg>')
(MAP/'atlas.svg').write_text(''.join(parts))
(MAP/'rios.svg').write_text('<svg viewBox="0 0 1768 728" width="1768" height="728" style="position:absolute;inset:0;pointer-events:none" aria-hidden="true">'+''.join(rivers)+'</svg>')
(MAP/'FUENTES.md').write_text('# Base cartográfica\n\nNatural Earth, dominio público. Proyección equirectangular con paralelo de referencia 36°. No se usan las fronteras actuales para atribuir territorio al relato antiguo.\n\n'+ '\n'.join('- https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'+s for s in ['ne_50m_admin_0_countries.geojson','ne_10m_rivers_lake_centerlines.geojson','ne_10m_lakes.geojson'])+'\n\nEl contorno de la zona tradicional es una marca ilustrativa de incertidumbre, no un límite arqueológico. Texto: Perspicacia, «Edén», pág. 733, según la investigación proporcionada.\n')
print('Mapa real escrito con cauces vectoriales')
