# Agent Guide

`main` is the landing-page and GitHub Pages orchestration branch. Runtime ROS
driver changes belong on the active distro branches, not directly here.

## Start Here

- Repository overview and public docs links: `README.md`
- Future/deferred work list: `TODO.md`
- Pages build script: `scripts/build-pages.sh`
- Active runtime branches: `noetic-dev`, `humble-dev`, `jazzy-dev`, `lyrical-dev`
- Legacy branches: `galactic-dev`, `melodic-dev`; do not modify
  unless explicitly requested.

## Development Rules

- Always make changes through pull requests.
- Use conventional commit messages, for example `docs: update agent guide`.
- Unless a request is explicitly branch-specific, apply concrete feature, fix,
  and process changes to all active runtime branches: `noetic-dev`,
  `humble-dev`, `jazzy-dev`, and `lyrical-dev`.
- Keep generated `site/` output and local planning scratch files out of git.

## Main Branch Verification

Run from the repository root:

```bash
bash scripts/build-pages.sh \
  /tmp/lebai-pages-site \
  /tmp/lebai-doc-branches \
  /tmp/lebai-legacy-pages
```

That command expects `/tmp/lebai-doc-branches` to contain `noetic`, `humble`,
`jazzy`, and `lyrical` checkouts with each branch's `scripts/build-docs.sh`,
and `/tmp/lebai-legacy-pages` to contain the existing `gh-pages` archive.
