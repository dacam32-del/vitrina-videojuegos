#!/bin/bash
set -e
python3 /workspace/videojuegos/gen_vitrina.py
cd /workspace/vitrina-videojuegos
git add -A
git diff --cached --quiet && { echo "Sin cambios"; echo "Publicado: https://dacam32-del.github.io/vitrina-videojuegos/"; exit 0; }
git commit -m "${1:-Actualiza vitrina de videojuegos $(date +%F)}"
git push origin main
echo "Publicado: https://dacam32-del.github.io/vitrina-videojuegos/"
