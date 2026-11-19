#!/usr/bin/env python3
"""Genera build/artifact.html desde index.html.

Variante para entornos donde las descargas de archivo están bloqueadas
(Artifact): el boton de calendario abre Google Calendar en vez de bajar el .ics.
"""
import re, pathlib
raiz = pathlib.Path(__file__).resolve().parent.parent
s = (raiz / 'index.html').read_text(encoding='utf-8')

style  = re.search(r'<style>.*?</style>', s, re.S).group(0)
script = re.search(r'<script>.*?</script>', s, re.S).group(0)
body   = s[s.index('</head>') + 7: s.index('<script>')]

body = body.replace('<button class="btn btn-ical" id="btnIcal" type="button">',
                    '<a class="btn btn-ical" id="btnIcal" target="_blank" rel="noopener">')
body = body.replace('</button>\n      <button class="btn btn-compartir"',
                    '</a>\n      <button class="btn btn-compartir"')

ics = re.search(r"\/\* ── agregar al calendario.*?aviso\('Listo, te lo agregamos al calendario 📅'\);\n\}\);", script, re.S).group(0)
cal = """/* ── agregar al calendario ────────────────────────────── */
(function(){
  const ini = new Date(EVENTO.fechaISO);
  const fin = new Date(ini.getTime() + 4 * 3600 * 1000);
  const fmt = d => d.toISOString().replace(/[-:]/g, '').replace(/\\.\\d{3}/, '');
  $('#btnIcal').href = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
    + '&text=' + encodeURIComponent(EVENTO.nombre + ' cumple 1 año')
    + '&dates=' + fmt(ini) + '/' + fmt(fin)
    + '&location=' + encodeURIComponent(EVENTO.direccion)
    + '&details=' + encodeURIComponent(EVENTO.mensajeWA);
})();"""
script = script.replace(ics, cal)

titulo = re.search(r'<title>(.*?)</title>', s, re.S).group(1)
nombre = re.search(r'<span class="nombre">(.*?)</span>', body).group(1)
out = f'<title>Cumpleaños de {nombre}</title>\n' + style + '\n' + body + '\n' + script + '\n'
(raiz / 'build' / 'artifact.html').write_text(out, encoding='utf-8')
print(f'build/artifact.html  ({len(out)//1024} KB)  ·  título: Cumpleaños de {nombre}')
