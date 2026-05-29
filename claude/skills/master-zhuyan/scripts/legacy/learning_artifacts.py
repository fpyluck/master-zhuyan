#!/usr/bin/env python3
"""Legacy helper for knowledge-card and study-report mechanics.

This script is not a MasterZhuyan delivery route. Write useful output as a
fallback/proposed artifact for DeepResearch notes such as notes/knowledge_model.md,
notes/chapter_plan.md, or validation notes; canonical use waits for an
integrator promotion, revision, or discard decision.
"""

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


CARD_STATUS_VALUES = {"draft", "reviewed", "stable"}
MAP_STATUS_VALUES = {"draft", "reviewed", "stable"}
REPORT_STATUS_VALUES = {"draft", "reviewed", "stable"}
EXPLANATORY_TYPES = {
    "mechanism",
    "formula",
    "process",
    "system",
    "decision",
    "argument",
    "classification",
    "procedure",
    "mixed",
}
NODE_PRIORITIES = {"load-bearing", "supporting", "optional"}
NODE_STATUSES = {"pending", "explored", "skipped"}
MARKDOWN_JSON_RE = re.compile(r"```json\s*\r?\n(.*?)\r?\n```", re.DOTALL)

CARD_FIELDS = [
    "topic", "slug", "created", "learner_goal", "core_model", "anchor_example",
    "key_boundaries", "misconceptions", "retrieval_hooks", "expansion_links",
    "provenance", "status",
]
MAP_FIELDS = [
    "topic", "slug", "created", "start_node", "nodes", "edges",
    "open_questions", "next_steps", "status",
]
REPORT_FIELDS = [
    "topic", "slug", "created", "learner_goal", "explanatory_type",
    "coverage_kernel", "core_model", "reasoning_chain", "load_bearing_branches",
    "key_boundaries", "misconceptions", "retrieval_hooks", "source_notes",
    "status",
]
NODE_FIELDS = ["node_id", "title", "question", "relation", "priority", "status"]
EDGE_FIELDS = ["source", "target", "relation"]
REASONING_STEP_FIELDS = ["step", "observable_consequence"]
REPORT_BRANCH_FIELDS = ["kernel_item", "title", "explanation", "boundary_or_failure_mode"]

KERNEL_PRESETS = {
    "generic": ["core model", "reasoning chain", "load-bearing branches", "boundaries"],
    "medicine": ["what it is", "why it happens", "how it presents", "how you tell", "how you treat", "what to avoid"],
    "formula": ["definition", "variables", "worked example", "interpretation boundary", "common confusion"],
    "process": ["goal", "stages", "decision points", "failure modes", "recovery checks"],
    "system": ["components", "feedback loops", "dependencies", "observability", "failure modes"],
    "decision": ["triggering condition", "criteria", "options", "tradeoffs", "exceptions"],
    "classification": ["category purpose", "distinguishing axes", "types", "borderline cases", "misclassification risk"],
    "procedure": ["goal", "prerequisites", "steps", "common failure", "recovery or check"],
    "argument": ["claim", "evidence", "context", "strongest objection", "better reading or boundary"],
}


class ValidationError(Exception):
    def __init__(self, check, code, message, *, path=None):
        super().__init__(message)
        self.check = check
        self.code = code
        self.message = message
        self.path = str(path) if path else ""


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(text):
    normalized = unicodedata.normalize("NFKD", text)
    slug = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", normalized.lower()).strip("-")
    if slug:
        return slug
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"topic-{timestamp}"


