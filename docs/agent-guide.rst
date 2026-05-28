Agent Guide
===========

The repository root contains ``AGENTS.md`` with the source-of-truth workflow
rules for AI agents and contributors.

Key points:

- Keep runtime code Python.
- Keep interface generation in ``lebai_interfaces``.
- Use released ``pylebai`` only.
- Do not commit ``docs/superpowers/``.
- Run focused unit tests and package builds before committing.
- Keep documentation source in ``docs/`` and generated HTML in ``site/``.

Useful commands:

.. code-block:: bash

   source /opt/ros/${ROS_DISTRO:-humble}/setup.bash
   colcon build --packages-select lebai_interfaces lebai_driver lebai_tutorials --symlink-install
   source install/setup.bash
   python3 -m pytest src/lebai-ros-sdk/lebai_driver/test -q -m "not integration and not linter"
   ./scripts/build-docs.sh
