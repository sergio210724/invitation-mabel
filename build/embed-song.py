#!/usr/bin/env python3
"""Mete cancion.mp3 dentro del index.html como data URI.

Así la invitación sigue siendo UN solo archivo que se manda por WhatsApp
(con el mp3 aparte, el botón de música se quedaria sin canción).
"""
import base64, pathlib, re
raiz = pathlib.Path(__file__).resolve().parent.parent
mp3 = (raiz / 'cancion.mp3').read_bytes()
b64 = base64.b64encode(mp3).decode()
p = raiz / 'index.html'
s = p.read_text(encoding='utf-8')

bloque = f'const CANCION_MP3 = "data:audio/mpeg;base64,{b64}";\n'
s = re.sub(r'const CANCION_MP3 = "data:audio/mpeg;base64,[^"]*";\n', '', s)
s = s.replace('/* ══════════════════════════════════════════════════════════════════════\n   EDITA AQUÍ los datos de la fiesta',
              bloque + '\n/* ══════════════════════════════════════════════════════════════════════\n   EDITA AQUÍ los datos de la fiesta')
s = re.sub(r"cancion    : '[^']*'", 'cancion    : CANCION_MP3', s)
p.write_text(s, encoding='utf-8')
print(f'cancion.mp3 embebida: {len(mp3)//1024} KB -> {len(b64)//1024} KB de base64')
print(f'index.html: {len(s)//1024} KB')
