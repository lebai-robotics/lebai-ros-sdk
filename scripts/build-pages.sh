#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE_DIR="${1:-$ROOT/site}"
BRANCH_ROOT="${2:-$ROOT/.docs-branches}"
LEGACY_ROOT="${3:-}"

prepare_site_root() {
  rm -rf "$SITE_DIR"
  mkdir -p "$SITE_DIR"

  if [[ -n "$LEGACY_ROOT" && -d "$LEGACY_ROOT" ]]; then
    (
      shopt -s dotglob nullglob
      for item in "$LEGACY_ROOT"/*; do
        [[ "$(basename "$item")" == ".git" ]] && continue
        cp -a "$item" "$SITE_DIR/"
      done
    )
  fi

  cp "$ROOT/docs/index.html" "$SITE_DIR/index.html"
  cp "$ROOT/docs/versions.json" "$SITE_DIR/versions.json"
  touch "$SITE_DIR/.nojekyll"
}

build_branch_docs() {
  local name="$1"
  local branch_dir="$BRANCH_ROOT/$name"
  local output_dir="$SITE_DIR/$name"

  if [[ ! -f "$branch_dir/scripts/build-docs.sh" ]]; then
    echo "Missing docs build script: $branch_dir/scripts/build-docs.sh" >&2
    return 1
  fi

  (
    cd "$branch_dir"
    rm -rf site
    bash scripts/build-docs.sh
  )

  rm -rf "$output_dir"
  cp -a "$branch_dir/site" "$output_dir"
}

prepare_site_root

build_branch_docs humble
build_branch_docs jazzy
build_branch_docs lyrical
