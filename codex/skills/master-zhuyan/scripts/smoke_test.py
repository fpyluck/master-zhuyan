#!/usr/bin/env python3
"""Smoke-test master-zhuyan helper scripts without requiring external services."""

from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREP_PATH = ROOT / "scripts" / "prep_template.py"
VALIDATOR_PATH = ROOT / "scripts" / "validate_deep_research_artifacts.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


PREP = load_module("mz_prep_template", PREP_PATH)
VALIDATOR = load_module("mz_validate_deep_research_artifacts", VALIDATOR_PATH)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def exercise_prep_templates(tmpdir: Path) -> None:
    local_dir = tmpdir / "prep_templates"
    created = PREP.create_template("猫", "优先教材和本轮材料，少联网，适合外科学复习。", local_dir)
    if not created.exists():
        raise AssertionError("prep template init did not create a file")
    matches = PREP.find_matches("请用猫式讲解急性阑尾炎", local_dir)
    if not matches or matches[0].name != "猫":
        raise AssertionError("prep template match did not activate explicit arbitrary style")
    bare_matches = PREP.find_matches("请讲一下猫抓病的临床表现", local_dir)
    if bare_matches:
        raise AssertionError("bare ordinary template name should not activate a prep template")
    PREP.create_template("外星人", "强调反常识类比。", local_dir)
    matches = PREP.find_matches("请按外星人教案讲解这段内容", local_dir)
    if not matches or matches[0].name != "外星人":
        raise AssertionError("arbitrary template names should be matchable through explicit activation phrases")


