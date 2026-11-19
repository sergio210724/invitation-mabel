#!/usr/bin/env python3
"""Recorta los personajes del pin de Pinterest y los mete en la invitación.

Cada personaje se separa de la imagen, se le quita el fondo blanco (solo el que
tocael borde, para no comerse los blancos de dentro) y se guarda en personajes/.
Luego se incrustan en index.html como data URI para que siga siendo un archivo
suelto.
"""
import base64, pathlib, re
import numpy as np
from PIL import Image
from collections import deque

raiz = pathlib.Path(__file__).resolve().parent.parent
ORIGEN = raiz / 'build' / 'pin-plimplim.jpg'
DESTINO = raiz / 'personajes'

# cajas (x1,y1,x2,y2) sobre la imagen de 675x1200
REGIONES = {
    'perro':       (0,   0, 335, 455),
    'payaso-azul': (330, 0, 675, 475),
    'cerdo':       (0, 460, 325, 875),
    'gato':        (330,470, 675, 875),
    'conejo':      (0, 860, 325, 1200),
    'oso':         (330,845, 675, 1200),
}
ORDEN = ['perro', 'payaso-azul', 'cerdo', 'gato', 'conejo', 'oso']

imagen = Image.open(ORIGEN).convert('RGBA')
arr = np.array(imagen)
DESTINO.mkdir(exist_ok=True)

def quitar_fondo_connected(a):
    """Pone transparentes solo los pixeles blancos conectados con el borde."""
    h, w = a.shape[:2]
    rgb = a[:, :, :3].astype(int)
    casi_blanco = (rgb.min(axis=2) > 232)
    alpha = a[:, :, 3].copy()
    libre = casi_blanco.copy()
    cola = deque()
    for x in range(w):
        for y in (0, h - 1):
            if libre[y, x]:
                cola.append((y, x)); libre[y, x] = False
    for y in range(h):
        for x in (0, w - 1):
            if libre[y, x]:
                cola.append((y, x)); libre[y, x] = False
    while cola:
        y, x = cola.popleft()
        alpha[y, x] = 0
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and libre[ny, nx]:
                libre[ny, nx] = False
                cola.append((ny, nx))
    return alpha

def mayor_componente(a):
    """Deja solo el personaje: descarta los pedazos sueltos de los vecinos."""
    mascara = a[:, :, 3] > 8
    h, w = mascara.shape
    vistos = np.zeros_like(mascara, dtype=bool)
    componentes = []
    for y in range(h):
        for x in range(w):
            if not mascara[y, x] or vistos[y, x]:
                continue
            pila = [(y, x)]
            vistos[y, x] = True
            pix = []
            while pila:
                cy, cx = pila.pop()
                pix.append((cy, cx))
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx = cy+dy, cx+dx
                    if 0 <= ny < h and 0 <= nx < w and mascara[ny, nx] and not vistos[ny, nx]:
                        vistos[ny, nx] = True
                        pila.append((ny, nx))
            componentes.append(pix)
    if not componentes:
        return a
    componentes.sort(key=len, reverse=True)
    mayor = len(componentes[0])
    conservar = {id(p) for c in componentes if len(c) >= mayor * 0.18 for p in c}
    salida = a.copy()
    for c in componentes:
        if len(c) < mayor * 0.18:
            for (cy, cx) in c:
                salida[cy, cx, 3] = 0
    return salida


def recortar_a_contenido(img, margen=4):
    a = np.array(img)
    ys, xs = np.where(a[:, :, 3] > 8)
    if len(xs) == 0:
        return img
    x1, x2 = max(0, xs.min()-margen), min(a.shape[1], xs.max()+margen+1)
    y1, y2 = max(0, ys.min()-margen), min(a.shape[0], ys.max()+margen+1)
    return img.crop((x1, y1, x2, y2))

data_uris = {}
for nombre, caja in REGIONES.items():
    trozo = imagen.crop(caja)
    a = np.array(trozo)
    a[:, :, 3] = quitar_fondo_connected(a)
    a = mayor_componente(a)
    limpio = recortar_a_contenido(Image.fromarray(a, 'RGBA'))
    # son ilustraciones planas: con 64 colores el PNG baja muchisimo de peso
    limpio = limpio.quantize(colors=64, method=Image.FASTOCTREE)
    limpio.save(DESTINO / f'{nombre}.png', optimize=True)
    b64 = base64.b64encode(limpio.tobytes()).decode()  # placeholder, se rehace abajo
    png = DESTINO / f'{nombre}.png'
    data_uris[nombre] = 'data:image/png;base64,' + base64.b64encode(png.read_bytes()).decode()
    print(f'{nombre:12} {limpio.size[0]}x{limpio.size[1]}  {png.stat().st_size//1024} KB')

# ── incrustar en index.html ──
p = raiz / 'index.html'
s = p.read_text(encoding='utf-8')
bloque = 'const CAST = {\n' + ''.join(f"  '{k}': '{data_uris[k]}'" + (',\n' if k != ORDEN[-1] else '\n') for k in ORDEN) + '};\n'
s = re.sub(r'const CAST = \{.*?\n\};\n', bloque, s, flags=re.S)
if 'const CAST = {' not in s:
    s = s.replace('const CANCION_MP3', bloque + 'const CANCION_MP3')
p.write_text(s, encoding='utf-8')
print(f'\nCAST incrustado en index.html ({len(bloque)//1024} KB)')
