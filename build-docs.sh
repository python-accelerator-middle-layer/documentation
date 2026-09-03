#!/usr/bin/env bash

set -euo pipefail

rm -rf docs/source/tutorials docs/source/sg_execution_times.rst
rm -rf docs/build
rm -rf .jupyter_cache

mkdir -p docs/source/_static

sphinx-build -E -a -b html docs/source docs/build/html
