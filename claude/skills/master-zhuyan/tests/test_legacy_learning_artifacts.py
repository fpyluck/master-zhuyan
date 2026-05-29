import json
import re
import contextlib
import importlib.util
import io
from dataclasses import dataclass
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "legacy" / "learning_artifacts.py"
SPEC = importlib.util.spec_from_file_location("learning_artifacts_cli", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)
JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


@dataclass
class CliResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


def run_cli(*args, check=True):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            code = MODULE.main(["--allow-legacy-helper", *list(args)])
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
    result = CliResult(["python3", str(SCRIPT), "--allow-legacy-helper", *args], int(code or 0), stdout.getvalue(), stderr.getvalue())
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed: {result.args}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def read_contract(path):
    text = Path(path).read_text(encoding="utf-8")
    match = JSON_BLOCK_RE.search(text)
    assert match, f"missing JSON block in {path}"
    return json.loads(match.group(1)), text[match.end():].lstrip("\n")


def write_contract(path, payload, body):
    Path(path).write_text(
        "```json\n" + json.dumps(payload, indent=2, ensure_ascii=False) + "\n```\n\n" + body.rstrip() + "\n",
        encoding="utf-8",
    )


def build_valid_card(card_path):
    payload, body = read_contract(card_path)
    payload.update({
        "learner_goal": "Explain why water moves across a membrane without using math.",
        "core_model": "Water moves from low to high solute concentration to equalize pressure.",
        "anchor_example": "A raisin placed in water swells because intracellular solute is higher.",
        "key_boundaries": ["applies only to semipermeable membranes"],
        "misconceptions": ["Water moves toward higher water concentration (backwards)"],
        "retrieval_hooks": ["What drives the net direction of water movement?"],
        "expansion_links": ["active-transport", "tonicity"],
        "provenance": {
            "source_facts": ["Campbell Biology ch. 7"],
            "teacher_framing": ["Lead with the raisin example before defining osmosis formally"],
        },
        "status": "draft",
    })
    write_contract(card_path, payload, body or "# Knowledge Card\n")


def build_valid_map(map_path):
    payload, body = read_contract(map_path)
    root_id = payload["start_node"]
    payload["nodes"] = [
        {
            "node_id": root_id,
            "title": payload["topic"],
            "question": "What is osmosis and when does it occur?",
            "relation": "root",
            "priority": "load-bearing",
            "status": "pending",
        },
        {
            "node_id": "tonicity",
            "title": "Tonicity",
            "question": "How do hypotonic, isotonic, and hypertonic solutions differ?",
            "relation": "extends",
            "priority": "supporting",
            "status": "pending",
        },
    ]
    payload["edges"] = [
        {"source": root_id, "target": "tonicity", "relation": "leads-to"},
    ]
    payload["open_questions"] = ["Does temperature affect the rate?"]
    payload["next_steps"] = ["Explore active transport comparison"]
    write_contract(map_path, payload, body or "# Expansion Map\n")


def build_valid_report(report_path):
    payload, body = read_contract(report_path)
    payload.update({
        "learner_goal": "Explain a medical condition through all clinically expected branches.",
        "core_model": "A stable report should preserve the full branch structure, then make each branch reason-able.",
        "reasoning_chain": [
            {
                "step": "Start from the defining disturbance.",
                "observable_consequence": "The signs, tests, and treatment priorities become predictable.",
            }
        ],
        "load_bearing_branches": [
            {
                "kernel_item": title,
                "title": title,
                "explanation": f"Explanation for {title}.",
                "boundary_or_failure_mode": f"What can go wrong when reasoning about {title}.",
            }
            for title in payload["coverage_kernel"]
        ],
        "key_boundaries": ["This is not a substitute for clinical decision-making."],
        "misconceptions": ["A nice core model is enough even when expected branches are missing."],
        "retrieval_hooks": ["Can I reconstruct every kernel branch from memory?"],
        "source_notes": ["Teacher framing only in this test."],
        "status": "draft",
    })
    write_contract(report_path, payload, body or "# Study Report\n")


