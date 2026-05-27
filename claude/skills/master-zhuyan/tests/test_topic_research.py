import json
import re
import contextlib
import importlib.util
import io
from dataclasses import dataclass
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "topic_research.py"
SPEC = importlib.util.spec_from_file_location("topic_research_cli", SCRIPT)
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
            code = MODULE.main(list(args))
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
    result = CliResult(["python3", str(SCRIPT), *args], int(code or 0), stdout.getvalue(), stderr.getvalue())
    if check and result.returncode != 0:
        raise AssertionError(f"command failed: {result.args}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
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


def read_failure_code(run_dir):
    payload, _ = read_contract(Path(run_dir) / "failure_report.md")
    return payload["code"]


def build_framing(run_dir):
    payload, body = read_contract(Path(run_dir) / "framing_brief.md")
    payload.update(
        {
            "expert_identity": "A transformer architecture researcher who teaches implementation-relevant intuition.",
            "learner_goal": "Understand why the architecture works before reading implementation details.",
            "primary_confusion": "The learner may know the term attention but not how information is routed.",
            "entry_point": "Start from the modeling problem, then introduce attention as a routing mechanism.",
            "research_plan": "Cover foundations first, then self-attention mechanics, then defer paper-reading strategy.",
            "source_strategy": "Use stable sources for foundations and primary sources for attention mechanics.",
            "success_criteria": "The final explanation can predict why self-attention helps with one concrete example.",
        }
    )
    write_contract(Path(run_dir) / "framing_brief.md", payload, body or "# Framing Brief\n")


def build_tree(run_dir):
    build_framing(run_dir)
    payload, body = read_contract(Path(run_dir) / "tree.md")
    payload["nodes"] = [
        {
            "node_id": "foundations",
            "title": "Foundations",
            "question": "What problem does the architecture solve and what is the core idea?",
            "source_tier": "stable",
            "priority": "load-bearing",
            "stop_condition": "Covered when the node explains the model goal and one concrete mental model.",
            "prerequisites": [],
            "status": "pending",
            "owner": "",
            "skip_reason": "",
        },
        {
            "node_id": "attention",
            "title": "Attention Mechanics",
            "question": "How does self-attention actually route information?",
            "source_tier": "primary",
            "priority": "load-bearing",
            "stop_condition": "Covered when the node can explain query-key-value flow with one worked example.",
            "prerequisites": ["foundations"],
            "status": "pending",
            "owner": "",
            "skip_reason": "",
        },
        {
            "node_id": "paper-reading",
            "title": "Paper Reading Path",
            "question": "How should a learner approach the original paper after the basics?",
            "source_tier": "secondary",
            "priority": "supporting",
            "stop_condition": "Covered when the node gives a short reading sequence and one warning about overload.",
            "prerequisites": ["attention"],
            "status": "skipped",
            "owner": "",
            "skip_reason": "Out of scope for the first teaching pass.",
        },
    ]
    write_contract(Path(run_dir) / "tree.md", payload, body or "# Tree\n")


def build_dispatch(run_dir):
    payload, body = read_contract(Path(run_dir) / "dispatch.md")
    payload["dispatch"] = [
        {
            "node_id": "foundations",
            "owner": "researcher-1",
            "token_budget": 1600,
            "status": "dispatched",
            "artifact_path": "agent_outputs/foundations.md",
        },
        {
            "node_id": "attention",
            "owner": "researcher-2",
            "token_budget": 1800,
            "status": "dispatched",
            "artifact_path": "agent_outputs/attention.md",
        },
    ]
    write_contract(Path(run_dir) / "dispatch.md", payload, body or "# Dispatch\n")


def write_artifact(run_dir, node_id, *, contradictions=None, coverage_gaps=None, scope_confirmed=True):
    contradictions = contradictions or []
    coverage_gaps = coverage_gaps or []
    payload = {
        "node_id": node_id,
        "title": "Foundations" if node_id == "foundations" else "Attention Mechanics",
        "scope_confirmed": scope_confirmed,
        "scope_evidence": "Stop condition met with a concrete mechanism explanation and anchored examples.",
        "confidence_level": "high",
        "prerequisite_nodes": [] if node_id == "foundations" else ["foundations"],
        "sources": [
            {
                "source_id": f"{node_id}-s1",
                "source": f"https://example.com/{node_id}/primary",
                "title": f"{node_id} primary source",
                "excerpt": f"{node_id} excerpt",
                "tier": "primary",
            }
        ],
        "claims": [
            {
                "claim_id": f"{node_id}-c1",
                "claim": f"{node_id} teaches a distinct load-bearing concept before the learner moves on.",
                "source_ids": [f"{node_id}-s1"],
                "confidence": "high",
            }
        ],
        "evidence": [f"{node_id}-s1"],
        "examples": [f"{node_id} example"],
        "contradictions": contradictions,
        "coverage_gaps": coverage_gaps,
        "teaching_hooks": [f"Teach {node_id} before broader comparisons."],
    }
    write_contract(Path(run_dir) / "agent_outputs" / f"{node_id}.md", payload, f"# Artifact: {node_id}\n")


def prepare_positive_run(tmp_path):
    run_dir = Path(tmp_path) / "transformer-run"
    run_cli("init-tree", "--topic", "Transformer research path", "--out", str(run_dir))
    build_tree(run_dir)
    run_cli("validate-tree", str(run_dir / "tree.md"))
    build_dispatch(run_dir)
    run_cli("validate-dispatch", str(run_dir / "dispatch.md"), "--tree", str(run_dir / "tree.md"))
    write_artifact(run_dir, "foundations")
    write_artifact(
        run_dir,
        "attention",
        contradictions=["Benchmarks can overstate understanding when they ignore context limits."],
        coverage_gaps=["Needs fresh retrieval before claiming the newest production usage pattern."],
    )
    run_cli("validate-artifact", str(run_dir / "agent_outputs" / "foundations.md"))
    run_cli("validate-artifact", str(run_dir / "agent_outputs" / "attention.md"))
    return run_dir


class TopicResearchCliTests(unittest.TestCase):
    def test_slugify_preserves_chinese_topic(self):
        self.assertEqual(MODULE.slugify("高钙血症"), "高钙血症")
        self.assertEqual(MODULE.slugify("高钙血症 机制"), "高钙血症-机制")

    def test_full_positive_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = prepare_positive_run(tmpdir)
            run_cli("merge", str(run_dir))
            run_cli("validate-synthesis", str(run_dir))
            run_cli("check-coverage", str(run_dir))

            learning_path, learning_body = read_contract(run_dir / "learning_path.md")
            self.assertIn("The learner may know the term attention", learning_body)
            self.assertEqual([row["node_id"] for row in learning_path["path"]], ["foundations", "attention"])
            self.assertIn("paper-reading", learning_body)
            self.assertIn("Out of scope for the first teaching pass.", learning_body)

            synthesis, synthesis_body = read_contract(run_dir / "synthesis.md")
            self.assertIn("The learner may know the term attention", synthesis_body)
            self.assertEqual(
                synthesis["open_gaps"],
                ["attention: Needs fresh retrieval before claiming the newest production usage pattern."],
            )
            self.assertEqual(
                synthesis["open_contradictions"],
                ["attention: Benchmarks can overstate understanding when they ignore context limits."],
            )

            status = json.loads(run_cli("status", str(run_dir)).stdout)
            self.assertEqual(status["node_counts"]["complete"], 2)
            self.assertEqual(status["node_counts"]["skipped"], 1)

    def test_validate_tree_fails_when_framing_incomplete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir) / "missing-framing"
            run_cli("init-tree", "--topic", "Missing framing", "--out", str(run_dir))
            build_tree(run_dir)
            framing, body = read_contract(run_dir / "framing_brief.md")
            framing["primary_confusion"] = ""
            write_contract(run_dir / "framing_brief.md", framing, body or "# Framing Brief\n")

            result = run_cli("validate-tree", str(run_dir / "tree.md"), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "FRAMING_INCOMPLETE")

    def test_validate_tree_fails_when_stop_condition_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir) / "missing-stop"
            run_cli("init-tree", "--topic", "Missing stop condition", "--out", str(run_dir))
            build_tree(run_dir)
            tree, body = read_contract(run_dir / "tree.md")
            tree["nodes"][0]["stop_condition"] = ""
            write_contract(run_dir / "tree.md", tree, body or "# Tree\n")

            result = run_cli("validate-tree", str(run_dir / "tree.md"), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "TREE_INCOMPLETE")
            failure, failure_body = read_contract(run_dir / "failure_report.md")
            self.assertIn("Fill the missing or invalid tree field", failure["recovery"])
            self.assertIn("Recovery:", failure_body)

    def test_validate_tree_fails_on_prerequisite_cycle(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir) / "tree-cycle"
            run_cli("init-tree", "--topic", "Cycle", "--out", str(run_dir))
            build_tree(run_dir)
            tree, body = read_contract(run_dir / "tree.md")
            tree["nodes"][0]["prerequisites"] = ["attention"]
            write_contract(run_dir / "tree.md", tree, body or "# Tree\n")

            result = run_cli("validate-tree", str(run_dir / "tree.md"), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "PREREQUISITE_CYCLE")

    def test_validate_dispatch_fails_for_skipped_or_missing_node(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir) / "dispatch-fail"
            run_cli("init-tree", "--topic", "Dispatch fail", "--out", str(run_dir))
            build_tree(run_dir)
            run_cli("validate-tree", str(run_dir / "tree.md"))
            payload, body = read_contract(run_dir / "dispatch.md")
            payload["dispatch"] = [
                {
                    "node_id": "paper-reading",
                    "owner": "researcher-1",
                    "token_budget": 1200,
                    "status": "dispatched",
                    "artifact_path": "agent_outputs/paper-reading.md",
                }
            ]
            write_contract(run_dir / "dispatch.md", payload, body or "# Dispatch\n")

            result = run_cli("validate-dispatch", str(run_dir / "dispatch.md"), "--tree", str(run_dir / "tree.md"), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "DISPATCH_ORPHAN")

    def test_validate_artifact_rejects_scope_not_confirmed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = prepare_positive_run(tmpdir)
            write_artifact(run_dir, "attention", scope_confirmed=False)

            result = run_cli("validate-artifact", str(run_dir / "agent_outputs" / "attention.md"), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "SCOPE_NOT_CONFIRMED")

    def test_validate_artifact_requires_evidence_to_cover_claim_sources(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = prepare_positive_run(tmpdir)
            artifact, body = read_contract(run_dir / "agent_outputs" / "attention.md")
            artifact["evidence"] = []
            write_contract(run_dir / "agent_outputs" / "attention.md", artifact, body)

            result = run_cli("validate-artifact", str(run_dir / "agent_outputs" / "attention.md"), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "CLAIM_UNTRACEABLE")

    def test_validate_artifact_requires_prerequisites_to_match_tree(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = prepare_positive_run(tmpdir)
            artifact, body = read_contract(run_dir / "agent_outputs" / "attention.md")
            artifact["prerequisite_nodes"] = []
            write_contract(run_dir / "agent_outputs" / "attention.md", artifact, body)

            result = run_cli("validate-artifact", str(run_dir / "agent_outputs" / "attention.md"), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "ARTIFACT_INCOMPLETE")

    def test_validate_artifact_rejects_empty_examples_and_teaching_hooks(self):
        for field_name in ["examples", "teaching_hooks"]:
            with self.subTest(field_name=field_name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    run_dir = prepare_positive_run(tmpdir)
                    artifact_path = run_dir / "agent_outputs" / "attention.md"
                    artifact, body = read_contract(artifact_path)
                    artifact[field_name] = []
                    write_contract(artifact_path, artifact, body)

                    result = run_cli("validate-artifact", str(artifact_path), check=False)
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(read_failure_code(run_dir), "ARTIFACT_INCOMPLETE")

    def test_synthesis_and_coverage_reject_nonresponsive_research(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = prepare_positive_run(tmpdir)
            for node_id in ["foundations", "attention"]:
                artifact_path = run_dir / "agent_outputs" / f"{node_id}.md"
                artifact, body = read_contract(artifact_path)
                artifact["scope_evidence"] = "The assigned branch has a source-backed paragraph and can be merged."
                artifact["claims"][0]["claim"] = "The assigned branch records background notes for later comparison."
                write_contract(artifact_path, artifact, body)

            run_cli("merge", str(run_dir))

            synthesis_result = run_cli("validate-synthesis", str(run_dir), check=False)
            self.assertEqual(synthesis_result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "SYNTHESIS_UNCOVERED")

            coverage_result = run_cli("check-coverage", str(run_dir), check=False)
            self.assertEqual(coverage_result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "SYNTHESIS_UNCOVERED")

    def test_validate_synthesis_requires_skipped_nodes_to_remain_visible(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = prepare_positive_run(tmpdir)
            run_cli("merge", str(run_dir))
            synthesis, body = read_contract(run_dir / "synthesis.md")
            synthesis["nodes_skipped"] = []
            body = body.replace("## Skipped Nodes", "## Deferred Nodes")
            write_contract(run_dir / "synthesis.md", synthesis, body)

            result = run_cli("validate-synthesis", str(run_dir), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "SYNTHESIS_UNCOVERED")

    def test_validate_synthesis_fails_when_claim_trace_is_broken(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = prepare_positive_run(tmpdir)
            run_cli("merge", str(run_dir))
            source_lines = (run_dir / "source_ledger.jsonl").read_text(encoding="utf-8").splitlines()
            (run_dir / "source_ledger.jsonl").write_text("\n".join(source_lines[1:]) + "\n", encoding="utf-8")

            result = run_cli("validate-synthesis", str(run_dir), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(read_failure_code(run_dir), "CLAIM_UNTRACEABLE")

    def test_validate_synthesis_preserves_claims_with_pipe_characters(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = prepare_positive_run(tmpdir)
            artifact, body = read_contract(run_dir / "agent_outputs" / "attention.md")
            artifact["claims"][0]["claim"] = "A|B notation can appear in valid source-grounded claims."
            write_contract(run_dir / "agent_outputs" / "attention.md", artifact, body)

            run_cli("merge", str(run_dir))
            run_cli("validate-synthesis", str(run_dir))


if __name__ == "__main__":
    unittest.main()
