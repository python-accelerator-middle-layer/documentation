#!/usr/bin/env bash

set -euo pipefail

rm -rf docs/build .jupyter_cache
mkdir -p docs/source/_static

sphinx-build -E -a -b html docs/source docs/build/html
