#!/bin/bash

set -euxo pipefail

write-requirements() {
  VERSION="$1"
  SCRATCH="$(mktemp -d --tmpdir "gen-reqs-$VERSION-XXXXXXXXX")"
  trap 'rm -r "$SCRATCH"' RETURN
  conda create -y -p "$SCRATCH/conda" "python=$VERSION"
  "$SCRATCH/conda/bin/python" -m venv "$SCRATCH/venv"
  "$SCRATCH/venv/bin/pip" install --upgrade pip wheel
  "$SCRATCH/venv/bin/pip" install .
  "$SCRATCH/venv/bin/pip" freeze --exclude tiledb-cloud >"requirements-py$VERSION.txt"
}

for VER in 3.6 3.7 3.9; do
  write-requirements "$VER"
done
