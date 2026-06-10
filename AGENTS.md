# Agent Guide

The `main` branch is a landing and documentation publishing branch. Do not add
runtime ROS driver packages to this branch.

## Branch Roles

- `main`: project landing page and GitHub Pages orchestration.
- `humble-dev`: ROS2 Humble runtime code and docs.
- `jazzy-dev`: ROS2 Jazzy runtime code and docs.
- `lyrical-dev`: ROS2 Lyrical runtime code and docs.
- `noetic-dev`, `galactic-dev`, `melodic-dev`: legacy branches; do not modify
  unless explicitly requested.

## Documentation Publishing

The Pages workflow on `main` builds a Chinese Sphinx landing page with the Read
the Docs theme, checks out each active distro branch, copies that branch's
generated Sphinx output under its distro path, adds redirects for legacy clean
URLs, and publishes the final `site/` directory to the `gh-pages` branch:

```text
site/
  index.html
  humble/
  jazzy/
  lyrical/
```

Legacy documentation is preserved from the existing `gh-pages` archive when the
workflow can check it out.

## Verification

Run local checks from this branch root:

```bash
bash scripts/build-pages.sh /tmp/lebai-pages-site /tmp/lebai-doc-branches
```

For that command to work, `/tmp/lebai-doc-branches` must contain `humble`,
`jazzy`, and `lyrical` checkouts with each branch's `scripts/build-docs.sh`.