def build_deep_research_sample(root: Path) -> None:
    write_text(
        root / "manifest.yaml",
        "title: DeepResearch smoke sample\n"
        "chapter_emphasis: understanding\n"
        "status: smoke\n"
        "chapters:\n"
        "  - id: 01_overview\n"
        "    title: Workbench overview\n"
        "    file: chapters/01_overview.md\n"
        "    status: planned\n",
    )
    write_text(
        root / "index.md",
        "# DeepResearch Smoke Sample\n\n"
        "## 阅读顺序\n\n"
        "- [Workbench overview](chapters/01_overview.md)\n\n"
        "### Research Workbench\n\n"
        "- [Process Trace](notes/process_trace.md)\n"
        "- [Research Tree](notes/research_tree.md)\n"
        "- [Citation Audit](notes/citation_audit.md)\n"
        "- [Continuation Map](notes/continuation_map.md)\n",
    )
    write_text(
        root / "chapters" / "01_overview.md",
        "# Overview\n\n"
        "This compact chapter teaches that semantic workbench validation needs evidence integration.\n",
    )
    write_text(
        root / "final" / "final_merged.md",
        "# DeepResearch Smoke Sample\n\n"
        "The merged output preserves that semantic workbench validation needs evidence integration.\n",
    )
    write_text(root / "notes" / "process_trace.md", "# Process Trace\n\nroute: deep-research\nphase: smoke\nagent: source_scout_smoke")
    write_text(
        root / "notes" / "research_brief.md",
        "# Research Brief\n\n"
        "learner_goal: validate workbench\n"
        "primary_confusion: how a compact workbench proves semantic integration\n"
        "success_criteria: chapter, final, and citation audit preserve EL-smoke\n",
    )
    write_text(
        root / "notes" / "research_tree.md",
        "# Research Tree\n\n"
        "node_id: smoke-root\n"
        "question: can the workbench validate semantic integration?\n"
        "status: evidence_ready\n"
        "next_action: promote evidence into model and citation audit\n"
        "stop_condition: EL-smoke supports the model and final merge\n",
    )
    write_text(
        root / "notes" / "source_map.md",
        "# Source Map\n\n"
        "source_id: supplied\n"
        "title: Supplied smoke source\n"
        "source_type: markdown\n"
        "locator: smoke source map\n"
        "access_method: local read\n"
        "read_state: full\n"
        "supports_questions: smoke-root\n"
        "failure_label: none\n",
    )
    write_text(
        root / "notes" / "evidence_ledger.md",
        "# Evidence Ledger\n\n"
        "claim_id: EL-smoke\n"
        "claim: semantic workbench validation needs evidence integration\n"
        "source_ref: supplied\n"
        "locator: smoke source map\n"
        "evidence_type: mechanism\n"
        "confidence: high\n"
        "status: accepted\n"
        "teaching_use: quality_check\n",
    )
    write_text(
        root / "notes" / "knowledge_model.md",
        "# Knowledge Model\n\nlocked: true\ncore_model: workbench completeness\nevidence_ids: EL-smoke\n",
    )
    write_text(
        root / "notes" / "chapter_plan.md",
        "# Chapter Plan\n\n"
        "learner_bottleneck: unclear artifact spine\n"
        "selected_spine: definition -> evidence -> model -> validation\n"
        "precision_anchors: EL-smoke\n\n"
        "chapter_id: 01_overview\n"
        "title: Workbench overview\n"
        "purpose: show how the DeepResearch sample proves semantic integration\n"
        "input_refs: notes/knowledge_model.md, notes/evidence_ledger.md\n"
        "required_anchors: EL-smoke, locked knowledge model, citation audit support state\n"
        "output_path: chapters/01_overview.md\n"
        "completion_criteria: chapter references evidence, model, and citation audit\n",
    )
    write_text(
        root / "notes" / "integrator_decisions.md",
        "# Integrator Decisions\n\n"
        "promotion_id: smoke\n"
        "source_artifact: notes/agent_outputs/source_scout/sample.md\n"
        "promoted_to: notes/source_map.md\n"
        "result: accepted\n\n"
        "promotion_id: smoke-chapter\n"
        "source_artifact: notes/agent_outputs/teaching_composer/01_overview/sample.md\n"
        "promoted_to: chapters/01_overview.md\n"
        "source_section_id: 01_overview\n"
        "result: accepted\n",
    )
    write_text(
        root / "notes" / "citation_audit.md",
        "# Citation Audit\n\n"
        "claim_or_section: chapters/01_overview.md\n"
        "evidence_ids: EL-smoke\n"
        "source_ids: supplied\n"
        "locator_check: source_map has supplied source\n"
        "support_state: supported\n"
        "integrator_action: accept\n",
    )
    write_text(root / "notes" / "continuation_map.md", "# Continuation Map\n\nbranch_id: next")
    write_text(
        root / "notes" / "agent_outputs" / "source_scout" / "sample.md",
        "## Agent Output: source_scout_smoke\n\n"
        "agent_id: source_scout_smoke\n"
        "agent_type: source_scout\n"
        "mission: validate sample\n\n"
        "### Trace Update\n\n"
        "agent_id: source_scout_smoke\n"
        "artifacts_read: notes/research_brief.md\n"
        "artifacts_written: notes/agent_outputs/source_scout/sample.md\n"
        "canonical_targets: notes/source_map.md\n"
        "strong_findings: EL-smoke\n"
        "open_branches: none\n"
        "handoff_suggestion: integrator\n",
    )
    write_text(
        root / "notes" / "agent_outputs" / "teaching_composer" / "01_overview" / "sample.md",
        "agent_id: teaching_composer_01_overview\n"
        "agent_type: teaching_composer\n"
        "mission: draft the assigned smoke chapter\n"
        "input_artifacts: notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md\n"
        "output_targets: chapters/01_overview.md\n\n"
        "evidence_ids_used: EL-smoke\n"
        "required_anchors_covered: EL-smoke, locked knowledge model, citation audit support state\n"
        "required_anchors_omitted: none\n"
        "integrator_action: accept\n\n"
        "canonical_promotion_hints:\n"
        "  promote_to: chapters/01_overview.md\n"
        "  sections_or_entries: 01_overview\n"
        "  edits_needed: integrator review\n"
        "trace_update:\n"
        "  artifacts_read: notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md\n"
        "  artifacts_written: notes/agent_outputs/teaching_composer/01_overview/sample.md\n"
        "  canonical_targets: chapters/01_overview.md\n"
        "  strong_findings: EL-smoke\n"
        "  open_branches: none\n"
        "  handoff_suggestion: integrator\n",
    )


def exercise_deep_research_validator(tmpdir: Path) -> None:
    help_stdout = io.StringIO()
    with contextlib.redirect_stdout(help_stdout):
        try:
            VALIDATOR.main(["--help"])
        except SystemExit as exc:
            if exc.code not in (0, None):
                raise AssertionError("validator --help should exit cleanly") from exc
    help_text = help_stdout.getvalue()
    if "--root" not in help_text or "--json" not in help_text:
        raise AssertionError("validator help should mention --root and --json")

    sample = tmpdir / "deep-research-smoke"
    build_deep_research_sample(sample)
    json_stdout = io.StringIO()
    with contextlib.redirect_stdout(json_stdout):
        code = VALIDATOR.main(["--root", str(sample), "--json"])
    payload = json.loads(json_stdout.getvalue())
    if code != 0 or not payload["ok"]:
        raise AssertionError("deep-research validator should accept the smoke sample")
    if not {"notes/research_tree.md", "notes/citation_audit.md"}.issubset(set(payload["present"])):
        raise AssertionError("deep-research validator should require research tree and citation audit")
    if payload["evidence_ids"] != ["EL-smoke"]:
        raise AssertionError("deep-research validator should report evidence semantics")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        exercise_prep_templates(tmpdir)
        exercise_deep_research_validator(tmpdir)
    print("SMOKE_TEST ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
