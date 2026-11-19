"""Distribution boundaries checked only in a full source checkout."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills/reasoning-workflow"
MODULAR = REPO / "modular/skills"


class EditionTests(unittest.TestCase):
    def test_modular_contracts(self):
        research = MODULAR / "deep-research"
        retrieve = (research / "references/retrieval-and-observation.md").read_text()
        self.assertIn("concise, observable decision note", retrieve)
        self.assertNotIn("state internally why", retrieve)
        entry = (research / "SKILL.md").read_text().lower()
        method = (research / "references/research-modes-and-methods.md").read_text().lower()
        for text in (entry, method):
            self.assertTrue("engineering" in text or "architecture" in text)
            self.assertIn("real-world", text)
            self.assertTrue("both" in text or "hybrid" in text)
            self.assertIn("user", text)
        self.assertTrue("default model" in entry or "host-selected model" in entry)
        for term in ("explicit", "ultra"):
            self.assertIn(term, entry)
        execution = MODULAR / "execution-control/references"
        recovery = (execution / "synchronization-and-recovery.md").read_text().lower()
        for term in ("root objective", "cannot be found", "parked side branch",
                     "compare the saved workflow/policy identity"):
            self.assertIn(term, recovery)
        self.assertIn("## Root cancellation and late worker results",
                      (execution / "runtime-and-delegation.md").read_text())

    def test_distribution_metadata(self):
        version = json.loads((SKILL / "RELEASE.json").read_text())["version"]
        plugin = json.loads((REPO / ".codex-plugin/plugin.json").read_text())
        self.assertIn("调用我的 workflow skills", plugin["interface"]["defaultPrompt"])
        self.assertEqual(plugin["version"], version)
        bundle = REPO / "integrations/deepseek-harness"
        self.assertEqual(json.loads((bundle / "package.json").read_text())["version"], version)
        index = "routing-index.json"
        self.assertEqual((bundle / "skills/reasoning-workflow" / index).read_bytes(),
                         (SKILL / index).read_bytes())

    def test_harness_prepares_packaged_tasks(self):
        bundle = REPO / "integrations/deepseek-harness/skills/reasoning-workflow"
        for case in ("standard_profile.json", "ultra_delegated_profile.json"):
            profile = SKILL / "tests/fixtures" / case
            def prepare(root):
                out = subprocess.run([sys.executable, root / "scripts/prepare_task.py", profile],
                                     check=True, capture_output=True, text=True)
                return json.loads(out.stdout)
            actual = prepare(bundle)
            self.assertEqual(actual["status"], "prepared")
            self.assertEqual(actual["selected_references"], prepare(SKILL)["selected_references"])