class LearningArtifactsCliTests(unittest.TestCase):
    def test_legacy_helper_requires_explicit_flag(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = MODULE.main(["status", "missing"])
        result = CliResult(["python3", str(SCRIPT), "status", "missing"], int(code or 0), stdout.getvalue(), stderr.getvalue())
        self.assertEqual(result.returncode, 2)
        self.assertIn("LEGACY_HELPER_DISABLED", result.stderr)

    def test_slugify_preserves_chinese_topic(self):
        self.assertEqual(MODULE.slugify("高钙血症"), "高钙血症")
        self.assertEqual(MODULE.slugify("高钙血症 机制"), "高钙血症-机制")

    def test_positive_card_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_cli("init-card", "--topic", "Osmosis", "--out", tmpdir)
            card_path = Path(out.stdout.strip())
            self.assertTrue(card_path.exists())
            self.assertEqual(card_path.name, "knowledge_card.md")

            build_valid_card(card_path)
            result = run_cli("validate-card", str(card_path))
            self.assertIn("CARD_CHECK ok", result.stdout)

    def test_positive_map_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_cli("init-map", "--topic", "Osmosis", "--out", tmpdir)
            map_path = Path(out.stdout.strip())
            self.assertTrue(map_path.exists())
            self.assertEqual(map_path.name, "expansion_map.md")

            build_valid_map(map_path)
            result = run_cli("validate-map", str(map_path))
            self.assertIn("MAP_CHECK ok", result.stdout)
            self.assertIn("2 nodes", result.stdout)

    def test_positive_report_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_cli(
                "init-report",
                "--topic",
                "Hyponatremia",
                "--out",
                tmpdir,
                "--kernel",
                "medicine",
                "--explanatory-type",
                "mechanism",
            )
            report_path = Path(out.stdout.strip())
            self.assertTrue(report_path.exists())
            self.assertEqual(report_path.name, "study_report.md")

            payload, _ = read_contract(report_path)
            self.assertIn("what it is", payload["coverage_kernel"])
            build_valid_report(report_path)
            result = run_cli("validate-report", str(report_path))
            self.assertIn("REPORT_CHECK ok", result.stdout)
            self.assertIn("6 branches", result.stdout)

    def test_card_missing_retrieval_hook_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_cli("init-card", "--topic", "Osmosis", "--out", tmpdir)
            card_path = Path(out.stdout.strip())
            build_valid_card(card_path)

            payload, body = read_contract(card_path)
            payload["retrieval_hooks"] = []
            write_contract(card_path, payload, body or "# Knowledge Card\n")

            result = run_cli("validate-card", str(card_path), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CARD_INCOMPLETE", result.stderr)

    def test_map_bad_edge_endpoint_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_cli("init-map", "--topic", "Osmosis", "--out", tmpdir)
            map_path = Path(out.stdout.strip())
            build_valid_map(map_path)

            payload, body = read_contract(map_path)
            payload["edges"].append({
                "source": payload["start_node"],
                "target": "nonexistent-node",
                "relation": "extends",
            })
            write_contract(map_path, payload, body or "# Expansion Map\n")

            result = run_cli("validate-map", str(map_path), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("MAP_INCOMPLETE", result.stderr)

    def test_report_missing_kernel_branch_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_cli("init-report", "--topic", "Hyponatremia", "--out", tmpdir, "--kernel", "medicine")
            report_path = Path(out.stdout.strip())
            build_valid_report(report_path)

            payload, body = read_contract(report_path)
            payload["load_bearing_branches"] = payload["load_bearing_branches"][:-1]
            write_contract(report_path, payload, body or "# Study Report\n")

            result = run_cli("validate-report", str(report_path), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("REPORT_INCOMPLETE", result.stderr)

    def test_status_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            status = json.loads(run_cli("status", tmpdir).stdout)
            self.assertFalse(status["knowledge_card"]["exists"])
            self.assertFalse(status["knowledge_card"]["valid"])
            self.assertFalse(status["expansion_map"]["exists"])
            self.assertFalse(status["expansion_map"]["valid"])
            self.assertFalse(status["study_report"]["exists"])
            self.assertFalse(status["study_report"]["valid"])

            out = run_cli("init-card", "--topic", "Osmosis", "--out", tmpdir)
            card_path = Path(out.stdout.strip())
            build_valid_card(card_path)

            status = json.loads(run_cli("status", tmpdir).stdout)
            self.assertTrue(status["knowledge_card"]["exists"])
            self.assertTrue(status["knowledge_card"]["valid"])
            self.assertFalse(status["expansion_map"]["exists"])
            self.assertFalse(status["expansion_map"]["valid"])

            out = run_cli("init-map", "--topic", "Osmosis", "--out", tmpdir)
            map_path = Path(out.stdout.strip())
            build_valid_map(map_path)

            status = json.loads(run_cli("status", tmpdir).stdout)
            self.assertTrue(status["knowledge_card"]["valid"])
            self.assertTrue(status["expansion_map"]["exists"])
            self.assertTrue(status["expansion_map"]["valid"])

            out = run_cli("init-report", "--topic", "Osmosis", "--out", tmpdir)
            report_path = Path(out.stdout.strip())
            build_valid_report(report_path)

            status = json.loads(run_cli("status", tmpdir).stdout)
            self.assertTrue(status["study_report"]["exists"])
            self.assertTrue(status["study_report"]["valid"])


class RenderCardTests(unittest.TestCase):
    def _setup_card(self, tmpdir):
        out = run_cli("init-card", "--topic", "Osmosis", "--out", tmpdir)
        card_path = Path(out.stdout.strip())
        build_valid_card(card_path)
        return card_path

    def test_render_card_stdout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            card_path = self._setup_card(tmpdir)
            result = run_cli("render-card", str(card_path))
            self.assertEqual(result.returncode, 0)
            self.assertIn("# Osmosis", result.stdout)
            self.assertIn("## Learner Goal", result.stdout)
            self.assertIn("## Core Model", result.stdout)
            self.assertIn("## Retrieval Hooks", result.stdout)
            self.assertIn("## Provenance", result.stdout)
            self.assertIn("**Status:**", result.stdout)

    def test_render_card_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            card_path = self._setup_card(tmpdir)
            out_path = str(Path(tmpdir) / "rendered_card.md")
            result = run_cli("render-card", str(card_path), "--out", out_path)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            content = Path(out_path).read_text(encoding="utf-8")
            self.assertIn("# Osmosis", content)
            self.assertIn("## Retrieval Hooks", content)


class RenderMapTests(unittest.TestCase):
    def _setup_map(self, tmpdir):
        out = run_cli("init-map", "--topic", "Osmosis", "--out", tmpdir)
        map_path = Path(out.stdout.strip())
        build_valid_map(map_path)
        return map_path

    def test_render_map_stdout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            map_path = self._setup_map(tmpdir)
            result = run_cli("render-map", str(map_path))
            self.assertEqual(result.returncode, 0)
            self.assertIn("# Osmosis — Exploration Map", result.stdout)
            self.assertIn("## Nodes", result.stdout)
            self.assertIn("## Connections", result.stdout)
            self.assertIn("## Open Questions", result.stdout)
            self.assertIn("## 后续知识拓展", result.stdout)
            self.assertIn("*(pending)*", result.stdout)

    def test_render_map_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            map_path = self._setup_map(tmpdir)
            out_path = str(Path(tmpdir) / "rendered_map.md")
            result = run_cli("render-map", str(map_path), "--out", out_path)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            content = Path(out_path).read_text(encoding="utf-8")
            self.assertIn("# Osmosis — Exploration Map", content)
            self.assertIn("## Nodes", content)


class RenderReportTests(unittest.TestCase):
    def _setup_report(self, tmpdir):
        out = run_cli("init-report", "--topic", "Hyponatremia", "--out", tmpdir, "--kernel", "medicine")
        report_path = Path(out.stdout.strip())
        build_valid_report(report_path)
        return report_path

    def test_render_report_stdout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = self._setup_report(tmpdir)
            result = run_cli("render-report", str(report_path))
            self.assertEqual(result.returncode, 0)
            self.assertIn("# Hyponatremia — Study Report", result.stdout)
            self.assertIn("## Reasoning Chain", result.stdout)
            self.assertIn("## Load-Bearing Branches", result.stdout)
            self.assertIn("### what it is", result.stdout)
            self.assertIn("## Retrieval Hooks", result.stdout)

    def test_render_report_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = self._setup_report(tmpdir)
            out_path = str(Path(tmpdir) / "rendered_report.md")
            result = run_cli("render-report", str(report_path), "--out", out_path)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            content = Path(out_path).read_text(encoding="utf-8")
            self.assertIn("# Hyponatremia — Study Report", content)
            self.assertIn("## Common Misconceptions", content)


if __name__ == "__main__":
    unittest.main()