def fail(check, code, message, *, path=None):
    raise ValidationError(check, code, message, path=path)


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def write_text(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")


def split_markdown_json(text):
    match = MARKDOWN_JSON_RE.search(text)
    if not match:
        return None, text
    payload = json.loads(match.group(1))
    remainder = text[match.end():].lstrip("\r\n")
    return payload, remainder


def read_markdown_contract(path, check, code):
    try:
        payload, body = split_markdown_json(read_text(path))
    except FileNotFoundError:
        fail(check, code, f"Missing file: {path}", path=path)
    except json.JSONDecodeError as exc:
        fail(check, code, f"Invalid JSON block in {path}: {exc}", path=path)
    if payload is None:
        fail(check, code, f"Missing first fenced JSON block in {path}", path=path)
    return payload, body


def write_markdown_contract(path, payload, body=""):
    block = "```json\n" + json.dumps(payload, indent=2, ensure_ascii=False) + "\n```"
    if body and not body.startswith("\n"):
        content = block + "\n\n" + body.rstrip() + "\n"
    elif body:
        content = block + body
    else:
        content = block + "\n"
    write_text(path, content)


def require_keys(obj, required, check, code, *, path):
    missing = [key for key in required if key not in obj]
    if missing:
        fail(check, code, f"Missing required fields {missing} in {path}", path=path)


def require_non_empty_string(value, field_name, check, code, *, path):
    if not isinstance(value, str) or not value.strip():
        fail(check, code, f"Field '{field_name}' must be a non-empty string in {path}", path=path)


def require_enum(value, field_name, allowed, check, code, *, path):
    if value not in allowed:
        fail(check, code, f"Field '{field_name}' must be one of {sorted(allowed)} in {path}", path=path)


def require_list(value, field_name, check, code, *, path):
    if not isinstance(value, list):
        fail(check, code, f"Field '{field_name}' must be a list in {path}", path=path)


def validate_card_document(card, card_path):
    path = Path(card_path)
    require_keys(card, CARD_FIELDS, "CARD_CHECK", "CARD_INCOMPLETE", path=path)
    for field_name in ["topic", "slug", "created", "learner_goal", "core_model", "anchor_example"]:
        require_non_empty_string(card[field_name], field_name, "CARD_CHECK", "CARD_INCOMPLETE", path=path)
    for field_name in ["key_boundaries", "misconceptions", "retrieval_hooks", "expansion_links"]:
        require_list(card[field_name], field_name, "CARD_CHECK", "CARD_INCOMPLETE", path=path)
    if not card["retrieval_hooks"]:
        fail("CARD_CHECK", "CARD_INCOMPLETE", f"Field 'retrieval_hooks' must be a non-empty list in {path}", path=path)
    require_enum(card["status"], "status", CARD_STATUS_VALUES, "CARD_CHECK", "CARD_INCOMPLETE", path=path)
    provenance = card["provenance"]
    if not isinstance(provenance, dict):
        fail("CARD_CHECK", "CARD_INCOMPLETE", f"Field 'provenance' must be an object in {path}", path=path)
    for prov_field in ["source_facts", "teacher_framing"]:
        if prov_field not in provenance:
            fail("CARD_CHECK", "CARD_INCOMPLETE", f"provenance missing required field '{prov_field}' in {path}", path=path)
        require_list(provenance[prov_field], f"provenance.{prov_field}", "CARD_CHECK", "CARD_INCOMPLETE", path=path)


def validate_map_document(map_data, map_path):
    path = Path(map_path)
    require_keys(map_data, MAP_FIELDS, "MAP_CHECK", "MAP_INCOMPLETE", path=path)
    for field_name in ["topic", "slug", "created", "start_node"]:
        require_non_empty_string(map_data[field_name], field_name, "MAP_CHECK", "MAP_INCOMPLETE", path=path)
    for field_name in ["nodes", "edges", "open_questions", "next_steps"]:
        require_list(map_data[field_name], field_name, "MAP_CHECK", "MAP_INCOMPLETE", path=path)
    require_enum(map_data["status"], "status", MAP_STATUS_VALUES, "MAP_CHECK", "MAP_INCOMPLETE", path=path)
    if not map_data["nodes"]:
        fail("MAP_CHECK", "MAP_INCOMPLETE", f"Map must contain at least one node in {path}", path=path)
    node_ids = set()
    for node in map_data["nodes"]:
        require_keys(node, NODE_FIELDS, "MAP_CHECK", "MAP_INCOMPLETE", path=path)
        node_id = node["node_id"]
        require_non_empty_string(node_id, "node_id", "MAP_CHECK", "MAP_INCOMPLETE", path=path)
        if node_id in node_ids:
            fail("MAP_CHECK", "MAP_INCOMPLETE", f"Duplicate node_id '{node_id}' in {path}", path=path)
        node_ids.add(node_id)
        require_non_empty_string(node["title"], "title", "MAP_CHECK", "MAP_INCOMPLETE", path=path)
        require_non_empty_string(node["question"], "question", "MAP_CHECK", "MAP_INCOMPLETE", path=path)
        require_non_empty_string(node["relation"], "relation", "MAP_CHECK", "MAP_INCOMPLETE", path=path)
        require_enum(node["priority"], "priority", NODE_PRIORITIES, "MAP_CHECK", "MAP_INCOMPLETE", path=path)
        require_enum(node["status"], "status", NODE_STATUSES, "MAP_CHECK", "MAP_INCOMPLETE", path=path)
    if map_data["start_node"] not in node_ids:
        fail("MAP_CHECK", "MAP_INCOMPLETE", f"start_node '{map_data['start_node']}' not found in nodes in {path}", path=path)
    for edge in map_data["edges"]:
        require_keys(edge, EDGE_FIELDS, "MAP_CHECK", "MAP_INCOMPLETE", path=path)
        for endpoint in ["source", "target"]:
            if edge[endpoint] not in node_ids:
                fail("MAP_CHECK", "MAP_INCOMPLETE", f"Edge {endpoint} '{edge[endpoint]}' is not a known node_id in {path}", path=path)
        require_non_empty_string(edge["relation"], "relation", "MAP_CHECK", "MAP_INCOMPLETE", path=path)


def validate_report_document(report, report_path):
    path = Path(report_path)
    require_keys(report, REPORT_FIELDS, "REPORT_CHECK", "REPORT_INCOMPLETE", path=path)
    for field_name in ["topic", "slug", "created", "learner_goal", "core_model"]:
        require_non_empty_string(report[field_name], field_name, "REPORT_CHECK", "REPORT_INCOMPLETE", path=path)
    require_enum(report["explanatory_type"], "explanatory_type", EXPLANATORY_TYPES, "REPORT_CHECK", "REPORT_INCOMPLETE", path=path)
    for field_name in [
        "coverage_kernel",
        "reasoning_chain",
        "load_bearing_branches",
        "key_boundaries",
        "misconceptions",
        "retrieval_hooks",
        "source_notes",
    ]:
        require_list(report[field_name], field_name, "REPORT_CHECK", "REPORT_INCOMPLETE", path=path)
    if not report["coverage_kernel"]:
        fail("REPORT_CHECK", "REPORT_INCOMPLETE", f"Field 'coverage_kernel' must be a non-empty list in {path}", path=path)
    if not report["reasoning_chain"]:
        fail("REPORT_CHECK", "REPORT_INCOMPLETE", f"Field 'reasoning_chain' must be a non-empty list in {path}", path=path)
    if not report["load_bearing_branches"]:
        fail("REPORT_CHECK", "REPORT_INCOMPLETE", f"Field 'load_bearing_branches' must be a non-empty list in {path}", path=path)
    if not report["retrieval_hooks"]:
        fail("REPORT_CHECK", "REPORT_INCOMPLETE", f"Field 'retrieval_hooks' must be a non-empty list in {path}", path=path)
    require_enum(report["status"], "status", REPORT_STATUS_VALUES, "REPORT_CHECK", "REPORT_INCOMPLETE", path=path)

    for index, step in enumerate(report["reasoning_chain"], start=1):
        require_keys(step, REASONING_STEP_FIELDS, "REPORT_CHECK", "REPORT_INCOMPLETE", path=path)
        require_non_empty_string(step["step"], f"reasoning_chain[{index}].step", "REPORT_CHECK", "REPORT_INCOMPLETE", path=path)
        require_non_empty_string(
            step["observable_consequence"],
            f"reasoning_chain[{index}].observable_consequence",
            "REPORT_CHECK",
            "REPORT_INCOMPLETE",
            path=path,
        )

    branch_titles = set()
    for index, branch in enumerate(report["load_bearing_branches"], start=1):
        require_keys(branch, REPORT_BRANCH_FIELDS, "REPORT_CHECK", "REPORT_INCOMPLETE", path=path)
        kernel_item = branch["kernel_item"]
        require_non_empty_string(
            kernel_item,
            f"load_bearing_branches[{index}].kernel_item",
            "REPORT_CHECK",
            "REPORT_INCOMPLETE",
            path=path,
        )
        title = branch["title"]
        require_non_empty_string(title, f"load_bearing_branches[{index}].title", "REPORT_CHECK", "REPORT_INCOMPLETE", path=path)
        require_non_empty_string(
            branch["explanation"],
            f"load_bearing_branches[{index}].explanation",
            "REPORT_CHECK",
            "REPORT_INCOMPLETE",
            path=path,
        )
        require_non_empty_string(
            branch["boundary_or_failure_mode"],
            f"load_bearing_branches[{index}].boundary_or_failure_mode",
            "REPORT_CHECK",
            "REPORT_INCOMPLETE",
            path=path,
        )
        branch_titles.add(kernel_item.strip().lower())

    missing_kernel_branches = [
        item for item in report["coverage_kernel"]
        if isinstance(item, str) and item.strip().lower() not in branch_titles
    ]
    if missing_kernel_branches:
        fail(
            "REPORT_CHECK",
            "REPORT_INCOMPLETE",
            f"Missing load-bearing branch entries for coverage_kernel items {missing_kernel_branches} in {path}",
            path=path,
        )


def command_init_card(args):
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    card_path = out_dir / "knowledge_card.md"
    payload = {
        "topic": args.topic,
        "slug": slugify(args.topic),
        "created": now_iso(),
        "learner_goal": "",
        "core_model": "",
        "anchor_example": "",
        "key_boundaries": [],
        "misconceptions": [],
        "retrieval_hooks": [],
        "expansion_links": [],
        "provenance": {
            "source_facts": [],
            "teacher_framing": [],
        },
        "status": "draft",
    }
    body = (
        "# Knowledge Card\n\n"
        "Fill `learner_goal`, `core_model`, `anchor_example`, and add at least one "
        "`retrieval_hooks` entry before running validate-card.\n"
    )
    write_markdown_contract(card_path, payload, body)
    print(str(card_path))


def command_validate_card(args):
    card_path = Path(args.path)
    card, _ = read_markdown_contract(card_path, "CARD_CHECK", "CARD_INCOMPLETE")
    validate_card_document(card, card_path)
    print(f"CARD_CHECK ok: {card_path.name}")


def command_init_map(args):
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    map_path = out_dir / "expansion_map.md"
    slug = slugify(args.topic)
    root_node_id = slug + "-root"
    payload = {
        "topic": args.topic,
        "slug": slug,
        "created": now_iso(),
        "start_node": root_node_id,
        "nodes": [
            {
                "node_id": root_node_id,
                "title": args.topic,
                "question": "",
                "relation": "root",
                "priority": "load-bearing",
                "status": "pending",
            }
        ],
        "edges": [],
        "open_questions": [],
        "next_steps": [],
        "status": "draft",
    }
    body = (
        "# Expansion Map\n\n"
        "Add nodes for each sub-question and edges to show relationships. "
        "Fill `question` for each node before validating.\n"
    )
    write_markdown_contract(map_path, payload, body)
    print(str(map_path))


def command_validate_map(args):
    map_path = Path(args.path)
    map_data, _ = read_markdown_contract(map_path, "MAP_CHECK", "MAP_INCOMPLETE")
    validate_map_document(map_data, map_path)
    print(f"MAP_CHECK ok: {map_path.name} ({len(map_data['nodes'])} nodes)")


def command_init_report(args):
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "study_report.md"
    slug = slugify(args.topic)
    kernel_key = args.kernel
    coverage_kernel = KERNEL_PRESETS.get(kernel_key, KERNEL_PRESETS["generic"])
    payload = {
        "topic": args.topic,
        "slug": slug,
        "created": now_iso(),
        "learner_goal": "",
        "explanatory_type": args.explanatory_type,
        "coverage_kernel": coverage_kernel,
        "core_model": "",
        "reasoning_chain": [],
        "load_bearing_branches": [
            {
                "kernel_item": title,
                "title": title,
                "explanation": "",
                "boundary_or_failure_mode": "",
            }
            for title in coverage_kernel
        ],
        "key_boundaries": [],
        "misconceptions": [],
        "retrieval_hooks": [],
        "source_notes": [],
        "status": "draft",
    }
    body = (
        "# Study Report\n\n"
        "Fill every `load_bearing_branches` entry, add at least one reasoning step and "
        "retrieval hook, then run validate-report.\n"
    )
    write_markdown_contract(report_path, payload, body)
    print(str(report_path))


def command_validate_report(args):
    report_path = Path(args.path)
    report, _ = read_markdown_contract(report_path, "REPORT_CHECK", "REPORT_INCOMPLETE")
    validate_report_document(report, report_path)
    print(f"REPORT_CHECK ok: {report_path.name} ({len(report['load_bearing_branches'])} branches)")


def command_status(args):
    out_dir = Path(args.dir)
    card_path = out_dir / "knowledge_card.md"
    map_path = out_dir / "expansion_map.md"
    report_path = out_dir / "study_report.md"

    card_exists = card_path.exists()
    map_exists = map_path.exists()
    report_exists = report_path.exists()
    card_valid = False
    map_valid = False
    report_valid = False

    if card_exists:
        try:
            card, _ = read_markdown_contract(card_path, "CARD_CHECK", "CARD_INCOMPLETE")
            validate_card_document(card, card_path)
            card_valid = True
        except Exception:
            pass

    if map_exists:
        try:
            map_data, _ = read_markdown_contract(map_path, "MAP_CHECK", "MAP_INCOMPLETE")
            validate_map_document(map_data, map_path)
            map_valid = True
        except Exception:
            pass

    if report_exists:
        try:
            report, _ = read_markdown_contract(report_path, "REPORT_CHECK", "REPORT_INCOMPLETE")
            validate_report_document(report, report_path)
            report_valid = True
        except Exception:
            pass

    summary = {
        "dir": str(out_dir),
        "knowledge_card": {"exists": card_exists, "valid": card_valid},
        "expansion_map": {"exists": map_exists, "valid": map_valid},
        "study_report": {"exists": report_exists, "valid": report_valid},
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def _list_items(items):
    return "\n".join(f"- {item}" for item in items)


def render_card(card):
    lines = []
    lines.append(f"# {card['topic']}")
    lines.append("")
    lines.append(f"**Status:** {card['status']}  ·  Created: {card['created']}")
    lines.append("")
    lines.append("## Learner Goal")
    lines.append(card["learner_goal"])
    lines.append("")
    lines.append("## Core Model")
    lines.append(card["core_model"])
    lines.append("")
    lines.append("## Anchor Example")
    lines.append(card["anchor_example"])
    lines.append("")
    if card["key_boundaries"]:
        lines.append("## Key Boundaries")
        lines.append(_list_items(card["key_boundaries"]))
        lines.append("")
    lines.append("## Common Misconceptions")
    lines.append(_list_items(card["misconceptions"]) if card["misconceptions"] else "None recorded.")
    lines.append("")
    lines.append("## Retrieval Hooks")
    lines.append(_list_items(card["retrieval_hooks"]))
    lines.append("")
    if card["expansion_links"]:
        lines.append("## Expansion Links")
        lines.append(_list_items(card["expansion_links"]))
        lines.append("")
    prov = card["provenance"]
    prov_lines = []
    if prov["source_facts"]:
        prov_lines.append("**Source facts:**")
        prov_lines.append(_list_items(prov["source_facts"]))
    if prov["teacher_framing"]:
        prov_lines.append("**Teacher framing:**")
        prov_lines.append(_list_items(prov["teacher_framing"]))
    if prov_lines:
        lines.append("## Provenance")
        lines.extend(prov_lines)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


_NODE_STATUS_MARKER = {"pending": " *(pending)*", "skipped": " *(skipped)*", "explored": ""}
_NODE_PRIORITY_ORDER = {"load-bearing": 0, "supporting": 1, "optional": 2}


def render_map(map_data):
    lines = []
    lines.append(f"# {map_data['topic']} — Exploration Map")
    lines.append("")
    lines.append(f"**Status:** {map_data['status']}  ·  Created: {map_data['created']}")
    lines.append("")
    node_by_id = {n["node_id"]: n for n in map_data["nodes"]}
    start_title = node_by_id.get(map_data["start_node"], {}).get("title", map_data["start_node"])
    lines.append(f"**Starting point:** {start_title}")
    lines.append("")
    sorted_nodes = sorted(
        map_data["nodes"],
        key=lambda n: (
            0 if n["node_id"] == map_data["start_node"] else 1,
            _NODE_PRIORITY_ORDER.get(n["priority"], 3),
        ),
    )
    lines.append("## Nodes")
    lines.append("")
    for node in sorted_nodes:
        marker = _NODE_STATUS_MARKER.get(node["status"], "")
        lines.append(f"### {node['title']} ({node['priority']}){marker}")
        lines.append(f"> {node['question']}")
        lines.append(f"Relation: {node['relation']}")
        lines.append("")
    if map_data["edges"]:
        lines.append("## Connections")
        for edge in map_data["edges"]:
            src = node_by_id.get(edge["source"], {}).get("title", edge["source"])
            tgt = node_by_id.get(edge["target"], {}).get("title", edge["target"])
            lines.append(f"- {src} → {tgt}: {edge['relation']}")
        lines.append("")
    if map_data["open_questions"]:
        lines.append("## Open Questions")
        lines.append(_list_items(map_data["open_questions"]))
        lines.append("")
    if map_data["next_steps"]:
        lines.append("## 后续知识拓展")
        lines.append(_list_items(map_data["next_steps"]))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_report(report):
    lines = []
    lines.append(f"# {report['topic']} — Study Report")
    lines.append("")
    lines.append(f"**Status:** {report['status']}  ·  Created: {report['created']}")
    lines.append(f"**Explanatory type:** {report['explanatory_type']}")
    lines.append("")
    lines.append("## Learner Goal")
    lines.append(report["learner_goal"])
    lines.append("")
    lines.append("## Core Model")
    lines.append(report["core_model"])
    lines.append("")
    lines.append("## Reasoning Chain")
    for index, step in enumerate(report["reasoning_chain"], start=1):
        lines.append(f"{index}. {step['step']}")
        lines.append(f"   - Observable consequence: {step['observable_consequence']}")
    lines.append("")
    lines.append("## Load-Bearing Branches")
    for branch in report["load_bearing_branches"]:
        lines.append(f"### {branch['title']}")
        if branch["title"].strip().lower() != branch["kernel_item"].strip().lower():
            lines.append(f"*Kernel item: {branch['kernel_item']}*")
            lines.append("")
        lines.append(branch["explanation"])
        lines.append("")
        lines.append(f"Boundary or repair focus: {branch['boundary_or_failure_mode']}")
        lines.append("")
    if report["key_boundaries"]:
        lines.append("## Key Boundaries")
        lines.append(_list_items(report["key_boundaries"]))
        lines.append("")
    lines.append("## Common Misconceptions")
    lines.append(_list_items(report["misconceptions"]) if report["misconceptions"] else "None recorded.")
    lines.append("")
    lines.append("## Retrieval Hooks")
    lines.append(_list_items(report["retrieval_hooks"]))
    lines.append("")
    if report["source_notes"]:
        lines.append("## Source Notes")
        lines.append(_list_items(report["source_notes"]))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def command_render_card(args):
    card_path = Path(args.path)
    card, _ = read_markdown_contract(card_path, "CARD_CHECK", "CARD_INCOMPLETE")
    validate_card_document(card, card_path)
    rendered = render_card(card)
    if args.out:
        write_text(args.out, rendered)
    else:
        print(rendered, end="")


def command_render_map(args):
    map_path = Path(args.path)
    map_data, _ = read_markdown_contract(map_path, "MAP_CHECK", "MAP_INCOMPLETE")
    validate_map_document(map_data, map_path)
    rendered = render_map(map_data)
    if args.out:
        write_text(args.out, rendered)
    else:
        print(rendered, end="")


def command_render_report(args):
    report_path = Path(args.path)
    report, _ = read_markdown_contract(report_path, "REPORT_CHECK", "REPORT_INCOMPLETE")
    validate_report_document(report, report_path)
    rendered = render_report(report)
    if args.out:
        write_text(args.out, rendered)
    else:
        print(rendered, end="")


def build_parser():
    parser = argparse.ArgumentParser(description="5.26 fallback helper for knowledge artifact mechanics.")
    parser.add_argument(
        "--allow-legacy-helper",
        action="store_true",
        help="Acknowledge this legacy helper is not a MasterZhuyan delivery route.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_card = subparsers.add_parser("init-card", help="Initialize a knowledge card.")
    init_card.add_argument("--topic", required=True)
    init_card.add_argument("--out", required=True)
    init_card.set_defaults(func=command_init_card)

    validate_card = subparsers.add_parser("validate-card", help="Validate a knowledge card.")
    validate_card.add_argument("path")
    validate_card.set_defaults(func=command_validate_card)

    init_map = subparsers.add_parser("init-map", help="Initialize an expansion map.")
    init_map.add_argument("--topic", required=True)
    init_map.add_argument("--out", required=True)
    init_map.set_defaults(func=command_init_map)

    validate_map = subparsers.add_parser("validate-map", help="Validate an expansion map.")
    validate_map.add_argument("path")
    validate_map.set_defaults(func=command_validate_map)

    init_report = subparsers.add_parser("init-report", help="Initialize a study report.")
    init_report.add_argument("--topic", required=True)
    init_report.add_argument("--out", required=True)
    init_report.add_argument("--explanatory-type", default="mixed", choices=sorted(EXPLANATORY_TYPES))
    init_report.add_argument("--kernel", default="generic", choices=sorted(KERNEL_PRESETS.keys()))
    init_report.set_defaults(func=command_init_report)

    validate_report = subparsers.add_parser("validate-report", help="Validate a study report.")
    validate_report.add_argument("path")
    validate_report.set_defaults(func=command_validate_report)

    status = subparsers.add_parser("status", help="Show card and map status for a directory.")
    status.add_argument("dir")
    status.set_defaults(func=command_status)

    render_card_p = subparsers.add_parser("render-card", help="Render a knowledge card as a wiki-style Markdown page.")
    render_card_p.add_argument("path")
    render_card_p.add_argument("--out", default=None, help="Write rendered output to a sidecar/proposed path.")
    render_card_p.set_defaults(func=command_render_card)

    render_map_p = subparsers.add_parser("render-map", help="Render an expansion map as a readable Markdown page.")
    render_map_p.add_argument("path")
    render_map_p.add_argument("--out", default=None, help="Write rendered output to a sidecar/proposed path.")
    render_map_p.set_defaults(func=command_render_map)

    render_report_p = subparsers.add_parser("render-report", help="Render a study report as a readable Markdown page.")
    render_report_p.add_argument("path")
    render_report_p.add_argument("--out", default=None, help="Write rendered output to a sidecar/proposed path.")
    render_report_p.set_defaults(func=command_render_report)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.allow_legacy_helper:
        print(
            "LEGACY_HELPER_DISABLED: use canonical AgenticResearch notes; pass --allow-legacy-helper only for 5.26 fallback or migration mechanics.",
            file=sys.stderr,
        )
        return 2
    try:
        args.func(args)
    except ValidationError as error:
        print(f"{error.check} {error.code}: {error.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
