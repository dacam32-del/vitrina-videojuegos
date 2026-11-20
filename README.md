# 🎮 Videojuegos de Todos los Tiempos

Vitrina virtual de la colección de videojuegos de David: consolas, juegos, accesorios y merch de todas las épocas, desde Atari y NES hasta PlayStation, Xbox, Switch y portátiles.

Cada ficha puede incluir fotos (publicadas tal cual se suben, sin recortes ni retoques), tipo, plataforma, marca o fabricante, línea o serie, modelo, región, formato, año, empaque o completitud, estado, rareza y un precio estimado en pesos chilenos (CLP) según el estado, con referencia internacional en USD.

**Funciones de la vitrina:**
- Filtros por tipo (Consola, Juego, Accesorio, Merch), plataforma, marca, año, época, estado, rareza y rango de precio.
- Orden por defecto: de más caro a más barato.
- Calculadora/carrito flotante para ir sumando piezas, guardado en el navegador.
- Botón de consulta por WhatsApp (+56 9 5659 2453), también en cada ficha.
- Música de fondo: "Video Dungeon Boss" de Kevin MacLeod (incompetech.com), licencia CC BY 4.0.

**Totales:** 10 Fichas · 10 Unidades — $126.000 – $188.000 (CLP, venta Chile). Publicados: VJ-001 y VJ-015 a VJ-023 (VJ-002 a VJ-014 quedan reservados para un lote pendiente).

## 🛒 Vitrina web
**[https://dacam32-del.github.io/vitrina-videojuegos/](https://dacam32-del.github.io/vitrina-videojuegos/)**

## Cómo agregar una pieza

La fuente del catálogo es [`inventario.json`](inventario.json). No hay precios ni fichas de ejemplo: solo se publica lo que se agregue.

Campos de cada ficha:

| Campo | Descripción |
| --- | --- |
| `id` | Código automático `VJ-001`, `VJ-002`… (o el que indiques) |
| `tipo` | `Consola`, `Juego`, `Accesorio` o `Merch` |
| `titulo` | Nombre de la pieza |
| `plataforma` | NES, SNES, PlayStation, Xbox, Game Boy, PC, etc. |
| `marca` | Nintendo, Sony, Sega, Microsoft, editora del juego… |
| `linea` | Línea o serie (opcional) |
| `modelo` | Modelo de consola o accesorio (opcional) |
| `region` | NTSC, PAL, NTSC-J u otra (opcional) |
| `formato` | Cartucho, CD, DVD, Blu-ray, etc. (opcional) |
| `anio` | Año o período |
| `empaque` | Completitud: caja, manual, solo cartucho… |
| `fabricacion` | País o fabricante (opcional) |
| `serial` | Inscripciones o número de serie (opcional) |
| `estado` | Objeto `{ "escala": "Bueno", "nota": 7, "detalle": "…" }` |
| `rareza` | Común, Poco común, etc. |
| `venta_chile_clp` | Precio o rango en CLP, o `"Precio a convenir"` |
| `valor_internacional_usd` / `valor_internacional_clp` | Referencia internacional (opcional) |
| `stock` | Unidades (por defecto 1) |
| `notas` | Comentarios y fuentes de tasación |
| `dolar` | Tipo de cambio usado (opcional) |
| `fecha` | Fecha de registro (`YYYY-MM-DD`) |
| `fotos` | Rutas de las fotos originales; se copian tal cual a `img/` |

**Opción A — script de ayuda** (copia las fotos sin editarlas y regenera el sitio):

```bash
python3 add_item.py \
  --titulo "Super Mario Bros." --tipo Juego --plataforma NES \
  --marca Nintendo --anio 1985 --region NTSC --formato Cartucho \
  --empaque "Solo cartucho" --estado Bueno --rareza Común \
  --venta "$25.000 – $40.000" \
  --fotos /ruta/foto1.jpg /ruta/foto2.jpg
```

**Opción B — a mano:** agrega el objeto a `inventario.json` y ejecuta `python3 gen_vitrina.py`. Luego, en este computador, `./publicar.sh` sube los cambios a GitHub Pages.
