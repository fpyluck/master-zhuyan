from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "validate_deep_research_artifacts.py"
FIXTURE = ROOT / "tests" / "fixtures" / "deep_research_sample"


def write_single_chapter_projection(root: Path, *, chapter_id: str, title: str, output_path: str) -> None:
    (root / "manifest.yaml").write_text(
        "title: DeepResearch sample\n"
        "chapter_emphasis: understanding\n"
        "status: fixture\n"
        "chapters:\n"
        f"  - id: {chapter_id}\n"
        f"    title: {title}\n"
        f"    file: {output_path}\n"
        "    status: planned\n",
        encoding="utf-8",
    )
    (root / "index.md").write_text(
        "# DeepResearch Sample\n\n"
        "## 阅读顺序\n\n"
        f"- [{title}]({output_path})\n\n"
        "### Research Workbench\n\n"
        "- [Process Trace](notes/process_trace.md)\n"
        "- [Research Brief](notes/research_brief.md)\n"
        "- [Research Tree](notes/research_tree.md)\n"
        "- [Source Map](notes/source_map.md)\n"
        "- [Evidence Ledger](notes/evidence_ledger.md)\n"
        "- [Knowledge Model](notes/knowledge_model.md)\n"
        "- [Chapter Plan](notes/chapter_plan.md)\n"
        "- [Integrator Decisions](notes/integrator_decisions.md)\n"
        "- [Citation Audit](notes/citation_audit.md)\n"
        "- [Continuation Map](notes/continuation_map.md)\n",
        encoding="utf-8",
    )


