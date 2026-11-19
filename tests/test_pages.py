import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PagesPublishingTests(unittest.TestCase):
    def test_noetic_is_an_active_version(self):
        versions = json.loads((ROOT / "docs/versions.json").read_text(encoding="utf-8"))
        noetic = next(version for version in versions if version["path"] == "noetic")

        self.assertEqual(
            noetic,
            {
                "label": "ROS Noetic",
                "path": "noetic",
                "branch": "noetic-dev",
                "status": "active",
                "ubuntu": "20.04",
            },
        )
        noetic_index = versions.index(noetic)
        legacy_indexes = [
            index for index, version in enumerate(versions) if version["status"] == "legacy"
        ]
        self.assertTrue(legacy_indexes)
        self.assertLess(noetic_index, min(legacy_indexes))

    def test_built_landing_promotes_noetic(self):
        with tempfile.TemporaryDirectory() as output:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "sphinx",
                    "-W",
                    "-b",
                    "html",
                    str(ROOT / "docs"),
                    output,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            landing = (Path(output) / "index.html").read_text(encoding="utf-8")

        current_start = landing.index("<h2>当前 ROS 和 ROS2 文档")
        historical_start = landing.index("<h2>历史文档", current_start)
        current = landing[current_start:historical_start]
        historical = landing[historical_start:]

        self.assertIn("ROS Noetic", current)
        self.assertIn('href="noetic/"', current)
        self.assertNotIn("ROS Noetic", historical)
        self.assertIn("ROS2 Galactic", historical)
        self.assertIn("ROS Melodic", historical)

    def test_workflow_checks_out_and_tests_noetic(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")

        for required in (
            "noetic_ref:",
            "NOETIC_REF:",
            "ref: ${{ env.NOETIC_REF }}",
            "path: branches/noetic",
            "-r branches/noetic/docs/requirements.txt",
            "python -m unittest discover -s main/tests -v",
        ):
            with self.subTest(required=required):
                self.assertIn(required, workflow)

    def test_combined_builder_replaces_legacy_noetic(self):
        with tempfile.TemporaryDirectory() as temporary:
            temporary = Path(temporary)
            branches = temporary / "branches"
            legacy = temporary / "legacy"
            output = temporary / "site"

            for name in ("noetic", "humble", "jazzy", "lyrical"):
                scripts = branches / name / "scripts"
                scripts.mkdir(parents=True)
                build_script = scripts / "build-docs.sh"
                build_script.write_text(
                    "#!/usr/bin/env bash\n"
                    "set -euo pipefail\n"
                    "rm -rf site\n"
                    "mkdir -p site\n"
                    f"printf '%s\\n' 'new-{name}-docs' > site/index.html\n",
                    encoding="utf-8",
                )
                build_script.chmod(0o755)

            (legacy / "noetic").mkdir(parents=True)
            (legacy / "noetic/index.html").write_text(
                "old-noetic-directory", encoding="utf-8"
            )
            (legacy / "noetic/obsolete.html").write_text(
                "old-noetic-obsolete-page", encoding="utf-8"
            )
            (legacy / "Noetic.html").write_text("old-noetic-root", encoding="utf-8")
            (legacy / "Galactic.html").write_text(
                "preserved-galactic-archive", encoding="utf-8"
            )
            (legacy / "Melodic.html").write_text(
                "preserved-melodic-archive", encoding="utf-8"
            )

            completed = subprocess.run(
                [
                    "bash",
                    str(ROOT / "scripts/build-pages.sh"),
                    str(output),
                    str(branches),
                    str(legacy),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

            self.assertEqual(
                (output / "noetic/index.html").read_text(encoding="utf-8").strip(),
                "new-noetic-docs",
            )
            self.assertFalse((output / "noetic/obsolete.html").exists())
            noetic_redirect = (output / "Noetic.html").read_text(encoding="utf-8")
            self.assertIn('content="0; url=noetic/"', noetic_redirect)
            self.assertIn('href="noetic/"', noetic_redirect)
            self.assertNotIn("old-noetic", noetic_redirect)
            self.assertEqual(
                (output / "Galactic.html").read_text(encoding="utf-8"),
                "preserved-galactic-archive",
            )
            self.assertEqual(
                (output / "Melodic.html").read_text(encoding="utf-8"),
                "preserved-melodic-archive",
            )


if __name__ == "__main__":
    unittest.main()
