#!/usr/bin/env python3
"""Genera la vitrina Videojuegos de Todos los Tiempos.

Fuente: inventario.json (mismo directorio que este script, o /workspace/videojuegos).
Salida: /workspace/vitrina-videojuegos (sitio estatico para GitHub Pages).

Las fotos se copian tal cual, sin recorte, redimensionado, rotacion ni recompresion.
"""
import json, os, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path('/workspace/vitrina-videojuegos')
if (HERE / '.git').exists() or HERE.name == 'vitrina-videojuegos':
    OUT = HERE
INV = HERE / 'inventario.json'
if not INV.exists():
    alt = Path('/workspace/videojuegos/inventario.json')
    if alt.exists():
        INV = alt

os.makedirs(OUT / 'img', exist_ok=True)

def rng(s):
    n = [int(x.replace('.', '')) for x in re.findall(r'\d[\d.]*', str(s or '')) if x.replace('.', '').isdigit()]
    return (min(n), max(n)) if n else (None, None)

def fmt(n):
    return f"{n:,}".replace(',', '.')

def year(p):
    y = re.findall(r'\b(19[5-9]\d|20[0-3]\d)\b', str(p.get('anio', '')))
    return int(y[0]) if y else 0

def epoca(y):
    if not y:
        return 'Sin confirmar'
    if y < 1980:
        return 'Antes de 1980'
    if y < 1990:
        return 'Años 80'
    if y < 2000:
        return 'Años 90'
    if y < 2010:
        return 'Años 2000'
    if y < 2020:
        return 'Años 2010'
    return '2020 en adelante'

def copy_as_is(src, dst):
    src, dst = Path(src), Path(dst)
    if dst.exists() and src.resolve() == dst.resolve():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

inv = json.loads(INV.read_text(encoding='utf-8')) if INV.exists() else []
items = []
tmin = tmax = uds = 0
priced = False
for p in inv:
    imgs = []
    for i, f in enumerate(p.get('fotos', []) or p.get('imgs', [])):
        src = Path(f)
        if not src.is_absolute():
            for base in (INV.parent, OUT, Path('/workspace/videojuegos')):
                cand = base / f
                if cand.exists():
                    src = cand
                    break
        if not src.exists():
            published = OUT / f if str(f).startswith('img/') else OUT / 'img' / Path(f).name
            if published.exists():
                imgs.append(str(published.relative_to(OUT)))
            continue
        suffix = src.suffix.lower() or '.jpg'
        name = f"{p['id']}{suffix}" if i == 0 else f"{p['id']}-{i+1}{suffix}"
        dst = OUT / 'img' / name
        copy_as_is(src, dst)
        imgs.append('img/' + name)
    a, b = rng(p.get('venta_chile_clp'))
    k = int(p.get('stock', 1) or 1)
    if a is not None:
        tmin += a * k
        tmax += (b if b is not None else a) * k
        priced = True
    uds += k
    y = year(p)
    q = {kk: v for kk, v in p.items() if kk not in ('fotos',)}
    if a is None:
        q.setdefault('venta_chile_clp', q.get('venta_chile_clp') or 'Precio a convenir')
    q.update(imgs=imgs, pmin=a, pmax=b, y=y, ep=p.get('epoca') or p.get('ep') or epoca(y))
    items.append(q)

total = f"${fmt(tmin)} – ${fmt(tmax)}" if priced else '—'
data = json.dumps(items, ensure_ascii=False).replace('</', '<\\/')
WA = "https://wa.me/56956592453?text=Hola!%20Vi%20tu%20vitrina%20de%20videojuegos%20y%20quiero%20consultar"

PLATAFORMAS = [
    'Atari', 'NES', 'SNES', 'Nintendo 64', 'GameCube', 'Wii', 'Wii U', 'Nintendo Switch',
    'PlayStation', 'PlayStation 2', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5',
    'Xbox', 'Xbox 360', 'Xbox One', 'Xbox Series',
    'Sega Master System', 'Sega Mega Drive / Genesis', 'Sega Saturn', 'Sega Dreamcast',
    'PC', 'Game Boy', 'Game Boy Color', 'Game Boy Advance', 'Nintendo DS', 'Nintendo 3DS',
    'PSP', 'PS Vita', 'Otras',
]
TIPOS = ['Consola', 'Juego', 'Accesorio', 'Merch']
plats = json.dumps(PLATAFORMAS, ensure_ascii=False)
tipos = json.dumps(TIPOS, ensure_ascii=False)

