#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 -m sphinx \
  -W \
  -b html \
  "$ROOT/docs" \
  "$ROOT/site"
