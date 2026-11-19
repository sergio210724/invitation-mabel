# Invitación virtual · primer añito

Invitación que es una **mini web** (no un PDF ni una historia de Instagram): se abre
en el celu, tiene cuenta regresiva en vivo, mapa, canción y confirmación por WhatsApp.
Modelada en el TikTok de `@invitella.mx`.

**Cero servicios externos en tiempo de ejecución**: las tres tipografías van embebidas
(base64) dentro del archivo, el mapa está dibujado en SVG, el calendario se genera como
`.ics` en el navegador y la canción se sintetiza con WebAudio. Lo único que abre algo
externo son dos enlaces que **el invitado toca**: Google Maps y WhatsApp.

```
invitacion-virtual/
├── index.html        ← la invitación completa (autocontenida, 1.4 MB con la canción)
├── cancion.mp3       ← "Hoy es tu cumpleaños" (también va embebida dentro del HTML)
├── og.png            ← imagen de vista previa para WhatsApp (1200×630)
└── build/
    ├── fonts.css       ← las 3 tipografías en base64 (origen del bloque <style>)
    ├── make-og.py      ← regenera build/og.html desde index.html
    ├── make-artifact.py← regenera build/artifact.html desde index.html
    ├── embed-song.py   ← vuelve a meter cancion.mp3 dentro de index.html
    └── artifact.html   ← misma página para entornos donde no hay descargas de archivo
```

Los tres scripts de `build/` leen los datos de `index.html`, así que el cartel, la
variante de Artifact y la canción nunca se quedan desincronizados con la invitación.

## Cómo editar los datos de la fiesta

Todo lo editable está en dos lugares.

**1. El bloque `EVENTO`** (al final del archivo, dentro del `<script>`):

```js
const EVENTO = {
  fechaISO   : '2026-11-28T16:00:00-06:00',   // <- con el desfase de tu zona horaria
  nombre     : 'Fátima Mabel',
  apellido   : 'Fernández Nevárez',
  archivoIcs : 'cumple-fatima-mabel.ics',
  whatsapp   : '526183637291',                // <- con clave de país, sin +
  mensajeWA  : '¡Hola! Confirmo mi asistencia al cumpleaños de Fátima Mabel...',
  direccion  : 'Adrián Mora 210, Industrial Ladrillera, 34289 Durango, Dgo.',
  mapsQuery  : 'https://share.google/g4rNXpoqAsnLWQb6n',
  cancion    : ''                              // 'cancion.mp3' si quieres una real
};
```

El número de WhatsApp va con clave de país y sin `+` ni espacios: `52` (México) +
10 dígitos.

**2. Los textos visibles** en el HTML: el nombre va dentro del `.liston`, la frase en
`.frase`, el día en `.dia-num`, el mes en `.dia-palabras` y la hora en `.hora`.

> La fecha usa desfase `-06:00` (Durango es UTC-6). Si la fiesta es en otra zona,
> cámbialo (`-07:0` para Ciudad de México en horario estándar, `-05:00` para
> Monterrey). El contador y el `.ics` se calculan solos a partir de ahí.

## El elenco

Los personajes son **dibujos propios** de circo (payaso azul de pelo rizado, perro con
lentes, cerdo, gato, conejo y oso). No son los personajes oficiales de Plim Plim:
copiar su arte con licencia es un problema para quien comparte la invitación, así que
el diseño dibuja su propio elenco con el mismo spirits y la misma paleta.

El **payaso azul** es el protagonista grande, junto a la carpa; los otros cinco van en
fila abajo. Cuando llega la foto de Mabel, ella toma el lugar del payaso en el hero y
el payaso baja a presentar al elenco.

Si tienes los personajes oficiales (los toppers decake, por ejemplo) y quieres usarlos,
guárdalos en una carpeta `personajes/` junto al HTML con estos nombres:
`payaso-azul.png`, `perro.png`, `cerdo.png`, `gato.png`, `conejo.png`, `oso.png`.

## Poner la foto de la festejada

Por defecto la protagonista es el payaso. Para ponerle la foto real:

1. Guarda la foto como `foto.jpg` junto al `index.html`.
2. Listo: el código la detecta y **sustituye al payaso** en el hero (si el archivo no
   está, se queda el payaso). Si quieres ajustarle el tamaño, edita `.foto-hero`.

Para compartir **un solo archivo** por WhatsApp, conviértela a base64 y ponla como
`data:` URI (queda el HTML más pesado, pero viaja en un solo mensaje).

## La canción

Ya va la de la fiesta: **"Hoy es tu cumpleaños (Arafa)"**, de 40 segundos, metida dentro
del HTML como `data:` URI (base64). Así el archivo se manda solo por WhatsApp y el
botón ♪ siempre suena, sin necesitar internet ni un mp3 al lado.

Para cambiar la canción:

```bash
cp /ruta/de/tu/cancion.mp3 cancion.mp3
python3 build/embed-song.py
```

Si el mp3 no se encuentra, el botón cae solo en la melodía sintetizada de WebAudio
(una lullaby original, sin copyrights) que ya venía de fábrica.

## Cómo se comparte

**Opción A — un archivo (lo más simple).** Manda `index.html` por WhatsApp como
documento. Quien lo abre lo ve en el celu; no necesita internet ni instalar nada.
El botón de compartir recuerda que hay que mandarlo por WhatsApp.

**Opción B — una URL (para que se vea en la vista previa de WhatsApp).** Sube la
carpeta a Vercel:

```bash
cd ~/Workspace/invitacion-virtual
vercel deploy --prod
```

Sale la URL de producción: `https://cumple-mabel.vercel.app`. La vista previa con la foto
(`og.png`) solo aparece con URL; como archivo, WhatsApp muestra un rectángulo vacío.

## Detalles técnicos

- **Tipografías**: Alfa Slab One (display), Sacramento (manuscrita) y Nunito (texto),
  subconjuntadas a latino y embebidas en base64. Sin Google Fonts ni ningún CDN.
- **Cuenta regresiva**: se recalcula cada segundo con `setInterval`; cuando pasa la
  fecha, el texto cambia a «¡Hoy es el gran día!».
- **Calendario**: se arma un `.ics` con `Blob` + `URL.createObjectURL` y se descarga.
  Incluye un aviso 2 horas antes. En `build/artifact.html` (donde las descargas están
  bloqueadas) el botón abre Google Calendar en su lugar.
- **Mapa**: es un SVG esquemático, no un embed de Maps. El botón «Ver en Maps» abre el
  enlace que compartiste del lugar (`EVENTO.mapsQuery`).
- **Cartel de WhatsApp** (`og.png`): se regenera con `python3 build/make-og.py` y luego
  `Chrome --headless --screenshot=og.png build/og.html`. El script lee los datos del
  `index.html`, así que no se desincroniza.
- **Accesibilidad**: respeta `prefers-reduced-motion` (sin confeti ni transiciones),
  foco visible, `aria-label` en los botones y roles correctos en el contador.
- **Texto**: `lang="es-MX"`, con acentos y `ñ` correctos en las tipografías embebidas.
