#!/usr/bin/env python3
"""Smoke-test master-zhuyan helper scripts without requiring external services."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
LEARNING_PATH = ROOT / "scripts" / "learning_artifacts.py"
TOPIC_PATH = ROOT / "scripts" / "topic_research.py"
PREP_PATH = ROOT / "scripts" / "prep_template.py"
JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


LEARNING = load_module("mz_learning_artifacts", LEARNING_PATH)
TOPIC = load_module("mz_topic_research", TOPIC_PATH)
PREP = load_module("mz_prep_template", PREP_PATH)


def read_contract(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = JSON_BLOCK_RE.search(text)
    if not match:
        raise AssertionError(f"missing json block in {path}")
    return json.loads(match.group(1)), text[match.end():].lstrip("\n")


def write_contract(path: Path, payload: dict, body: str = "# Draft\n") -> None:
    path.write_text(
        "```json\n" + json.dumps(payload, indent=2, ensure_ascii=False) + "\n```\n\n" + body,
        encoding="utf-8",
    )


def exercise_learning_artifacts(tmpdir: Path) -> None:
    LEARNING.command_init_card(SimpleNamespace(topic="osmosis", out=str(tmpdir)))
    card = tmpdir / "knowledge_card.md"
    payload, body = read_contract(card)
    payload.update(
        {
            "learner_goal": "explain osmosis as a transferable model.",
            "core_model": "water moves across a semipermeable membrane toward the side with higher effective solute pressure.",
            "anchor_example": "a raisin swells in water because water enters through semipermeable membranes.",
            "key_boundaries": ["requires a semipermeable barrier"],
            "misconceptions": ["water always moves toward the side with more water"],
            "retrieval_hooks": ["what barrier and gradient make osmosis happen?"],
            "expansion_links": ["tonicity"],
            "provenance": {"source_facts": [], "teacher_framing": ["raisin anchor"]},
            "status": "draft",
        }
    )
    write_contract(card, payload, body)
    LEARNING.command_validate_card(SimpleNamespace(path=str(card)))
    rendered = LEARNING.render_card(payload)
    if "# osmosis" not in rendered.lower() or "retrieval hooks" not in rendered.lower():
        raise AssertionError("render-card smoke output missing expected sections")

    LEARNING.command_init_report(
        SimpleNamespace(topic="hyponatremia", out=str(tmpdir), kernel="medicine", explanatory_type="mechanism")
    )
    report = tmpdir / "study_report.md"
    payload, body = read_contract(report)
    payload.update(
        {
            "learner_goal": "reason through a dense medical concept without losing branches.",
            "core_model": "a report links the defining disturbance to signs, tests, treatment logic, and avoidable errors.",
            "reasoning_chain": [
                {"step": "start from the defining disturbance", "observable_consequence": "branches become predictable"}
            ],
            "load_bearing_branches": [
                {
                    "kernel_item": item,
                    "title": item,
                    "explanation": f"explanation for {item}.",
                    "boundary_or_failure_mode": f"boundary for {item}.",
                }
                for item in payload["coverage_kernel"]
            ],
            "key_boundaries": [],
            "misconceptions": [],
            "retrieval_hooks": ["can the core model reconstruct every branch?"],
            "source_notes": [],
            "status": "draft",
        }
    )
    write_contract(report, payload, body)
    LEARNING.command_validate_report(SimpleNamespace(path=str(report)))

    cjk_dir = tmpdir / "cjk-learning"
    LEARNING.command_init_report(SimpleNamespace(topic="高钙血症", out=str(cjk_dir), kernel="generic", explanatory_type="mixed"))
    cjk_payload, _ = read_contract(cjk_dir / "study_report.md")
    if cjk_payload["slug"] != "高钙血症":
        raise AssertionError("learning_artifacts slugify should preserve CJK topic text")


def exercise_topic_research(tmpdir: Path) -> None:
    run_dir = tmpdir / "deep"
    TOPIC.command_init_tree(SimpleNamespace(topic="sample topic", out=str(run_dir)))

    brief = run_dir / "framing_brief.md"
    brief_payload, brief_body = read_contract(brief)
    brief_payload.update(
        {
            "expert_identity": "conceptual teacher",
            "learner_goal": "reason about the sample topic",
            "primary_confusion": "what core model organizes the topic",
            "entry_point": "start from the named concept",
            "research_plan": "check the core model, one example, and one boundary",
            "source_strategy": "stable conceptual sources are enough for this smoke test",
            "success_criteria": "the learner can explain one example and one boundary",
        }
    )
    write_contract(brief, brief_payload, brief_body)

    tree = run_dir / "tree.md"
    payload, body = read_contract(tree)
    payload["nodes"] = [
        {
            "node_id": "root",
            "title": "root",
            "question": "what is the core model?",
            "source_tier": "stable",
            "priority": "load-bearing",
            "stop_condition": "covered when the core model has one example and one boundary.",
            "prerequisites": [],
            "status": "pending",
            "owner": "",
            "skip_reason": "",
        }
    ]
    write_contract(tree, payload, body)
    TOPIC.command_validate_tree(SimpleNamespace(tree=str(tree)))

    cjk_run = tmpdir / "deep-cjk"
    TOPIC.command_init_tree(SimpleNamespace(topic="高钙血症", out=str(cjk_run)))
    cjk_tree, _ = read_contract(cjk_run / "tree.md")
    if cjk_tree["slug"] != "高钙血症":
        raise AssertionError("topic_research slugify should preserve CJK topic text")


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


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        exercise_learning_artifacts(tmpdir)
        exercise_topic_research(tmpdir)
        exercise_prep_templates(tmpdir)
    print("SMOKE_TEST ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
