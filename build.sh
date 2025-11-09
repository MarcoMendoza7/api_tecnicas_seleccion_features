#!/usr/bin/env bash
set -euo pipefail

# actualizar pip
python -m pip install --upgrade pip

# instalar dependencias forzando solo binarios
pip install --upgrade wheel
pip install -r requirements.txt
