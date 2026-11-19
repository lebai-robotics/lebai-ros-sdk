#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
python3 -m sphinx -W --keep-going -E -b html "$repo_dir/docs" "$repo_dir/docs/build/html"
