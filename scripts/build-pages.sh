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

  touch "$SITE_DIR/.nojekyll"
}

build_landing_docs() {
  python3 -m sphinx \
    -W \
    -b html \
    "$ROOT/docs" \
    "$SITE_DIR"
}

write_legacy_redirect() {
  local path="$1"
  local target="$2"
  local title="$3"
  local dir="$SITE_DIR/$path"

  mkdir -p "$dir"
  cat > "$dir/index.html" <<EOF
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=../$target">
    <link rel="canonical" href="../$target">
    <title>$title</title>
  </head>
  <body>
    <p><a href="../$target">$title</a></p>
  </body>
</html>
EOF
}

write_legacy_redirects() {
  write_legacy_redirect noetic Noetic.html "ROS Noetic 历史文档"
  write_legacy_redirect galactic Galactic.html "ROS2 Galactic 历史文档"
  write_legacy_redirect melodic Melodic.html "ROS Melodic 历史文档"
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
build_landing_docs
write_legacy_redirects

build_branch_docs humble
build_branch_docs jazzy
build_branch_docs lyrical
