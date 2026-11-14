#!/usr/bin/env python3
"""Agrega una ficha a inventario.json y regenera la vitrina.

Las fotos se copian tal cual (sin recorte, rotación ni recompresión).

Ejemplo:
  python3 add_item.py \\
    --titulo "Super Mario Bros." --tipo Juego --plataforma NES \\
    --marca Nintendo --anio 1985 --region NTSC --formato Cartucho \\
    --empaque "Solo cartucho" --estado Bueno --rareza Común \\
    --venta "$25.000 – $40.000" --fotos /ruta/foto1.jpg /ruta/foto2.jpg
"""
import argparse, json, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INV = ROOT / 'inventario.json'

TIPOS = ['Consola', 'Juego', 'Accesorio', 'Merch']

def next_id(items):
    nums = []
    for x in items:
        m = re.match(r'VJ-(\d+)$', str(x.get('id', '')))
        if m:
            nums.append(int(m.group(1)))
    return f"VJ-{(max(nums) if nums else 0)+1:03d}"

def main():
    p = argparse.ArgumentParser(description='Agrega una pieza al catálogo de videojuegos.')
    p.add_argument('--titulo', required=True)
    p.add_argument('--tipo', required=True, choices=TIPOS)
    p.add_argument('--plataforma', required=True)
    p.add_argument('--marca', default='')
    p.add_argument('--linea', default='')
    p.add_argument('--modelo', default='')
    p.add_argument('--anio', default='Sin confirmar')
    p.add_argument('--region', default='')
    p.add_argument('--formato', default='')
    p.add_argument('--empaque', default='')
    p.add_argument('--fabricacion', default='')
    p.add_argument('--serial', default='')
    p.add_argument('--estado', default='Sin confirmar', help='Escala: Excelente, Muy bueno, Bueno, Regular, Usado…')
    p.add_argument('--estado-nota', type=int, default=None, help='Nota 1-10, opcional')
    p.add_argument('--estado-detalle', default='')
    p.add_argument('--rareza', default='Sin confirmar')
    p.add_argument('--venta', default='Precio a convenir', help='Venta Chile CLP, ej. "$25.000 – $40.000"')
    p.add_argument('--usd', default='')
    p.add_argument('--clp-int', default='')
    p.add_argument('--stock', type=int, default=1)
    p.add_argument('--notas', default='')
    p.add_argument('--dolar', default='')
    p.add_argument('--id', default='')
    p.add_argument('--fotos', nargs='*', default=[], help='Rutas de fotos originales; se copian tal cual.')
    args = p.parse_args()

    items = json.loads(INV.read_text(encoding='utf-8')) if INV.exists() else []
    pid = args.id or next_id(items)
    if any(x.get('id') == pid for x in items):
        sys.exit(f'Ya existe el id {pid}')

    item = {
        'id': pid,
        'tipo': args.tipo,
        'titulo': args.titulo,
        'plataforma': args.plataforma,
        'marca': args.marca,
        'linea': args.linea,
        'modelo': args.modelo,
        'region': args.region,
        'formato': args.formato,
        'anio': args.anio,
        'empaque': args.empaque,
        'fabricacion': args.fabricacion,
        'serial': args.serial,
        'estado': {'escala': args.estado, **({'nota': args.estado_nota} if args.estado_nota is not None else {}), **({'detalle': args.estado_detalle} if args.estado_detalle else {})},
        'rareza': args.rareza,
        'valor_internacional_usd': args.usd,
        'valor_internacional_clp': args.clp_int,
        'venta_chile_clp': args.venta,
        'stock': args.stock,
        'notas': args.notas,
        'dolar': args.dolar,
        'fecha': date.today().isoformat(),
        'fotos': [str(Path(f).resolve()) for f in args.fotos],
    }
    # quitar vacíos excepto campos clave
    keep = {'id', 'tipo', 'titulo', 'plataforma', 'venta_chile_clp', 'stock', 'fecha', 'fotos', 'estado'}
    item = {k: v for k, v in item.items() if k in keep or v not in ('', None, [], {})}
    items.append(item)
    INV.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Agregado {pid}: {args.titulo}')
    # regenerar sitio
    sys.path.insert(0, str(ROOT))
    import runpy
    runpy.run_path(str(ROOT / 'gen_vitrina.py'), run_name='__main__')

if __name__ == '__main__':
    main()