H = r"""<!DOCTYPE html><html lang="es-CL"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Videojuegos de Todos los Tiempos · Consolas, Juegos y Accesorios</title>
<meta name="description" content="Vitrina virtual de videojuegos de todos los tiempos: consolas, juegos, accesorios y merch. Tasacion en Chile (CLP) segun estado.">
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Nunito:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
:root{--bg:#0b1020;--paper:#161b2e;--ink:#e8ecff;--bur:#ff3d7f;--grn:#39ff88;--gold:#ffd23f;--mut:#8b93b8}
*{box-sizing:border-box}body{margin:0;background:var(--bg) radial-gradient(#1c2750 1.6px,transparent 1.6px) 0 0/22px 22px;color:var(--ink);font-family:Nunito,sans-serif}
header{background:linear-gradient(135deg,#141a3a,#3b0a5c 50%,#0a3d4d);color:#fff;padding:38px 20px 26px;text-align:center;border-bottom:6px dashed var(--grn)}
h1{font-family:Fredoka,sans-serif;font-size:2.4em;margin:0;letter-spacing:.5px;text-shadow:0 0 18px rgba(57,255,136,.35)}header p{margin:6px 0 0;font-style:italic;color:#c8ffd9}
.wa{display:inline-flex;gap:6px;align-items:center;margin-top:14px;background:#25d366;color:#fff;text-decoration:none;padding:8px 16px;border-radius:22px;font-family:Fredoka;font-weight:600}
.stats{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:20px}.stat{border:1px solid var(--gold);padding:10px 18px;border-radius:4px;background:rgba(255,255,255,.06)}
.stat b{display:block;font-family:Fredoka;font-size:1.4em;color:#fff}.stat span{font-size:.8em;text-transform:uppercase;letter-spacing:1px}
.filters{max-width:1200px;margin:20px auto;padding:16px;background:var(--paper);border:3px solid #2a3a6a;border-radius:6px;display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}
.filters label{font-size:.75em;text-transform:uppercase;letter-spacing:1px;color:var(--grn);font-weight:600}
select,input{width:100%;padding:7px;border:2px solid #2a3a6a;background:#0e1428;font-family:Nunito;border-radius:3px;color:var(--ink)}
#count{max-width:1200px;margin:0 auto;padding:0 16px;color:var(--mut);font-style:italic}
.grid{max-width:1200px;margin:10px auto 40px;padding:0 16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:22px}
.card{background:var(--paper);border-radius:18px;box-shadow:6px 6px 0 #39ff88;border:3px solid var(--ink);cursor:pointer;overflow:hidden;transition:transform .15s}
.card:hover{transform:translateY(-4px) rotate(-.4deg)}.card img{width:100%;aspect-ratio:1/1;object-fit:contain;background:#0e1428;display:block}
.noimg{aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;background:#10203a;color:var(--grn);font-family:Fredoka;font-size:3em}
.cb{padding:12px}.cb .t{font-family:Fredoka;font-weight:800;font-size:1.05em;line-height:1.2}.cb .a{color:var(--mut);font-size:.85em;font-style:italic;margin:3px 0 8px}
.tag{display:inline-block;font-size:.7em;padding:2px 7px;border-radius:10px;background:var(--grn);color:#0b1020;margin:0 3px 3px 0}.tag.r{background:var(--gold);color:#0b1020}.tag.p{background:#3b7dff;color:#fff}
.price{margin-top:8px;color:var(--bur);font-weight:600}.empty{grid-column:1/-1;text-align:center;padding:70px 20px;font-family:Fredoka;font-size:1.6em;color:var(--grn)}
.modal{position:fixed;inset:0;background:rgba(8,10,24,.82);display:none;align-items:center;justify-content:center;padding:16px;z-index:9}.modal.on{display:flex}
.box{background:var(--paper);max-width:900px;width:100%;max-height:92vh;overflow:auto;border-radius:6px;border-top:8px solid var(--bur);padding:22px;position:relative}
.box h2{font-family:Fredoka;margin:0 0 4px;color:var(--bur)}.x{position:absolute;right:14px;top:8px;font-size:1.8em;cursor:pointer;color:var(--grn)}
.ph{display:flex;gap:8px;overflow-x:auto;margin:12px 0}.ph img{height:280px;border-radius:4px;border:3px solid #2a3a6a;background:#0e1428}
table{width:100%;border-collapse:collapse;font-size:.92em}td{padding:6px;border-bottom:1px dashed #2a3a6a;vertical-align:top}td:first-child{color:var(--grn);font-weight:600;width:38%}
footer{text-align:center;padding:20px;color:var(--mut);font-size:.85em;border-top:1px solid #2a3a6a}
</style></head><body>
<header><h1>🎮 Videojuegos de Todos los Tiempos</h1><p>Consolas, juegos, accesorios y merch de todas las épocas · tasación según estado en Chile</p>
<a class="wa" href="__WA__" target="_blank" rel="noopener">💬 Consultar por WhatsApp</a>
<div class="stats"><div class="stat"><b>__N__</b><span>Fichas</span></div><div class="stat"><b>__U__</b><span>Unidades</span></div><div class="stat"><b>__T__</b><span>Valor total Chile (CLP)</span></div></div></header>
<div class="filters">
<div><label>Buscar</label><input id="q" placeholder="Título, plataforma, marca…"></div>
<div><label>Tipo</label><select id="f_tipo"></select></div>
<div><label>Plataforma</label><select id="f_plat"></select></div>
<div><label>Marca / fabricante</label><select id="f_marca"></select></div>
<div><label>Año</label><select id="f_anio"></select></div>
<div><label>Época</label><select id="f_ep"></select></div>
<div><label>Estado</label><select id="f_estado"></select></div>
<div><label>Rareza</label><select id="f_rareza"></select></div>
<div><label>Precio mín. (CLP)</label><input id="pmin" type="number" min="0"></div>
<div><label>Precio máx. (CLP)</label><input id="pmax" type="number" min="0"></div>
<div><label>Ordenar</label><select id="ord"><option value="d">Más caros primero</option><option value="a">Más baratos primero</option><option value="yo">Más antiguos</option><option value="yn">Más recientes</option><option value="t">Nombre A–Z</option></select></div>
</div><div id="count"></div><div class="grid" id="g"></div>
<div class="modal" id="m"><div class="box" id="mb"></div></div>
<footer>Valores referenciales: internacional (eBay, PriceCharting, Mercado Libre) · Chile (MercadoLibre, coleccionistas). Precio según estado · dólar según cada ficha. Las fotos se publican tal cual se suben, sin recortes ni retoques.</footer>
<script>
const D=__DATA__,WA="__WA__",TIPOS=__TIPOS__,PLATS=__PLATS__;
const $=i=>document.getElementById(i);const e=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const est=p=>{const s=p.estado;return typeof s==='object'&&s?(s.escala||''):String(s||'').split(/[(·,-]/)[0].trim()};
const F={f_tipo:p=>p.tipo,f_plat:p=>p.plataforma,f_marca:p=>p.marca,f_anio:p=>p.y?String(p.y):'',f_ep:p=>p.ep,f_estado:est,f_rareza:p=>p.rareza};
const PRE={f_tipo:TIPOS,f_plat:PLATS};
for(const[id,fn]of Object.entries(F)){const fromD=[...new Set(D.map(fn).filter(Boolean))];const v=[...new Set([...(PRE[id]||[]),...fromD])].sort((a,b)=>String(a).localeCompare(String(b),'es'));$(id).innerHTML='<option value="">Todos</option>'+v.map(x=>`<option>${e(x)}</option>`).join('');$(id).onchange=r}
['q','pmin','pmax','ord'].forEach(i=>$(i).oninput=r);
const estTxt=p=>{const s=p.estado;return typeof s==='object'&&s?`${s.escala||''}${s.nota?' · '+s.nota+'/10':''}${s.detalle?' — '+s.detalle:''}`:(s||'')};
const precio=p=>p.venta_chile_clp||'Precio a convenir';
const inPrice=(p,a,b)=>{if(p.pmin==null||p.pmax==null)return !a&&b>=1e15;return p.pmax>=a&&p.pmin<=b};
function r(){const q=$('q').value.toLowerCase(),a=+$('pmin').value||0,b=+$('pmax').value||1e15;
let L=D.filter(p=>Object.entries(F).every(([id,fn])=>!$(id).value||fn(p)==$(id).value)&&inPrice(p,a,b)&&(!q||JSON.stringify(p).toLowerCase().includes(q)));
const o=$('ord').value;L.sort((x,y)=>{const xn=x.pmin==null?1:0,yn=y.pmin==null?1:0;if(xn!==yn)return xn-yn;return o=='a'?(x.pmin||0)-(y.pmin||0):o=='yo'?(x.y||9999)-(y.y||9999):o=='yn'?(y.y||0)-(x.y||0):o=='t'?String(x.titulo).localeCompare(y.titulo,'es'):(y.pmax||0)-(x.pmax||0)||(y.pmin||0)-(x.pmin||0)});
$('count').textContent=D.length?`${L.length} de ${D.length} piezas`:'Catálogo listo · todavía no hay fichas publicadas';
$('g').innerHTML=!D.length?'<div class="empty">🎮 Pronto nuevos videojuegos, consolas y accesorios</div>':!L.length?'<div class="empty">Sin resultados para estos filtros</div>':L.map(p=>`<div class="card" data-id="${e(p.id)}" onclick="sh('${p.id}')">${(p.imgs&&p.imgs.length)?`<img loading="lazy" src="${p.imgs[0]}" alt="">`:`<div class="noimg">🎮</div>`}<div class="cb"><div class="t">${e(p.titulo)}</div><div class="a">${e(p.plataforma||p.marca||'')}${p.anio?' · '+e(p.anio):''}</div>${p.tipo?`<span class="tag">${e(p.tipo)}</span>`:''}${p.plataforma?`<span class="tag p">${e(p.plataforma)}</span>`:''}${est(p)?`<span class="tag">${e(est(p))}</span>`:''}${p.rareza?`<span class="tag r">${e(p.rareza)}</span>`:''}<div class="price">${e(precio(p))}${/a convenir/i.test(precio(p))?'':' CLP'}</div></div></div>`).join('')}
const LB={id:'Código',tipo:'Tipo',titulo:'Nombre',plataforma:'Plataforma',marca:'Marca / fabricante',linea:'Línea / serie',modelo:'Modelo',region:'Región',formato:'Formato',anio:'Año',epoca:'Época',empaque:'Empaque / completitud',fabricacion:'Fabricación',serial:'Serie / inscripciones',estado:'Estado',rareza:'Rareza',valor_internacional_usd:'Valor internacional (USD)',valor_internacional_clp:'Valor internacional (CLP)',venta_chile_clp:'Venta sugerida en Chile (CLP)',stock:'Unidades',notas:'Notas',dolar:'Dólar usado',fecha:'Fecha de registro'};
function sh(id){const p=D.find(x=>x.id==id);$('mb').innerHTML=`<span class="x" onclick="$('m').classList.remove('on')">×</span><h2>${e(p.titulo)}</h2><i>${e([p.tipo,p.plataforma,p.marca].filter(Boolean).join(' · '))}${p.anio?' · '+e(p.anio):''}</i><div class="ph">${(p.imgs||[]).map(i=>`<a href="${i}" target="_blank"><img src="${i}" alt=""></a>`).join('')}</div><table>${Object.entries(LB).filter(([k])=>p[k]!=null&&p[k]!=='').map(([k,l])=>`<tr><td>${l}</td><td>${e(k=='estado'?estTxt(p):p[k])}</td></tr>`).join('')}</table><p><a class="wa" href="${WA}%20por%20${encodeURIComponent(p.id+' '+p.titulo)}" target="_blank" rel="noopener">💬 Consultar por esta pieza</a></p>`;$('m').classList.add('on')}
$('m').onclick=ev=>{if(ev.target.id=='m')$('m').classList.remove('on')};document.onkeydown=ev=>{if(ev.key=='Escape')$('m').classList.remove('on')};r();
</script></body></html>"""

H = (H.replace('__N__', str(len(items)))
      .replace('__U__', str(uds))
      .replace('__T__', total)
      .replace('__DATA__', data)
      .replace('__WA__', WA)
      .replace('__TIPOS__', tipos)
      .replace('__PLATS__', plats))

sys.path.insert(0, '/workspace/musica')
from musica_vitrina import inject as _mus
H = _mus(H, str(OUT), 'videojuegos', 'Video Dungeon Boss', '#141a3a', '#39ff88')
sys.path.insert(0, '/workspace/calculadora')
from calculadora_vitrina import inject as _calc
H = _calc(H, 'videojuegos')

(OUT / 'index.html').write_text(H, encoding='utf-8')
(OUT / '.nojekyll').write_text('')
print(f"OK: {len(items)} FICHAS, {uds} unidades, total {total} -> {OUT}")
