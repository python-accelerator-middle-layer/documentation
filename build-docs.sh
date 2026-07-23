#!/usr/bin/env bash

set -euo pipefail

rm -rf docs/build .jupyter_cache
mkdir -p docs/source/_static

python - <<'PY'
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

tutorials_dir = Path("docs/source/tutorials")
archive = Path("docs/source/_static/tutorials.zip")

with ZipFile(archive, "w", compression=ZIP_DEFLATED) as zf:
    for path in tutorials_dir.rglob("*.ipynb"):
        zf.write(path, path.relative_to(tutorials_dir.parent))
PY

sphinx-build -E -a -b html docs/source docs/build/html

sphinx-build -E -a -b html docs/source docs/build/html
