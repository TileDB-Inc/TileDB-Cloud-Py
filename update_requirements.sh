#!/bin/bash

set -euxo pipefail

write-requirements() {
  VERSION="$1"
  SCRATCH="$(mktemp -d --tmpdir "gen-reqs-$VERSION-XXXXXXXXX")"
  trap 'rm -r "$SCRATCH"' RETURN
  conda create -y -p "$SCRATCH/conda" "python=$VERSION"
  "$SCRATCH/conda/bin/python" -m venv "$SCRATCH/venv"
  "$SCRATCH/venv/bin/pip" install --upgrade pip wheel
  # xarray is a test-only direct dependency for us.
  # It is normally just a transitive optional dependency of Pandas.
  "$SCRATCH/venv/bin/pip" install . xarray
  "$SCRATCH/venv/bin/pip" freeze --exclude tiledb-cloud >"requirements-py$VERSION.txt"
}

for VER in 3.7 3.9; do
  write-requirements "$VER"
done
