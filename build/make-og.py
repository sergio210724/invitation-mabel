#!/usr/bin/env python3
"""Genera build/og.html (el cartel 1200x630) desde index.html.

Toma los <symbol> del archivo principal, asi que el payaso, la carpa y el
pastel nunca se quedan desincronizados con la invitacion.
"""
import re, pathlib
raiz = pathlib.Path(__file__).resolve().parent.parent
s = (raiz / 'index.html').read_text(encoding='utf-8')
defs = s[s.index('<svg width="0" height="0"'): s.index('</defs></svg>') + len('</defs></svg>')]
fonts = (raiz / 'build' / 'fonts.css').read_text(encoding='utf-8')

og = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<style>
{fonts}
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:630px;overflow:hidden;background:#FFF4F8;font-family:'Nunito',sans-serif;color:#43202F;position:relative}}
.rayos{{position:absolute;inset:-25% -20%;
  background:repeating-conic-gradient(from 8deg at 26% 58%, #FFD9E7 0deg 6.5deg, transparent 6.5deg 13deg);opacity:.75;
  -webkit-mask-image:radial-gradient(85% 95% at 26% 58%, #000 18%, transparent 74%)}}
.grana{{position:absolute;inset:0;opacity:.3;mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='150'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='150' height='150' filter='url(%23n)' opacity='.38'/%3E%3C/svg%3E")}}
.banderines{{position:absolute;top:0;left:0;width:1200px}}
.escena{{position:absolute;left:26px;bottom:58px;width:520px}}
.tienda{{width:372px}}
.payaso{{position:absolute;right:4px;bottom:34px;width:168px;height:auto}}
.globo{{position:absolute;left:-6px;top:-52px;width:96px}}
.elenco{{position:absolute;left:10px;bottom:0;display:flex;align-items:flex-end;gap:3px}}
.elenco img{{width:60px;height:auto;max-width:100%}}
.texto{{position:absolute;right:74px;top:96px;width:560px;text-align:center}}
.cinta{{position:relative;display:inline-block;padding:0 26px 44px}}
.cinta-cola{{position:absolute;top:54%;width:22px;height:56px;background:#D36BA0;z-index:0;clip-path:polygon(0 0,100% 0,100% 100%,50% 72%,0 100%)}}
.cinta-cola.izq{{left:8px;transform:rotate(7deg)}}
.cinta-cola.der{{right:8px;transform:rotate(-7deg)}}
.liston{{position:relative;z-index:1;display:block;padding:.4em 1.1em .48em;background:#F486B6;color:#fff;border-radius:5px;
  box-shadow:0 16px 26px -14px rgba(150,30,80,.95), inset 0 -5px 0 rgba(0,0,0,.09)}}
.nombre{{display:block;font-family:'Alfa Slab One',serif;font-size:64px;line-height:1.05}}
.familia{{display:block;font-weight:800;font-size:17px;letter-spacing:.12em;text-transform:uppercase;opacity:.92;margin-top:.35em}}
.guion{{font-family:'Sacramento',cursive;font-size:78px;line-height:1;color:#C43D6E;margin:2px 0 0}}
.fecha{{font-family:'Alfa Slab One',serif;font-size:31px;color:#43202F;margin-top:16px;line-height:1.4}}
.lugar{{font-weight:800;font-size:21px;color:#7C4A5E;margin-top:8px}}
</style></head><body>
{defs}
<div class="rayos"></div><div class="grana"></div>
<svg class="banderines" viewBox="0 0 480 62" aria-hidden="true">
  <path d="M-4 8 C90 40 200 34 250 12 C310 -14 400 4 484 26" fill="none" stroke="#E9A8C6" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M14 14 l15 0 l-7.5 26 z" fill="#F486B6"/><path d="M56 25 l15 0 l-7.5 26 z" fill="#A5E0CE"/>
  <path d="M100 30 l15 0 l-7.5 26 z" fill="#F6C244"/><path d="M144 27 l15 0 l-7.5 26 z" fill="#F486B6"/>
  <path d="M188 17 l15 0 l-7.5 26 z" fill="#A5E0CE"/><path d="M232 6 l15 0 l-7.5 26 z" fill="#F6C244"/>
  <path d="M276 1 l15 0 l-7.5 26 z" fill="#F486B6"/><path d="M320 3 l15 0 l-7.5 26 z" fill="#A5E0CE"/>
  <path d="M364 11 l15 0 l-7.5 26 z" fill="#F6C244"/><path d="M408 19 l15 0 l-7.5 26 z" fill="#F486B6"/>
  <path d="M450 25 l15 0 l-7.5 26 z" fill="#A5E0CE"/>
</svg>
<div class="escena">
  <svg class="tienda" viewBox="0 0 320 236"><use href="#tienda"/></svg>
  <svg class="globo" viewBox="0 0 80 120"><use href="#globo"/></svg>
  <img class="payaso" src="../personajes/payaso-azul.png" alt="">
  <div class="elenco">
    <img src="../personajes/perro.png" alt="">
    <img src="../personajes/cerdo.png" alt="">
    <img src="../personajes/oso.png" alt="">
    <img src="../personajes/gato.png" alt="">
    <img src="../personajes/conejo.png" alt="">
  </div>
</div>
<div class="texto">
  <div class="cinta"><span class="cinta-cola izq"></span><span class="cinta-cola der"></span>
    <div class="liston"><span class="nombre">__NOMBRE__</span><span class="familia">__FAMILIA__</span></div>
  </div>
  <p class="guion">cumple 1 año</p>
  <p class="fecha">__FECHA__<br>__HORA__</p>
  <p class="lugar">__LUGAR__</p>
</div>
</body></html>'''

def dato(patron, defecto=''):
    m = re.search(patron, s)
    return m.group(1) if m else defecto

nombre  = dato(r'<span class="nombre">(.*?)</span>')
familia = dato(r'<span class="familia">(.*?)</span>')
dia     = dato(r'<p class="dia-num">(.*?)</p>')
mes     = re.sub(r'\s*\d{4}$', '', dato(r'<p class="dia-palabras">(.*?)</p>'))
hora    = dato(r'<p class="hora">\s*<svg.*?</svg>\s*(.*?)\s*</p>', re.S)
lugar   = dato(r'<p class="lugar-nom">(.*?)</p>')
ciudad  = dato(r'<p class="lugar-dir">.*?<br>(.*?)</p>', re.S)
ciudad  = re.sub(r'^\d+\s*', '', ciudad).strip().replace('Durango, Dgo.', 'Durango').strip()

for k, v in [('__NOMBRE__', nombre), ('__FAMILIA__', familia), ('__FECHA__', f'sábado {dia} de {mes}'),
             ('__HORA__', hora), ('__LUGAR__', f'{lugar}, {ciudad}')]:
    og = og.replace(k, v)

(raiz / 'build' / 'og.html').write_text(og, encoding='utf-8')
print(f'build/og.html · {nombre} {familia} · {dia} de {mes}, {hora} · {lugar}, {ciudad}')
