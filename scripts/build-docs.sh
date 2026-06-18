#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

rm -rf "$ROOT/site"

python3 -m sphinx \
  -W \
  -b html \
  "$ROOT/docs" \
  "$ROOT/site"