class DeepResearchArtifactValidatorTests(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
        )

    def test_deep_research_fixture_validates(self) -> None:
        result = self.run_validator("--root", str(FIXTURE))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ok", result.stdout)
        self.assertIn("evidence_ids:", result.stdout)

    def test_deep_research_fixture_json(self) -> None:
        result = self.run_validator("--root", str(FIXTURE), "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["evidence_ids"], ["EL-fixture-claim"])
        self.assertIn("notes/research_tree.md", payload["present"])
        self.assertIn("notes/citation_audit.md", payload["present"])
        self.assertIn("notes/continuation_map.md", payload["present"])

    def test_missing_required_artifact_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "source_map.md").unlink()

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing:", result.stdout)
        self.assertIn("notes/source_map.md", result.stdout)

    def test_empty_required_artifact_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "knowledge_model.md").write_text("", encoding="utf-8")

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("empty_files:", result.stdout)
        self.assertIn("notes/knowledge_model.md", result.stdout)

    def test_research_brief_requires_primary_confusion_and_success_criteria(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "research_brief.md").write_text(
                "# Research Brief\n\nlearner_goal: validate the DeepResearch artifact validator\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing planning field: primary_confusion", result.stdout)
        self.assertIn("missing planning field: success_criteria", result.stdout)

    def test_source_map_requires_traceable_source_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "source_map.md").write_text(
                "# Source Map\n\nsource_id: fixture-source\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing source field: source_type", result.stdout)
        self.assertIn("missing source field: locator", result.stdout)
        self.assertIn("missing source field: access_method", result.stdout)
        self.assertIn("missing source field: read_state", result.stdout)
        self.assertIn("missing source field: supports_questions", result.stdout)

    def test_source_map_uses_evidence_card_ids_for_source_to_ledger_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_source_map_rejects_evidence_ids_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            source_map = broken / "notes" / "source_map.md"
            source_map.write_text(
                source_map.read_text(encoding="utf-8").replace(
                    "evidence_card_ids: EL-fixture-claim",
                    "evidence_ids: EL-fixture-claim",
                ),
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("uses evidence_ids; use evidence_card_ids", result.stdout)

    def test_source_map_evidence_card_ids_must_resolve_to_ledger_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            source_map = broken / "notes" / "source_map.md"
            source_map.write_text(
                source_map.read_text(encoding="utf-8").replace("EL-fixture-claim", "EL-ghost"),
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("references evidence_card_id not in notes/evidence_ledger.md: EL-ghost", result.stdout)

    def test_source_map_must_preserve_requires_evidence_card_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            source_map = broken / "notes" / "source_map.md"
            source_map.write_text(
                source_map.read_text(encoding="utf-8").replace(
                    "evidence_card_ids: EL-fixture-claim\n",
                    "",
                ),
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("has must_preserve details but no evidence_card_ids", result.stdout)

    def test_source_map_must_preserve_links_to_same_source_ledger_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: preserved detail came from another source\n"
                "source_ref: other-source\n"
                "locator: fixture heading\n"
                "evidence_type: mechanism\n"
                "confidence: high\n"
                "status: accepted\n"
                "teaching_use: core_explanation\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("must_preserve details are not linked to same-source", result.stdout)

    def test_accepted_must_preserve_precision_must_reach_model_and_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            source_map = broken / "notes" / "source_map.md"
            source_map.write_text(
                source_map.read_text(encoding="utf-8")
                .replace(
                    "must_preserve: semantic integration signals",
                    "must_preserve: normal range 3.5-5.0; threshold above reference frame",
                )
                .replace("evidence_card_ids: EL-fixture-claim", "evidence_card_ids: EL-fixture-claim, EL-precision"),
                encoding="utf-8",
            )
            with (broken / "notes" / "evidence_ledger.md").open("a", encoding="utf-8") as handle:
                handle.write(
                    "\nclaim_id: EL-precision\n"
                    "claim: normal range 3.5-5.0 anchors the threshold interpretation\n"
                    "source_ref: fixture-source\n"
                    "locator: fixture heading\n"
                    "evidence_type: threshold\n"
                    "confidence: high\n"
                    "status: accepted\n"
                    "teaching_use: boundary\n"
                )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("accepted must_preserve evidence is missing from notes/knowledge_model.md: EL-precision", result.stdout)
        self.assertIn("accepted must_preserve evidence is missing from notes/chapter_plan.md: EL-precision", result.stdout)

    def test_accepted_must_preserve_mechanism_must_reach_model_and_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            source_map = broken / "notes" / "source_map.md"
            source_map.write_text(
                source_map.read_text(encoding="utf-8")
                .replace(
                    "must_preserve: semantic integration signals",
                    "must_preserve: semantic integration signals; mechanism bridge must survive",
                )
                .replace("evidence_card_ids: EL-fixture-claim", "evidence_card_ids: EL-fixture-claim, EL-mechanism"),
                encoding="utf-8",
            )
            with (broken / "notes" / "evidence_ledger.md").open("a", encoding="utf-8") as handle:
                handle.write(
                    "\nclaim_id: EL-mechanism\n"
                    "claim: mechanism bridge must survive from evidence into teaching synthesis\n"
                    "source_ref: fixture-source\n"
                    "locator: fixture heading\n"
                    "evidence_type: mechanism\n"
                    "confidence: high\n"
                    "status: accepted\n"
                    "teaching_use: core_explanation\n"
                )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("accepted must_preserve evidence is missing from notes/knowledge_model.md: EL-mechanism", result.stdout)
        self.assertIn("accepted must_preserve evidence is missing from notes/chapter_plan.md: EL-mechanism", result.stdout)

    def test_accepted_must_preserve_precision_in_model_and_plan_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            source_map = sample / "notes" / "source_map.md"
            source_map.write_text(
                source_map.read_text(encoding="utf-8")
                .replace(
                    "must_preserve: semantic integration signals",
                    "must_preserve: normal range 3.5-5.0; threshold above reference frame",
                )
                .replace("evidence_card_ids: EL-fixture-claim", "evidence_card_ids: EL-fixture-claim, EL-precision"),
                encoding="utf-8",
            )
            with (sample / "notes" / "evidence_ledger.md").open("a", encoding="utf-8") as handle:
                handle.write(
                    "\nclaim_id: EL-precision\n"
                    "claim: normal range 3.5-5.0 anchors the threshold interpretation\n"
                    "source_ref: fixture-source\n"
                    "locator: fixture heading\n"
                    "evidence_type: threshold\n"
                    "confidence: high\n"
                    "status: accepted\n"
                    "teaching_use: boundary\n"
                )
            knowledge_model = sample / "notes" / "knowledge_model.md"
            knowledge_model.write_text(
                knowledge_model.read_text(encoding="utf-8").replace(
                    "evidence_ids: EL-fixture-claim",
                    "evidence_ids: EL-fixture-claim, EL-precision",
                ),
                encoding="utf-8",
            )
            chapter_plan = sample / "notes" / "chapter_plan.md"
            chapter_plan.write_text(
                chapter_plan.read_text(encoding="utf-8")
                .replace("precision_anchors: EL-fixture-claim", "precision_anchors: EL-fixture-claim, EL-precision")
                .replace(
                    "required_anchors: EL-fixture-claim, locked knowledge model, supported citation audit",
                    "required_anchors: EL-fixture-claim, EL-precision, locked knowledge model, supported citation audit",
                ),
                encoding="utf-8",
            )
            citation_audit = sample / "notes" / "citation_audit.md"
            citation_audit.write_text(
                citation_audit.read_text(encoding="utf-8").replace(
                    "evidence_ids: EL-fixture-claim",
                    "evidence_ids: EL-fixture-claim, EL-precision",
                ),
                encoding="utf-8",
            )
            sidecar = sample / "notes" / "agent_outputs" / "teaching_composer" / "01_overview" / "sample.md"
            sidecar.write_text(
                sidecar.read_text(encoding="utf-8").replace(
                    "evidence_ids_used: EL-fixture-claim",
                    "evidence_ids_used: EL-fixture-claim, EL-precision",
                ),
                encoding="utf-8",
            )
            (sample / "chapters" / "01_overview.md").write_text(
                "# Overview\n\n"
                "This chapter teaches that DeepResearch workbench artifacts need semantic integration signals.\n\n"
                "The normal range 3.5-5.0 anchors the threshold interpretation for EL-precision.\n",
                encoding="utf-8",
            )
            (sample / "final" / "final_merged.md").write_text(
                "# DeepResearch Sample\n\n"
                "DeepResearch workbench artifacts need semantic integration signals, and the normal range "
                "3.5-5.0 anchors the threshold interpretation.\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_required_evidence_needs_claim_content_not_only_visible_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "chapters" / "01_overview.md").write_text(
                "# Overview\n\nEL-fixture-claim\n",
                encoding="utf-8",
            )
            (broken / "final" / "final_merged.md").write_text(
                "# DeepResearch Sample\n\nEL-fixture-claim\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("lacks claim content in cited chapter/final target", result.stdout)

    def test_required_evidence_claim_content_can_be_replaced_by_resolution_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            (sample / "chapters" / "01_overview.md").write_text(
                "# Overview\n\nEL-fixture-claim\n",
                encoding="utf-8",
            )
            (sample / "final" / "final_merged.md").write_text(
                "# DeepResearch Sample\n\nEL-fixture-claim\n",
                encoding="utf-8",
            )
            (sample / "notes" / "citation_audit.md").write_text(
                "# Citation Audit\n\n"
                "claim_or_section: chapters/01_overview.md\n"
                "evidence_ids: EL-fixture-claim\n"
                "source_ids: fixture-source\n"
                "locator_check: source map contains fixture-source\n"
                "support_state: missing\n"
                "integrator_action: mark_unavailable\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_chapter_plan_required_evidence_needs_chapter_or_final_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            citation_audit = broken / "notes" / "citation_audit.md"
            citation_audit.write_text(
                citation_audit.read_text(encoding="utf-8").replace(
                    "claim_or_section: chapters/01_overview.md",
                    "claim_or_section: unrelated quality note",
                ),
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "chapter_plan required evidence lacks chapter/final citation or integrator resolution for 01_overview: EL-fixture-claim",
            result.stdout,
        )

    def test_evidence_source_ref_must_exist_in_source_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: evidence source refs must be retraceable\n"
                "source_ref: missing-source\n"
                "locator: fixture heading\n"
                "evidence_type: mechanism\n"
                "confidence: high\n"
                "status: accepted\n"
                "teaching_use: core_explanation\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("references source not in notes/source_map.md: missing-source", result.stdout)

    def test_empty_agent_outputs_allowed_with_recorded_agent_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            shutil.rmtree(broken / "notes" / "agent_outputs")
            (broken / "notes" / "integrator_decisions.md").write_text(
                "# Integrator Decisions\n\n"
                "decision_id: agent-runtime-fallback\n"
                "result: accepted\n"
                "execution: native agent runtime unavailable; fallback to 5.26 sequential research/modeling for this artifact.\n"
                "source_artifact: notes/agent_outputs/fallback/sequential-research.md\n"
                "promoted_to: chapters/01_overview.md\n"
                "source_section_id: 01_overview\n"
                "reason: fallback artifact accepted by integrator\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ok", result.stdout)

    def test_agent_outputs_directory_not_required_for_recorded_runtime_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            shutil.rmtree(broken / "notes" / "agent_outputs")
            (broken / "notes" / "integrator_decisions.md").write_text(
                "# Integrator Decisions\n\n"
                "decision_id: agent-runtime-fallback\n"
                "result: accepted\n"
                "execution: agent_runtime_unavailable; fallback to 5.26 sequential research/modeling for this artifact.\n"
                "source_artifact: notes/agent_outputs/fallback/sequential-research.md\n"
                "promoted_to: chapters/01_overview.md\n"
                "source_section_id: 01_overview\n"
                "reason: fallback artifact accepted by integrator\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ok", result.stdout)

    def test_empty_agent_outputs_without_concrete_fallback_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            shutil.rmtree(broken / "notes" / "agent_outputs")
            (broken / "notes" / "integrator_decisions.md").write_text(
                "# Integrator Decisions\n\nresult: accepted\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("semantic_failures:", result.stdout)
        self.assertIn("no traceable agent runtime/tool/worker fallback artifact", result.stdout)

    def test_fallback_label_without_artifact_and_target_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            shutil.rmtree(broken / "notes" / "agent_outputs")
            (broken / "notes" / "integrator_decisions.md").write_text(
                "# Integrator Decisions\n\n"
                "decision_id: agent-runtime-fallback\n"
                "result: accepted\n"
                "execution: agent_runtime_unavailable; fallback to 5.26 sequential research/modeling for this artifact.\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("no traceable agent runtime/tool/worker fallback artifact", result.stdout)

    def test_metadata_plan_fails_even_when_numbered_00(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "chapter_plan.md").write_text(
                "# Chapter Plan\n\n"
                "chapter_id: 00\n"
                "title: 阅读地图与安全边界\n"
                "purpose: explain how to read the package\n"
                "required_anchors: source map, safety boundary\n"
                "output_path: chapters/00_reading-map.md\n"
                "completion_criteria: user knows the reading order\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("metadata", result.stdout)

    def test_00_knowledge_overview_warns_but_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            (sample / "notes" / "chapter_plan.md").write_text(
                "# Chapter Plan\n\n"
                "chapter_id: 00_reference_frame\n"
                "title: 基线状态与第一判断\n"
                "purpose: teach the reference frame that later thresholds depend on\n"
                "input_refs: notes/knowledge_model.md, notes/evidence_ledger.md\n"
                "required_anchors: EL-fixture-claim, reference_frame\n"
                "output_path: chapters/00_reference-frame.md\n"
                "completion_criteria: learner can state the baseline before applying thresholds\n",
                encoding="utf-8",
            )
            write_single_chapter_projection(
                sample,
                chapter_id="00_reference_frame",
                title="基线状态与第一判断",
                output_path="chapters/00_reference-frame.md",
            )
            output = (
                sample
                / "notes"
                / "agent_outputs"
                / "teaching_composer"
                / "00_reference_frame"
                / "sample.md"
            )
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                "agent_id: teaching_composer_00_reference_frame\n"
                "agent_type: teaching_composer\n"
                "mission: draft the reference-frame chapter\n"
                "input_artifacts: notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md\n"
                "output_targets: chapters/00_reference-frame.md\n\n"
                "trace_update:\n"
                "  artifacts_read: notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md\n"
                "  artifacts_written: notes/agent_outputs/teaching_composer/00_reference_frame/sample.md\n"
                "  canonical_targets: chapters/00_reference-frame.md\n"
                "  strong_findings: EL-fixture-claim\n",
                encoding="utf-8",
            )
            (sample / "chapters" / "00_reference-frame.md").write_text(
                "# 基线状态与第一判断\n\n"
                "This chapter teaches the reference frame for EL-fixture-claim.\n",
                encoding="utf-8",
            )
            with (sample / "notes" / "integrator_decisions.md").open("a", encoding="utf-8") as handle:
                handle.write(
                    "\nsource_artifact: notes/agent_outputs/teaching_composer/00_reference_frame/sample.md\n"
                    "promoted_to: chapters/00_reference-frame.md\n"
                    "source_section_id: 00_reference_frame\n"
                    "result: accepted\n"
                )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0)
        self.assertIn("warnings:", result.stdout)
        self.assertIn("leading chapter id", result.stdout)

    def test_reference_frame_in_evidence_missing_from_plan_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            with (sample / "notes" / "evidence_ledger.md").open("a", encoding="utf-8") as handle:
                handle.write(
                    "\nclaim_id: EL-reference\n"
                    "claim: deviation threshold depends on a source-grounded reference_frame baseline\n"
                    "source_ref: fixture-source\n"
                    "locator: fixture heading\n"
                    "evidence_type: threshold\n"
                    "confidence: high\n"
                    "status: accepted\n"
                    "teaching_use: boundary\n"
                )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0)
        self.assertIn("reference frame appears in evidence ledger", result.stdout)

    def test_evidence_entry_requires_source_locator_and_teaching_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-thin\n"
                "claim: thin evidence should not pass as a teachable claim\n"
                "status: accepted\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing evidence field: source_ref", result.stdout)
        self.assertIn("missing evidence field: locator", result.stdout)
        self.assertIn("missing evidence field: evidence_type", result.stdout)
        self.assertIn("missing evidence field: confidence", result.stdout)
        self.assertIn("missing evidence field: teaching_use", result.stdout)

    def test_accepted_evidence_cannot_be_inferred_confidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-inferred\n"
                "claim: inferred evidence needs visible support state\n"
                "source_ref: fixture-source\n"
                "locator: fixture heading\n"
                "evidence_type: mechanism\n"
                "confidence: inferred\n"
                "status: accepted\n"
                "teaching_use: core_explanation\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot be accepted with confidence", result.stdout)

    def test_evidence_entry_accepts_support_state_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            (sample / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: support_state is accepted as the schema-shaped support field\n"
                "source_ref: fixture-source\n"
                "locator: fixture heading\n"
                "evidence_type: mechanism\n"
                "confidence: high\n"
                "support_state: strong\n"
                "teaching_use: core_explanation\n",
                encoding="utf-8",
            )
            (sample / "chapters" / "01_overview.md").write_text(
                "# Overview\n\n"
                "This chapter confirms that support_state is accepted as the schema-shaped support field.\n",
                encoding="utf-8",
            )
            (sample / "final" / "final_merged.md").write_text(
                "# DeepResearch Sample\n\n"
                "support_state is accepted as the schema-shaped support field.\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_evidence_entry_accepts_source_id_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            (sample / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: source_id is accepted as the schema-shaped source field\n"
                "source_id: fixture-source\n"
                "locator: fixture heading\n"
                "evidence_type: mechanism\n"
                "confidence: high\n"
                "status: accepted\n"
                "teaching_use: core_explanation\n",
                encoding="utf-8",
            )
            (sample / "chapters" / "01_overview.md").write_text(
                "# Overview\n\n"
                "This chapter confirms that source_id is accepted as the schema-shaped source field.\n",
                encoding="utf-8",
            )
            (sample / "final" / "final_merged.md").write_text(
                "# DeepResearch Sample\n\n"
                "source_id is accepted as the schema-shaped source field.\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_evidence_references_must_match_structured_ledger_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: structured evidence mentions EL-ghost only as text\n"
                "source_ref: fixture-source\n"
                "locator: fixture heading\n"
                "evidence_type: mechanism\n"
                "confidence: high\n"
                "status: accepted\n"
                "teaching_use: core_explanation\n",
                encoding="utf-8",
            )
            (broken / "notes" / "knowledge_model.md").write_text(
                "# Knowledge Model\n\n"
                "locked: true\n"
                "core_model: ghost evidence reference\n"
                "evidence_ids: EL-ghost\n",
                encoding="utf-8",
            )
            (broken / "notes" / "citation_audit.md").write_text(
                "# Citation Audit\n\n"
                "claim_or_section: ghost reference\n"
                "evidence_ids: EL-ghost\n"
                "source_ids: fixture-source\n"
                "locator_check: source map contains fixture-source\n"
                "support_state: supported\n"
                "integrator_action: accept\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("knowledge_model.md does not reference any evidence id", result.stdout)
        self.assertIn("citation_audit.md does not reference any evidence id", result.stdout)

    def test_evidence_entry_rejects_unsupported_teaching_use(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: teaching use must map to the existing schema contract\n"
                "source_ref: fixture-source\n"
                "locator: fixture heading\n"
                "evidence_type: mechanism\n"
                "confidence: high\n"
                "status: accepted\n"
                "teaching_use: decorative_slot\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("unsupported teaching_use: decorative_slot", result.stdout)

    def test_knowledge_model_cannot_use_weak_evidence_without_uncertainty_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: weak evidence needs downstream uncertainty handling\n"
                "source_ref: fixture-source\n"
                "locator: fixture heading\n"
                "evidence_type: mechanism\n"
                "confidence: low\n"
                "status: uncertain\n"
                "teaching_use: core_explanation\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("uses weak evidence without uncertainty", result.stdout)

    def test_citation_audit_can_handle_weak_evidence_with_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            (sample / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: weak evidence can remain when the audit weakens the claim\n"
                "source_ref: fixture-source\n"
                "locator: fixture heading\n"
                "evidence_type: mechanism\n"
                "confidence: low\n"
                "status: uncertain\n"
                "teaching_use: core_explanation\n",
                encoding="utf-8",
            )
            (sample / "notes" / "knowledge_model.md").write_text(
                "# Knowledge Model\n\n"
                "locked: true\n"
                "core_model: workbench completeness with uncertain evidence\n"
                "evidence_ids: EL-fixture-claim\n"
                "support_state: uncertain; integrator_action: soften_claim\n",
                encoding="utf-8",
            )
            (sample / "notes" / "citation_audit.md").write_text(
                "# Citation Audit\n\n"
                "claim_or_section: chapters/01_overview.md\n"
                "evidence_ids: EL-fixture-claim\n"
                "source_ids: fixture-source\n"
                "locator_check: source map contains fixture-source\n"
                "support_state: partial\n"
                "integrator_action: soften_claim\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_citation_audit_requires_source_ids_and_locator_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "citation_audit.md").write_text(
                "# Citation Audit\n\n"
                "claim_or_section: citation without source locator\n"
                "evidence_ids: EL-fixture-claim\n"
                "support_state: supported\n"
                "integrator_action: accept\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing citation field: source_ids", result.stdout)
        self.assertIn("missing citation field: locator_check", result.stdout)

    def test_citation_audit_source_ids_must_exist_in_source_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "citation_audit.md").write_text(
                "# Citation Audit\n\n"
                "claim_or_section: citation with missing source\n"
                "evidence_ids: EL-fixture-claim\n"
                "source_ids: missing-source\n"
                "locator_check: missing source should fail\n"
                "support_state: supported\n"
                "integrator_action: accept\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("references source not in notes/source_map.md: missing-source", result.stdout)

    def test_citation_audit_rejects_alias_action_and_accepting_weak_support(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "citation_audit.md").write_text(
                "# Citation Audit\n\n"
                "claim_or_section: weak citation with alias action\n"
                "evidence_ids: EL-fixture-claim\n"
                "source_ids: fixture-source\n"
                "locator_check: source map contains fixture-source\n"
                "support_state: partial\n"
                "integrator_action: weaken\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("unsupported integrator_action: weaken", result.stdout)

    def test_load_bearing_reference_gap_without_action_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: threshold needs a reference frame before teaching\n"
                "source_ref: fixture-source\n"
                "locator: fixture heading\n"
                "evidence_type: threshold\n"
                "confidence: low\n"
                "status: uncertain\n"
                "teaching_use: boundary\n",
                encoding="utf-8",
            )
            (broken / "notes" / "knowledge_model.md").write_text(
                "# Knowledge Model\n\n"
                "locked: true\n"
                "core_model: threshold depends on weak evidence\n"
                "evidence_ids: EL-fixture-claim\n"
                "support_state: uncertain; integrator_action: soften_claim\n",
                encoding="utf-8",
            )
            (broken / "notes" / "citation_audit.md").write_text(
                "# Citation Audit\n\n"
                "claim_or_section: chapters/01_overview.md\n"
                "evidence_ids: EL-fixture-claim\n"
                "source_ids: fixture-source\n"
                "locator_check: source map contains fixture-source\n"
                "support_state: partial\n"
                "integrator_action: accept\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("reference-frame or precision gap lacks", result.stdout)

    def test_load_bearing_reference_gap_with_audit_action_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            (sample / "notes" / "evidence_ledger.md").write_text(
                "# Evidence Ledger\n\n"
                "claim_id: EL-fixture-claim\n"
                "claim: threshold needs a reference frame before teaching\n"
                "source_ref: fixture-source\n"
                "locator: fixture heading\n"
                "evidence_type: threshold\n"
                "confidence: low\n"
                "status: uncertain\n"
                "teaching_use: boundary\n",
                encoding="utf-8",
            )
            (sample / "notes" / "knowledge_model.md").write_text(
                "# Knowledge Model\n\n"
                "locked: true\n"
                "core_model: threshold depends on weak evidence\n"
                "evidence_ids: EL-fixture-claim\n"
                "support_state: uncertain; integrator_action: soften_claim\n",
                encoding="utf-8",
            )
            (sample / "notes" / "citation_audit.md").write_text(
                "# Citation Audit\n\n"
                "claim_or_section: chapters/01_overview.md\n"
                "evidence_ids: EL-fixture-claim\n"
                "source_ids: fixture-source\n"
                "locator_check: source map contains fixture-source\n"
                "support_state: partial\n"
                "integrator_action: mark_unavailable\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_chapter_plan_requires_lesson_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "chapter_plan.md").write_text(
                "# Chapter Plan\n\nchapter_id: 01_overview\nobjective: old loose objective\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing lesson-plan field: purpose", result.stdout)
        self.assertIn("missing lesson-plan field: required_anchors", result.stdout)
        self.assertIn("missing lesson-plan field: completion_criteria", result.stdout)

    def test_chapter_plan_requires_row_local_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "chapter_plan.md").write_text(
                "# Chapter Plan\n\n"
                "learner_bottleneck: needs row-local chapter contracts\n"
                "selected_spine: two chapter rows\n"
                "precision_anchors: EL-fixture-claim\n\n"
                "chapter_id: 01_overview\n"
                "title: Workbench overview\n"
                "purpose: explain the workbench\n"
                "input_refs: notes/knowledge_model.md\n"
                "required_anchors: EL-fixture-claim\n"
                "output_path: chapters/01_overview.md\n"
                "completion_criteria: learner can name the artifact spine\n\n"
                "chapter_id: 02_missing_target\n"
                "title: Missing target\n"
                "purpose: show that fields are checked per row\n"
                "input_refs: notes/knowledge_model.md\n"
                "required_anchors: EL-fixture-claim\n"
                "completion_criteria: learner can see the missing output path\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("row 02_missing_target missing lesson-plan field: output_path", result.stdout)

    def test_missing_teaching_composer_sidecar_fails_without_chapter_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            shutil.rmtree(sample / "notes" / "agent_outputs" / "teaching_composer")

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 1)
        self.assertIn("semantic_failures:", result.stdout)
        self.assertIn("has no Teaching Composer sidecar", result.stdout)

    def test_chapter_fallback_must_be_row_local(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            shutil.rmtree(broken / "notes" / "agent_outputs" / "teaching_composer")
            with (broken / "notes" / "integrator_decisions.md").open("a", encoding="utf-8") as handle:
                handle.write(
                    "\n\ndecision_id: unrelated-agent-runtime-fallback\n"
                    "result: accepted\n"
                    "execution: agent_runtime_unavailable; fallback to sequential modeling for this artifact.\n"
                    "source_artifact: notes/agent_outputs/fallback/other-section.md\n"
                    "promoted_to: chapters/other.md\n"
                    "source_section_id: other_section\n"
                    "reason: fallback artifact accepted by integrator\n"
                )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("has no Teaching Composer sidecar", result.stdout)

    def test_chapter_row_local_fallback_can_replace_missing_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            shutil.rmtree(sample / "notes" / "agent_outputs" / "teaching_composer")
            (sample / "notes" / "integrator_decisions.md").write_text(
                "# Integrator Decisions\n\n"
                "decision_id: chapter-runtime-fallback\n"
                "result: accepted\n"
                "execution: agent_runtime_unavailable; fallback to sequential Teaching Composer for this chapter row.\n"
                "source_artifact: notes/agent_outputs/fallback/teaching-composer-01-overview.md\n"
                "promoted_to: chapters/01_overview.md\n"
                "source_section_id: 01_overview\n"
                "reason: row-local fallback artifact accepted by integrator\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_safety_topic_chapter_can_pass_when_it_teaches_risk(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            (sample / "notes" / "chapter_plan.md").write_text(
                "# Chapter Plan\n\n"
                "learner_bottleneck: needs to understand risk logic, not delivery metadata\n"
                "selected_spine: risk mechanism -> boundary judgment\n"
                "precision_anchors: EL-fixture-claim\n\n"
                "chapter_id: 01_safety_logic\n"
                "title: 风险机制与边界判断\n"
                "purpose: teach how the risk mechanism changes judgment\n"
                "input_refs: notes/knowledge_model.md, notes/evidence_ledger.md\n"
                "required_anchors: EL-fixture-claim, risk mechanism, boundary judgment\n"
                "output_path: chapters/01_safety_logic.md\n"
                "completion_criteria: learner can explain why the boundary matters\n",
                encoding="utf-8",
            )
            write_single_chapter_projection(
                sample,
                chapter_id="01_safety_logic",
                title="风险机制与边界判断",
                output_path="chapters/01_safety_logic.md",
            )
            output = sample / "notes" / "agent_outputs" / "teaching_composer" / "01_safety_logic" / "sample.md"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                "agent_id: teaching_composer_01_safety_logic\n"
                "agent_type: teaching_composer\n"
                "mission: draft the safety logic chapter\n"
                "input_artifacts: notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md\n"
                "output_targets: chapters/01_safety_logic.md\n\n"
                "trace_update:\n"
                "  artifacts_read: notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md\n"
                "  artifacts_written: notes/agent_outputs/teaching_composer/01_safety_logic/sample.md\n"
                "  canonical_targets: chapters/01_safety_logic.md\n"
                "  strong_findings: EL-fixture-claim\n",
                encoding="utf-8",
            )
            (sample / "chapters" / "01_safety_logic.md").write_text(
                "# 风险机制与边界判断\n\n"
                "This chapter teaches the risk mechanism and boundary judgment for EL-fixture-claim.\n",
                encoding="utf-8",
            )
            with (sample / "notes" / "integrator_decisions.md").open("a", encoding="utf-8") as handle:
                handle.write(
                    "\nsource_artifact: notes/agent_outputs/teaching_composer/01_safety_logic/sample.md\n"
                    "promoted_to: chapters/01_safety_logic.md\n"
                    "source_section_id: 01_safety_logic\n"
                    "result: accepted\n"
                )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_teaching_composer_sidecar_must_target_chapter_output_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            output = broken / "notes" / "agent_outputs" / "teaching_composer" / "01_overview" / "sample.md"
            text = output.read_text(encoding="utf-8").replace("chapters/01_overview.md", "chapters/wrong.md")
            output.write_text(text, encoding="utf-8")

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("does not target chapter output_path", result.stdout)

    def test_teaching_composer_sidecar_requires_model_plan_and_evidence_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            output = broken / "notes" / "agent_outputs" / "teaching_composer" / "01_overview" / "sample.md"
            output.write_text(
                output.read_text(encoding="utf-8").replace(", notes/evidence_ledger.md", ""),
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing required input artifact notes/evidence_ledger.md", result.stdout)

    def test_chapter_plan_output_path_must_be_existing_chapter_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            plan = broken / "notes" / "chapter_plan.md"
            plan.write_text(
                plan.read_text(encoding="utf-8").replace(
                    "output_path: chapters/01_overview.md",
                    "output_path: notes/agent_outputs/teaching_composer/01_overview/sample.md",
                ),
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("output_path is not an existing chapter file", result.stdout)

    def test_manifest_chapters_must_project_current_chapter_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "manifest.yaml").write_text(
                "title: DeepResearch sample\n"
                "chapter_emphasis: understanding\n"
                "status: fixture\n"
                "chapters:\n"
                "  - id: stale\n"
                "    title: Stale chapter\n"
                "    file: chapters/stale.md\n"
                "    status: planned\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("manifest.yaml chapters do not match notes/chapter_plan.md rows", result.stdout)

    def test_index_must_link_manifest_chapter_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "index.md").write_text(
                "# DeepResearch Sample\n\n"
                "### Research Workbench\n\n"
                "- [Process Trace](notes/process_trace.md)\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("index.md reading order missing manifest chapter link: chapters/01_overview.md", result.stdout)

    def test_teaching_composer_sidecar_requires_integrator_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "integrator_decisions.md").write_text(
                "# Integrator Decisions\n\n"
                "promotion_id: source-only\n"
                "source_artifact: notes/agent_outputs/source_scout/sample.md\n"
                "promoted_to: notes/source_map.md\n"
                "result: accepted\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("lacks integrator decision for chapter_id 01_overview", result.stdout)

    def test_teaching_composer_decision_must_be_in_same_decision_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "integrator_decisions.md").write_text(
                "# Integrator Decisions\n\n"
                "promotion_id: source-only\n"
                "source_artifact: notes/agent_outputs/source_scout/sample.md\n"
                "promoted_to: notes/source_map.md\n"
                "result: accepted\n\n"
                "notes/agent_outputs/teaching_composer/01_overview/sample.md\n"
                "chapters/01_overview.md\n"
                "source_section_id: 01_overview\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("lacks integrator decision for chapter_id 01_overview", result.stdout)

    def test_teaching_composer_decision_must_bind_sidecar_target_and_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "integrator_decisions.md").write_text(
                "# Integrator Decisions\n\n"
                "promotion_id: weak-chapter-promotion\n"
                "promoted_to: chapters/01_overview.md\n"
                "source_section_id: 01_overview\n"
                "result: accepted\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("lacks integrator decision for chapter_id 01_overview", result.stdout)

    def test_agent_output_without_trace_update_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            output = broken / "notes" / "agent_outputs" / "source_scout" / "sample.md"
            output.write_text("agent_type: source_scout\n\nNo trace here.\n", encoding="utf-8")

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("semantic_failures:", result.stdout)
        self.assertIn("Trace Update", result.stdout)

    def test_agent_output_accepts_trace_update_field_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, sample)
            output = sample / "notes" / "agent_outputs" / "teaching_composer" / "01_overview" / "sample.md"
            output.write_text(
                "agent_id: teaching_composer_01_overview\n"
                "agent_type: teaching_composer\n"
                "mission: draft the assigned chapter\n"
                "input_artifacts: notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md\n"
                "output_targets: chapters/01_overview.md\n\n"
                "canonical_promotion_hints:\n"
                "  promote_to: chapters/01_overview.md\n"
                "  sections_or_entries: 01_overview\n"
                "  edits_needed: integrator review\n"
                "trace_update:\n"
                "  artifacts_read: notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md\n"
                "  artifacts_written: notes/agent_outputs/teaching_composer/01_overview/sample.md\n"
                "  canonical_targets: chapters/01_overview.md\n"
                "  strong_findings: EL-fixture-claim\n"
                "  open_branches: none\n"
                "  handoff_suggestion: integrator\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(sample))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_knowledge_model_without_evidence_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "knowledge_model.md").write_text(
                "# Knowledge Model\n\nlocked: true\ncore_model: unsupported model\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("does not reference any evidence id", result.stdout)

    def test_knowledge_model_evidence_id_must_be_in_field_not_free_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "knowledge_model.md").write_text(
                "# Knowledge Model\n\n"
                "locked: true\n"
                "core_model: unsupported model that only mentions EL-fixture-claim in prose\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("does not reference any evidence id", result.stdout)

    def test_knowledge_model_rejects_unknown_field_evidence_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "knowledge_model.md").write_text(
                "# Knowledge Model\n\n"
                "locked: true\n"
                "core_model: model with unknown evidence field\n"
                "evidence_ids: EL-ghost\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("references evidence not in notes/evidence_ledger.md: EL-ghost", result.stdout)

    def test_knowledge_model_supported_entry_requires_evidence_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "knowledge_model.md").write_text(
                "# Knowledge Model\n\n"
                "locked: true\n"
                "core_model: model with one supported concept\n"
                "evidence_ids: EL-fixture-claim\n\n"
                "concept: traceability\n"
                "definition: final claims must stay traceable\n"
                "support_state: supported\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("is supported but has no evidence_ids", result.stdout)

    def test_integrator_without_promotion_decision_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "notes" / "integrator_decisions.md").write_text(
                "# Integrator Decisions\n\nsource_artifact: notes/agent_outputs/source_scout/sample.md\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("does not record promotion", result.stdout)

    def test_final_output_with_source_placeholder_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            broken = Path(tmpdir) / "deep_research_sample"
            shutil.copytree(FIXTURE, broken)
            (broken / "final" / "final_merged.md").write_text(
                "# DeepResearch Sample\n\nThis claim still has [CITATION].\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", str(broken))

        self.assertEqual(result.returncode, 1)
        self.assertIn("placeholder source or citation markers", result.stdout)


if __name__ == "__main__":
    unittest.main()
