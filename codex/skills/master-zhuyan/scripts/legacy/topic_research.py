#!/usr/bin/env python3
"""Legacy helper for tree, dispatch, and traceability mechanics.

This script is not a MasterZhuyan delivery route. Write useful output as a
fallback/proposed artifact for DeepResearch notes such as notes/research_tree.md,
notes/source_map.md, notes/evidence_ledger.md, or notes/integrator_decisions.md;
canonical use waits for an integrator promotion, revision, or discard decision.
"""

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path


SOURCE_TIERS = {"stable", "current", "primary", "secondary", "user-provided", "web"}
NODE_PRIORITIES = {"load-bearing", "supporting", "optional"}
NODE_STATUSES = {"pending", "dispatched", "complete", "skipped"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
MARKDOWN_JSON_RE = re.compile(r"```json\s*\r?\n(.*?)\r?\n```", re.DOTALL)
ALIGNMENT_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "before",
    "but",
    "can",
    "for",
    "from",
    "how",
    "is",
    "it",
    "of",
    "one",
    "or",
    "the",
    "to",
    "with",
    "why",
    "该",
    "的",
    "了",
    "和",
    "或",
    "与",
}
FRAMING_FIELDS = [
    "topic",
    "expert_identity",
    "learner_goal",
    "primary_confusion",
    "entry_point",
    "research_plan",
    "source_strategy",
    "success_criteria",
]
VAGUE_STOP_CONDITIONS = {
    "research thoroughly",
    "understand enough",
    "cover comprehensively",
    "learn enough",
}
RECOVERY_HINTS = {
    "SCOPE_TOO_BROAD": "Ask one narrowing question before creating or dispatching the tree.",
    "FRAMING_INCOMPLETE": "Complete the framing brief fields, ensure its topic matches tree.md, then rerun validate-tree.",
    "TREE_INCOMPLETE": "Fill the missing or invalid tree field, then rerun validate-tree.",
    "STOP_CONDITION_VAGUE": "Rewrite the stop_condition as a falsifiable condition that can be checked against an artifact.",
    "PREREQUISITE_CYCLE": "Split or reorder nodes so prerequisites form an acyclic learning path.",
    "DISPATCH_ORPHAN": "Fix dispatch.md so every row maps to a non-skipped tree node with owner, budget, dispatched status, and expected artifact path.",
    "ARTIFACT_INCOMPLETE": "Return the artifact to the Researcher with the missing fields or malformed traceability called out.",
    "SCOPE_NOT_CONFIRMED": "Retry with a narrower scope, split the node, or mark it skipped in tree.md with a reason.",
    "CLAIM_UNTRACEABLE": "Add the missing source entry, include the source in evidence, or remove the unsupported claim.",
    "SYNTHESIS_UNCOVERED": "Complete, skip, or split the affected node and regenerate synthesis before teaching.",
    "GAP_DROPPED": "Restore dropped gaps or contradictions in synthesis before teaching.",
}


class ValidationError(Exception):
    def __init__(self, check, code, message, *, run_dir=None, path=None, node_id=None):
        super().__init__(message)
        self.check = check
        self.code = code
        self.message = message
        self.run_dir = Path(run_dir) if run_dir else None
        self.path = str(path) if path else ""
        self.node_id = node_id or ""


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(text):
    normalized = unicodedata.normalize("NFKD", text)
    slug = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", normalized.lower()).strip("-")
    if slug:
        return slug
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"topic-{timestamp}"


def normalize_space(text):
    return re.sub(r"\s+", " ", text.strip())


def is_vague_stop_condition(text):
    cleaned = normalize_space(text).lower()
    if not cleaned:
        return False
    if cleaned in VAGUE_STOP_CONDITIONS:
        return True
    if cleaned.startswith("covered when ") and cleaned.endswith("etc"):
        return True
    if cleaned in {"tbd", "todo", "n/a"}:
        return True
    return False


def fail(check, code, message, *, run_dir=None, path=None, node_id=None):
    raise ValidationError(check, code, message, run_dir=run_dir, path=path, node_id=node_id)


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


def read_markdown_contract(path, check, code, *, run_dir=None, node_id=None):
    try:
        payload, body = split_markdown_json(read_text(path))
    except FileNotFoundError:
        fail(check, code, f"Missing file: {path}", run_dir=run_dir, path=path, node_id=node_id)
    except json.JSONDecodeError as exc:
        fail(
            check,
            code,
            f"Invalid JSON block in {path}: {exc}",
            run_dir=run_dir,
            path=path,
            node_id=node_id,
        )
    if payload is None:
        fail(check, code, f"Missing first fenced JSON block in {path}", run_dir=run_dir, path=path, node_id=node_id)
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


def load_tree(tree_path):
    tree_path = Path(tree_path)
    tree, body = read_markdown_contract(
        tree_path,
        "TREE_CHECK",
        "TREE_INCOMPLETE",
        run_dir=tree_path.parent,
        node_id="",
    )
    return tree, body


def validate_framing_brief_document(framing, framing_path, *, expected_topic=""):
    run_dir = framing_path.parent
    require_keys(
        framing,
        FRAMING_FIELDS,
        "TOPIC_CHECK",
        "FRAMING_INCOMPLETE",
        run_dir=run_dir,
        path=framing_path,
    )
    for field_name in FRAMING_FIELDS:
        require_non_empty_string(
            framing[field_name],
            field_name,
            "TOPIC_CHECK",
            "FRAMING_INCOMPLETE",
            run_dir=run_dir,
            path=framing_path,
        )
    if expected_topic and framing["topic"] != expected_topic:
        fail(
            "TOPIC_CHECK",
            "FRAMING_INCOMPLETE",
            "framing_brief.md topic must match tree.md topic",
            run_dir=run_dir,
            path=framing_path,
        )


def load_valid_framing_brief(run_dir, *, expected_topic=""):
    framing_path = Path(run_dir) / "framing_brief.md"
    framing, body = read_markdown_contract(
        framing_path,
        "TOPIC_CHECK",
        "FRAMING_INCOMPLETE",
        run_dir=run_dir,
    )
    validate_framing_brief_document(framing, framing_path, expected_topic=expected_topic)
    return framing, body


def require_keys(obj, required, check, code, *, run_dir, path, node_id=""):
    missing = [key for key in required if key not in obj]
    if missing:
        fail(
            check,
            code,
            f"Missing required fields {missing} in {path}",
            run_dir=run_dir,
            path=path,
            node_id=node_id,
        )


def require_non_empty_string(value, field_name, check, code, *, run_dir, path, node_id=""):
    if not isinstance(value, str) or not value.strip():
        fail(
            check,
            code,
            f"Field '{field_name}' must be a non-empty string in {path}",
            run_dir=run_dir,
            path=path,
            node_id=node_id,
        )


def require_enum(value, field_name, allowed, check, code, *, run_dir, path, node_id=""):
    if value not in allowed:
        fail(
            check,
            code,
            f"Field '{field_name}' must be one of {sorted(allowed)} in {path}",
            run_dir=run_dir,
            path=path,
            node_id=node_id,
        )


def require_list(value, field_name, check, code, *, run_dir, path, node_id=""):
    if not isinstance(value, list):
        fail(
            check,
            code,
            f"Field '{field_name}' must be a list in {path}",
            run_dir=run_dir,
            path=path,
            node_id=node_id,
        )


def require_non_empty_string_list(value, field_name, check, code, *, run_dir, path, node_id=""):
    require_list(value, field_name, check, code, run_dir=run_dir, path=path, node_id=node_id)
    if not value:
        fail(
            check,
            code,
            f"Field '{field_name}' must be a non-empty list in {path}",
            run_dir=run_dir,
            path=path,
            node_id=node_id,
        )
    for index, item in enumerate(value, start=1):
        require_non_empty_string(item, f"{field_name}[{index}]", check, code, run_dir=run_dir, path=path, node_id=node_id)


def alignment_tokens(text):
    tokens = set()
    for token in re.findall(r"[A-Za-z0-9\u4e00-\u9fff][A-Za-z0-9\u4e00-\u9fff-]*", text.lower()):
        cleaned = token.strip("-")
        if len(cleaned) < 3 or cleaned in ALIGNMENT_STOPWORDS:
            continue
        tokens.add(cleaned)
    return tokens


def framing_alignment_terms(framing):
    text = f"{framing.get('success_criteria', '')} {framing.get('primary_confusion', '')}"
    return alignment_tokens(text)


def text_aligns_with_framing(text, framing_terms):
    return bool(alignment_tokens(text) & framing_terms)


def artifact_aligns_with_framing(artifact, framing_terms):
    if text_aligns_with_framing(artifact.get("scope_evidence", ""), framing_terms):
        return True
    for claim in artifact.get("claims", []):
        if text_aligns_with_framing(claim.get("claim", ""), framing_terms):
            return True
    return False


def topo_sort(nodes):
    node_order = {node["node_id"]: index for index, node in enumerate(nodes)}
    indegree = {node["node_id"]: 0 for node in nodes}
    edges = defaultdict(list)
    for node in nodes:
        for prereq in node["prerequisites"]:
            edges[prereq].append(node["node_id"])
            indegree[node["node_id"]] += 1
    queue = deque(sorted([node_id for node_id, count in indegree.items() if count == 0], key=node_order.get))
    ordered = []
    while queue:
        current = queue.popleft()
        ordered.append(current)
        for neighbor in sorted(edges[current], key=node_order.get):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(ordered) != len(nodes):
        return None
    return ordered


def validate_tree_document(tree, tree_path):
    run_dir = tree_path.parent
    require_keys(tree, ["topic", "slug", "created", "nodes"], "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path)
    require_non_empty_string(tree["topic"], "topic", "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path)
    require_non_empty_string(tree["slug"], "slug", "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path)
    require_non_empty_string(tree["created"], "created", "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path)
    load_valid_framing_brief(run_dir, expected_topic=tree["topic"])
    require_list(tree["nodes"], "nodes", "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path)
    if not tree["nodes"]:
        fail("TREE_CHECK", "TREE_INCOMPLETE", "tree.md must contain at least one node", run_dir=run_dir, path=tree_path)

    node_ids = set()
    for node in tree["nodes"]:
        require_keys(
            node,
            [
                "node_id",
                "title",
                "question",
                "source_tier",
                "priority",
                "stop_condition",
                "prerequisites",
                "status",
                "owner",
                "skip_reason",
            ],
            "TREE_CHECK",
            "TREE_INCOMPLETE",
            run_dir=run_dir,
            path=tree_path,
        )
        node_id = node["node_id"]
        require_non_empty_string(node_id, "node_id", "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path)
        if node_id in node_ids:
            fail("TREE_CHECK", "TREE_INCOMPLETE", f"Duplicate node_id '{node_id}' in tree.md", run_dir=run_dir, path=tree_path, node_id=node_id)
        node_ids.add(node_id)
        require_non_empty_string(node["title"], "title", "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path, node_id=node_id)
        require_non_empty_string(node["question"], "question", "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path, node_id=node_id)
        require_enum(node["source_tier"], "source_tier", SOURCE_TIERS, "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path, node_id=node_id)
        require_enum(node["priority"], "priority", NODE_PRIORITIES, "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path, node_id=node_id)
        require_enum(node["status"], "status", NODE_STATUSES, "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path, node_id=node_id)
        require_list(node["prerequisites"], "prerequisites", "TREE_CHECK", "TREE_INCOMPLETE", run_dir=run_dir, path=tree_path, node_id=node_id)
        if not isinstance(node["owner"], str):
            fail("TREE_CHECK", "TREE_INCOMPLETE", f"Field 'owner' must be a string for node '{node_id}'", run_dir=run_dir, path=tree_path, node_id=node_id)
        if not isinstance(node["skip_reason"], str):
            fail("TREE_CHECK", "TREE_INCOMPLETE", f"Field 'skip_reason' must be a string for node '{node_id}'", run_dir=run_dir, path=tree_path, node_id=node_id)
        stop_condition = node["stop_condition"]
        if not isinstance(stop_condition, str) or not stop_condition.strip():
            fail(
                "TREE_CHECK",
                "TREE_INCOMPLETE",
                f"Node '{node_id}' is missing a non-empty stop_condition",
                run_dir=run_dir,
                path=tree_path,
                node_id=node_id,
            )
        if is_vague_stop_condition(stop_condition):
            fail(
                "TREE_CHECK",
                "STOP_CONDITION_VAGUE",
                f"Node '{node_id}' has a vague stop_condition",
                run_dir=run_dir,
                path=tree_path,
                node_id=node_id,
            )
        if node["status"] == "skipped" and not node["skip_reason"].strip():
            fail(
                "TREE_CHECK",
                "TREE_INCOMPLETE",
                f"Skipped node '{node_id}' must include skip_reason",
                run_dir=run_dir,
                path=tree_path,
                node_id=node_id,
            )
        if node["status"] != "skipped" and node["skip_reason"].strip():
            fail(
                "TREE_CHECK",
                "TREE_INCOMPLETE",
                f"Only skipped nodes may include skip_reason (node '{node_id}')",
                run_dir=run_dir,
                path=tree_path,
                node_id=node_id,
            )

    for node in tree["nodes"]:
        node_id = node["node_id"]
        for prereq in node["prerequisites"]:
            if prereq not in node_ids:
                fail(
                    "TREE_CHECK",
                    "TREE_INCOMPLETE",
                    f"Node '{node_id}' references missing prerequisite '{prereq}'",
                    run_dir=run_dir,
                    path=tree_path,
                    node_id=node_id,
                )

    if topo_sort(tree["nodes"]) is None:
        fail("TREE_CHECK", "PREREQUISITE_CYCLE", "Tree prerequisites contain a cycle", run_dir=run_dir, path=tree_path)


def validate_dispatch_document(dispatch, dispatch_path, tree):
    run_dir = dispatch_path.parent
    require_keys(dispatch, ["dispatch"], "DISPATCH_CHECK", "DISPATCH_ORPHAN", run_dir=run_dir, path=dispatch_path)
    require_list(dispatch["dispatch"], "dispatch", "DISPATCH_CHECK", "DISPATCH_ORPHAN", run_dir=run_dir, path=dispatch_path)
    tree_nodes = {node["node_id"]: node for node in tree["nodes"]}
    seen = set()
    for row in dispatch["dispatch"]:
        require_keys(
            row,
            ["node_id", "owner", "token_budget", "status", "artifact_path"],
            "DISPATCH_CHECK",
            "DISPATCH_ORPHAN",
            run_dir=run_dir,
            path=dispatch_path,
        )
        node_id = row["node_id"]
        if node_id in seen:
            fail("DISPATCH_CHECK", "DISPATCH_ORPHAN", f"Duplicate dispatch row for '{node_id}'", run_dir=run_dir, path=dispatch_path, node_id=node_id)
        seen.add(node_id)
        require_non_empty_string(node_id, "node_id", "DISPATCH_CHECK", "DISPATCH_ORPHAN", run_dir=run_dir, path=dispatch_path, node_id=node_id)
        require_non_empty_string(row["owner"], "owner", "DISPATCH_CHECK", "DISPATCH_ORPHAN", run_dir=run_dir, path=dispatch_path, node_id=node_id)
        if not isinstance(row["token_budget"], int) or row["token_budget"] <= 0:
            fail(
                "DISPATCH_CHECK",
                "DISPATCH_ORPHAN",
                f"token_budget must be a positive integer for '{node_id}'",
                run_dir=run_dir,
                path=dispatch_path,
                node_id=node_id,
            )
        if row["status"] != "dispatched":
            fail(
                "DISPATCH_CHECK",
                "DISPATCH_ORPHAN",
                f"Dispatch row '{node_id}' must have status 'dispatched'",
                run_dir=run_dir,
                path=dispatch_path,
                node_id=node_id,
            )
        require_non_empty_string(row["artifact_path"], "artifact_path", "DISPATCH_CHECK", "DISPATCH_ORPHAN", run_dir=run_dir, path=dispatch_path, node_id=node_id)
        if node_id not in tree_nodes:
            fail("DISPATCH_CHECK", "DISPATCH_ORPHAN", f"Dispatch row '{node_id}' does not match a tree node", run_dir=run_dir, path=dispatch_path, node_id=node_id)
        if tree_nodes[node_id]["status"] == "skipped":
            fail("DISPATCH_CHECK", "DISPATCH_ORPHAN", f"Skipped node '{node_id}' may not be dispatched", run_dir=run_dir, path=dispatch_path, node_id=node_id)
        expected_path = Path("agent_outputs") / f"{node_id}.md"
        if Path(row["artifact_path"]).as_posix() != expected_path.as_posix():
            fail(
                "DISPATCH_CHECK",
                "DISPATCH_ORPHAN",
                f"artifact_path for '{node_id}' must be '{expected_path.as_posix()}'",
                run_dir=run_dir,
                path=dispatch_path,
                node_id=node_id,
            )


def collect_other_artifact_ids(run_dir, current_path):
    source_ids = set()
    claim_ids = set()
    artifact_dir = Path(run_dir) / "agent_outputs"
    if not artifact_dir.exists():
        return source_ids, claim_ids
    for artifact_path in sorted(artifact_dir.glob("*.md")):
        if artifact_path.resolve() == Path(current_path).resolve():
            continue
        try:
            artifact, _ = read_markdown_contract(
                artifact_path,
                "ARTIFACT_CHECK",
                "ARTIFACT_INCOMPLETE",
                run_dir=run_dir,
            )
        except ValidationError:
            continue
        for source in artifact.get("sources", []):
            source_id = source.get("source_id")
            if isinstance(source_id, str) and source_id:
                source_ids.add(source_id)
        for claim in artifact.get("claims", []):
            claim_id = claim.get("claim_id")
            if isinstance(claim_id, str) and claim_id:
                claim_ids.add(claim_id)
    return source_ids, claim_ids


def validate_artifact_document(artifact, artifact_path, tree):
    artifact_path = Path(artifact_path)
    run_dir = artifact_path.parent.parent
    require_keys(
        artifact,
        [
            "node_id",
            "title",
            "scope_confirmed",
            "scope_evidence",
            "confidence_level",
            "prerequisite_nodes",
            "sources",
            "claims",
            "evidence",
            "examples",
            "contradictions",
            "coverage_gaps",
            "teaching_hooks",
        ],
        "ARTIFACT_CHECK",
        "ARTIFACT_INCOMPLETE",
        run_dir=run_dir,
        path=artifact_path,
    )
    node_id = artifact["node_id"]
    require_non_empty_string(node_id, "node_id", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path)
    if artifact_path.stem != node_id:
        fail("ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", f"Artifact filename must match node_id '{node_id}'", run_dir=run_dir, path=artifact_path, node_id=node_id)
    tree_nodes = {node["node_id"]: node for node in tree["nodes"]}
    if node_id not in tree_nodes:
        fail("ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", f"Artifact node_id '{node_id}' is not present in tree.md", run_dir=run_dir, path=artifact_path, node_id=node_id)
    if tree_nodes[node_id]["status"] == "skipped":
        fail("ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", f"Skipped node '{node_id}' must not produce an artifact", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_non_empty_string(artifact["title"], "title", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    if not isinstance(artifact["scope_confirmed"], bool):
        fail("ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", f"scope_confirmed must be boolean for '{node_id}'", run_dir=run_dir, path=artifact_path, node_id=node_id)
    if not artifact["scope_confirmed"]:
        fail("ARTIFACT_CHECK", "SCOPE_NOT_CONFIRMED", f"Artifact '{node_id}' did not confirm scope", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_non_empty_string(artifact["scope_evidence"], "scope_evidence", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_enum(artifact["confidence_level"], "confidence_level", CONFIDENCE_LEVELS, "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_list(artifact["prerequisite_nodes"], "prerequisite_nodes", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    if artifact["prerequisite_nodes"] != tree_nodes[node_id]["prerequisites"]:
        fail(
            "ARTIFACT_CHECK",
            "ARTIFACT_INCOMPLETE",
            f"Artifact '{node_id}' prerequisite_nodes must match tree.md prerequisites",
            run_dir=run_dir,
            path=artifact_path,
            node_id=node_id,
        )
    require_list(artifact["sources"], "sources", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_list(artifact["claims"], "claims", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_list(artifact["evidence"], "evidence", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_non_empty_string_list(artifact["examples"], "examples", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_list(artifact["contradictions"], "contradictions", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_list(artifact["coverage_gaps"], "coverage_gaps", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    require_non_empty_string_list(artifact["teaching_hooks"], "teaching_hooks", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
    if not artifact["sources"]:
        fail("ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", f"Artifact '{node_id}' must include at least one source", run_dir=run_dir, path=artifact_path, node_id=node_id)
    if not artifact["claims"]:
        fail("ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", f"Artifact '{node_id}' must include at least one claim", run_dir=run_dir, path=artifact_path, node_id=node_id)

    other_source_ids, other_claim_ids = collect_other_artifact_ids(run_dir, artifact_path)
    source_ids = set()
    for source in artifact["sources"]:
        require_keys(
            source,
            ["source_id", "source", "title", "excerpt", "tier"],
            "ARTIFACT_CHECK",
            "ARTIFACT_INCOMPLETE",
            run_dir=run_dir,
            path=artifact_path,
            node_id=node_id,
        )
        source_id = source["source_id"]
        require_non_empty_string(source_id, "source_id", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        require_non_empty_string(source["source"], "source", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        require_non_empty_string(source["title"], "title", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        require_non_empty_string(source["excerpt"], "excerpt", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        require_enum(source["tier"], "tier", SOURCE_TIERS, "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        if source_id in source_ids or source_id in other_source_ids:
            fail("ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", f"Duplicate source_id '{source_id}' in package", run_dir=run_dir, path=artifact_path, node_id=node_id)
        source_ids.add(source_id)

    evidence_ids = set()
    for evidence_id in artifact["evidence"]:
        require_non_empty_string(evidence_id, "evidence[]", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        if evidence_id not in source_ids:
            fail("ARTIFACT_CHECK", "CLAIM_UNTRACEABLE", f"Evidence id '{evidence_id}' is missing from sources in '{node_id}'", run_dir=run_dir, path=artifact_path, node_id=node_id)
        evidence_ids.add(evidence_id)

    claim_ids = set()
    for claim in artifact["claims"]:
        require_keys(
            claim,
            ["claim_id", "claim", "source_ids", "confidence"],
            "ARTIFACT_CHECK",
            "ARTIFACT_INCOMPLETE",
            run_dir=run_dir,
            path=artifact_path,
            node_id=node_id,
        )
        claim_id = claim["claim_id"]
        require_non_empty_string(claim_id, "claim_id", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        require_non_empty_string(claim["claim"], "claim", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        require_list(claim["source_ids"], "source_ids", "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        require_enum(claim["confidence"], "confidence", CONFIDENCE_LEVELS, "ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", run_dir=run_dir, path=artifact_path, node_id=node_id)
        if claim_id in claim_ids or claim_id in other_claim_ids:
            fail("ARTIFACT_CHECK", "ARTIFACT_INCOMPLETE", f"Duplicate claim_id '{claim_id}' in package", run_dir=run_dir, path=artifact_path, node_id=node_id)
        if not claim["source_ids"]:
            fail("ARTIFACT_CHECK", "CLAIM_UNTRACEABLE", f"Claim '{claim_id}' must reference at least one source", run_dir=run_dir, path=artifact_path, node_id=node_id)
        for source_id in claim["source_ids"]:
            if source_id not in source_ids:
                fail(
                    "ARTIFACT_CHECK",
                    "CLAIM_UNTRACEABLE",
                    f"Claim '{claim_id}' references missing source_id '{source_id}'",
                    run_dir=run_dir,
                    path=artifact_path,
                    node_id=node_id,
                )
            if source_id not in evidence_ids:
                fail(
                    "ARTIFACT_CHECK",
                    "CLAIM_UNTRACEABLE",
                    f"Claim '{claim_id}' source_id '{source_id}' is not listed in evidence for '{node_id}'",
                    run_dir=run_dir,
                    path=artifact_path,
                    node_id=node_id,
                )
        claim_ids.add(claim_id)


def append_jsonl(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def log_event(run_dir, event, *, check="", status="ok", code="", path="", node_id="", message="", details=None):
    record = {
        "timestamp": now_iso(),
        "event": event,
        "check": check,
        "status": status,
        "code": code,
        "path": str(path) if path else "",
        "node_id": node_id or "",
        "message": message,
    }
    if details is not None:
        record["details"] = details
    append_jsonl(Path(run_dir) / "run_log.jsonl", record)


def write_failure_report(error):
    if not error.run_dir:
        return
    recovery = RECOVERY_HINTS.get(
        error.code,
        "Fix the reported issue, update the affected artifact or tree state, and rerun the check.",
    )
    payload = {
        "check": error.check,
        "code": error.code,
        "node_id": error.node_id,
        "timestamp": now_iso(),
        "message": error.message,
        "recovery": recovery,
    }
    body = (
        "# Failure Report\n\n"
        f"- Check: `{error.check}`\n"
        f"- Code: `{error.code}`\n"
        f"- Path: `{error.path}`\n"
        f"- Node: `{error.node_id or 'N/A'}`\n"
        f"- Message: {error.message}\n"
        f"- Recovery: {recovery}\n"
    )
    write_markdown_contract(Path(error.run_dir) / "failure_report.md", payload, body)
    log_event(
        error.run_dir,
        "on_check_failed",
        check=error.check,
        status="failed",
        code=error.code,
        path=error.path,
        node_id=error.node_id,
        message=error.message,
    )


def summarize_claim(claim_text):
    text = normalize_space(claim_text)
    if len(text) <= 120:
        return text
    return text[:117].rstrip() + "..."


def parse_claim_ledger(path):
    if not Path(path).exists():
        return {}
    lines = read_text(path).splitlines()
    rows = {}
    pipe_placeholder = "\0PIPE\0"
    for line in lines:
        if not line.startswith("|"):
            continue
        safe_line = line.replace("\\|", pipe_placeholder)
        cells = [cell.strip().replace(pipe_placeholder, "|") for cell in safe_line.strip().strip("|").split("|")]
        if len(cells) != 5:
            continue
        if cells[0] in {"claim_id", "---"}:
            continue
        claim_id, node_id, claim_text, source_ids, status = cells
        rows[claim_id] = {
            "node_id": node_id,
            "claim_text": claim_text,
            "source_ids": [item.strip() for item in source_ids.split(",") if item.strip()],
            "status": status,
        }
    return rows


def parse_source_ledger(path):
    records = {}
    if not Path(path).exists():
        return records
    for line in read_text(path).splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        records[record["id"]] = record
    return records


def get_tree_and_validate(tree_path):
    tree, _ = load_tree(tree_path)
    validate_tree_document(tree, Path(tree_path))
    return tree


def command_init_tree(args):
    run_dir = Path(args.out)
    if (run_dir / "tree.md").exists():
        fail("TOPIC_CHECK", "TREE_INCOMPLETE", f"Run package already exists at {run_dir}", run_dir=run_dir, path=run_dir / "tree.md")
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "agent_outputs").mkdir(exist_ok=True)
    framing_payload = {
        "topic": args.topic,
        "expert_identity": "",
        "learner_goal": "",
        "primary_confusion": "",
        "entry_point": "",
        "research_plan": "",
        "source_strategy": "",
        "success_criteria": "",
    }
    framing_body = (
        "# Framing Brief\n\n"
        "Complete this before filling `tree.md`. Keep the brief compact: name the subject-matter lens, "
        "the learner goal, the confusion to resolve, the entry point, the research plan, the source strategy, "
        "and the success test for the final teaching answer.\n"
    )
    tree_payload = {
        "topic": args.topic,
        "slug": slugify(args.topic),
        "created": now_iso(),
        "nodes": [],
    }
    tree_body = (
        "# Tree\n\n"
        "Fill the JSON block with model-inferred semantic nodes. Let the assigning Agent or Integrator "
        "choose node boundaries from knowledge questions, source structure, dependency order, and teaching value. "
        "Each node needs a falsifiable `stop_condition`, valid `source_tier`, prerequisite list, and status.\n"
    )
    dispatch_payload = {"dispatch": []}
    dispatch_body = (
        "# Dispatch\n\n"
        "Add one row per dispatched node after `validate-tree` passes. Use `agent_outputs/<node_id>.md` as `artifact_path`.\n"
    )
    write_markdown_contract(run_dir / "framing_brief.md", framing_payload, framing_body)
    write_markdown_contract(run_dir / "tree.md", tree_payload, tree_body)
    write_markdown_contract(run_dir / "dispatch.md", dispatch_payload, dispatch_body)
    log_event(
        run_dir,
        "on_tree_created",
        check="TOPIC_CHECK",
        status="ok",
        path=run_dir / "tree.md",
        message=f"Initialized research package for '{args.topic}'",
    )
    print(run_dir)


def command_validate_tree(args):
    tree_path = Path(args.tree)
    tree = get_tree_and_validate(tree_path)
    print(f"TREE_CHECK ok: {len(tree['nodes'])} nodes")


def command_validate_dispatch(args):
    tree_path = Path(args.tree)
    dispatch_path = Path(args.dispatch)
    tree, tree_body = load_tree(tree_path)
    validate_tree_document(tree, tree_path)
    dispatch, _ = read_markdown_contract(
        dispatch_path,
        "DISPATCH_CHECK",
        "DISPATCH_ORPHAN",
        run_dir=dispatch_path.parent,
    )
    validate_dispatch_document(dispatch, dispatch_path, tree)
    node_map = {node["node_id"]: node for node in tree["nodes"]}
    for row in dispatch["dispatch"]:
        node = node_map[row["node_id"]]
        node["status"] = "dispatched"
        node["owner"] = row["owner"]
    write_markdown_contract(tree_path, tree, tree_body)
    print(f"DISPATCH_CHECK ok: {len(dispatch['dispatch'])} rows")


def command_validate_artifact(args):
    artifact_path = Path(args.artifact)
    run_dir = artifact_path.parent.parent
    tree = get_tree_and_validate(run_dir / "tree.md")
    artifact, _ = read_markdown_contract(
        artifact_path,
        "ARTIFACT_CHECK",
        "ARTIFACT_INCOMPLETE",
        run_dir=run_dir,
    )
    validate_artifact_document(artifact, artifact_path, tree)
    print(f"ARTIFACT_CHECK ok: {artifact['node_id']}")


def render_claim_ledger(rows):
    lines = [
        "| claim_id | node_id | claim_text | source_ids | status |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {claim_id} | {node_id} | {claim_text} | {source_ids} | {status} |".format(
                claim_id=row["claim_id"].replace("|", "\\|"),
                node_id=row["node_id"].replace("|", "\\|"),
                claim_text=row["claim_text"].replace("|", "\\|"),
                source_ids=", ".join(row["source_ids"]).replace("|", "\\|"),
                status=row["status"].replace("|", "\\|"),
            )
        )
    return "# Claim Ledger\n\n" + "\n".join(lines) + "\n"


def ensure_skipped_nodes_in_body(body, nodes):
    for node in nodes:
        if node["node_id"] not in body or node["skip_reason"] not in body:
            return False
    return True


def ensure_any_artifact_aligns_with_framing(run_dir, tree, framing, check, path):
    framing_terms = framing_alignment_terms(framing)
    if not framing_terms:
        fail(check, "SYNTHESIS_UNCOVERED", "framing_brief lacks checkable success_criteria or primary_confusion terms", run_dir=run_dir, path=path)
    for node in tree["nodes"]:
        if node["status"] == "skipped":
            continue
        artifact, _ = read_markdown_contract(
            Path(run_dir) / "agent_outputs" / f"{node['node_id']}.md",
            "ARTIFACT_CHECK",
            "ARTIFACT_INCOMPLETE",
            run_dir=run_dir,
            node_id=node["node_id"],
        )
        if artifact_aligns_with_framing(artifact, framing_terms):
            return
    fail(
        check,
        "SYNTHESIS_UNCOVERED",
        "No artifact claim or scope_evidence aligns with framing_brief success_criteria or primary_confusion",
        run_dir=run_dir,
        path=path,
    )


def render_framing_brief_lines(framing):
    return [
        "## Framing Brief",
        f"- Expert identity: {framing['expert_identity']}",
        f"- Learner goal: {framing['learner_goal']}",
        f"- Primary confusion: {framing['primary_confusion']}",
        f"- Entry point: {framing['entry_point']}",
        f"- Research plan: {framing['research_plan']}",
        f"- Source strategy: {framing['source_strategy']}",
        f"- Success criteria: {framing['success_criteria']}",
        "",
    ]


def command_merge(args):
    run_dir = Path(args.run_dir)
    tree_path = run_dir / "tree.md"
    tree, tree_body = load_tree(tree_path)
    validate_tree_document(tree, tree_path)
    framing, _ = load_valid_framing_brief(run_dir, expected_topic=tree["topic"])
    ordered_node_ids = topo_sort(tree["nodes"])
    node_map = {node["node_id"]: node for node in tree["nodes"]}

    artifacts = {}
    all_sources = []
    claim_rows = []
    all_claim_ids = []
    open_gaps = []
    open_contradictions = []
    skipped_nodes = [node for node in tree["nodes"] if node["status"] == "skipped"]

    for node_id in ordered_node_ids:
        node = node_map[node_id]
        if node["status"] == "skipped":
            continue
        artifact_path = run_dir / "agent_outputs" / f"{node_id}.md"
        artifact, _ = read_markdown_contract(
            artifact_path,
            "ARTIFACT_CHECK",
            "ARTIFACT_INCOMPLETE",
            run_dir=run_dir,
            node_id=node_id,
        )
        validate_artifact_document(artifact, artifact_path, tree)
        artifacts[node_id] = artifact
        node["status"] = "complete"
        for source in artifact["sources"]:
            all_sources.append(
                {
                    "id": source["source_id"],
                    "node_id": node_id,
                    "source": source["source"],
                    "title": source["title"],
                    "excerpt": source["excerpt"],
                    "tier": source["tier"],
                    "retrieved": now_iso(),
                }
            )
        for claim in artifact["claims"]:
            claim_rows.append(
                {
                    "claim_id": claim["claim_id"],
                    "node_id": node_id,
                    "claim_text": summarize_claim(claim["claim"]),
                    "source_ids": claim["source_ids"],
                    "status": "confirmed",
                }
            )
            all_claim_ids.append(claim["claim_id"])
        open_gaps.extend([f"{node_id}: {gap}" for gap in artifact["coverage_gaps"]])
        open_contradictions.extend([f"{node_id}: {item}" for item in artifact["contradictions"]])
        log_event(
            run_dir,
            "on_artifact_accepted",
            check="ARTIFACT_CHECK",
            status="ok",
            code="",
            path=artifact_path,
            node_id=node_id,
            message=f"Accepted artifact for '{node_id}'",
        )

    write_markdown_contract(tree_path, tree, tree_body)

    source_ledger_path = run_dir / "source_ledger.jsonl"
    source_ledger_path.write_text("", encoding="utf-8")
    for record in all_sources:
        append_jsonl(source_ledger_path, record)

    claim_ledger_path = run_dir / "claim_ledger.md"
    write_text(claim_ledger_path, render_claim_ledger(claim_rows))

    synthesis_payload = {
        "topic": tree["topic"],
        "slug": tree["slug"],
        "generated": now_iso(),
        "framing_brief": framing,
        "nodes_covered": [node_id for node_id in ordered_node_ids if node_map[node_id]["status"] != "skipped"],
        "nodes_skipped": [node["node_id"] for node in skipped_nodes],
        "claim_ids": all_claim_ids,
        "open_contradictions": open_contradictions,
        "open_gaps": open_gaps,
    }
    synthesis_lines = [f"# Synthesis: {tree['topic']}", ""]
    synthesis_lines.extend(render_framing_brief_lines(framing))
    for node_id in ordered_node_ids:
        node = node_map[node_id]
        if node["status"] == "skipped":
            continue
        artifact = artifacts[node_id]
        synthesis_lines.extend([f"## {node['title']} (`{node_id}`)", f"- Question: {node['question']}", f"- Scope evidence: {artifact['scope_evidence']}"])
        synthesis_lines.append("- Claims:")
        for claim in artifact["claims"]:
            synthesis_lines.append(f"  - [{claim['claim_id']}] {claim['claim']}")
        if artifact["examples"]:
            synthesis_lines.append("- Examples:")
            for example in artifact["examples"]:
                synthesis_lines.append(f"  - {example}")
        if artifact["contradictions"]:
            synthesis_lines.append("- Contradictions:")
            for item in artifact["contradictions"]:
                synthesis_lines.append(f"  - {item}")
        if artifact["coverage_gaps"]:
            synthesis_lines.append("- Coverage Gaps:")
            for gap in artifact["coverage_gaps"]:
                synthesis_lines.append(f"  - {gap}")
        if artifact["teaching_hooks"]:
            synthesis_lines.append("- Teaching Hooks:")
            for hook in artifact["teaching_hooks"]:
                synthesis_lines.append(f"  - {hook}")
        synthesis_lines.append("")
    synthesis_lines.append("## Skipped Nodes")
    if skipped_nodes:
        for node in skipped_nodes:
            synthesis_lines.append(f"- `{node['node_id']}` ({node['title']}): {node['skip_reason']}")
    else:
        synthesis_lines.append("- None")
    if open_gaps:
        synthesis_lines.extend(["", "## Open Gaps"])
        for gap in open_gaps:
            synthesis_lines.append(f"- {gap}")
    if open_contradictions:
        synthesis_lines.extend(["", "## Open Contradictions"])
        for item in open_contradictions:
            synthesis_lines.append(f"- {item}")
    write_markdown_contract(run_dir / "synthesis.md", synthesis_payload, "\n".join(synthesis_lines) + "\n")

    learning_path_payload = {
        "topic": tree["topic"],
        "slug": tree["slug"],
        "generated": now_iso(),
        "framing_brief": framing,
        "path": [],
    }
    learning_path_lines = [f"# Learning Path: {tree['topic']}", ""]
    learning_path_lines.extend(render_framing_brief_lines(framing))
    learning_path_lines.append("## Ordered Path")
    for index, node_id in enumerate(ordered_node_ids, start=1):
        node = node_map[node_id]
        if node["status"] == "skipped":
            continue
        artifact = artifacts[node_id]
        summary = summarize_claim(artifact["claims"][0]["claim"])
        claim_ids = [claim["claim_id"] for claim in artifact["claims"]]
        learning_path_payload["path"].append(
            {
                "node_id": node_id,
                "title": node["title"],
                "summary": summary,
                "claim_ids": claim_ids,
                "prerequisites": node["prerequisites"],
            }
        )
        learning_path_lines.append(f"{index}. `{node_id}` - {node['title']}: {summary}")
    learning_path_lines.extend(["", "## Skipped Nodes"])
    if skipped_nodes:
        for node in skipped_nodes:
            learning_path_lines.append(f"- `{node['node_id']}` ({node['title']}): {node['skip_reason']}")
    else:
        learning_path_lines.append("- None")
    learning_path_lines.extend(["", "## Open Gaps"])
    if open_gaps:
        for gap in open_gaps:
            learning_path_lines.append(f"- {gap}")
    else:
        learning_path_lines.append("- None")
    write_markdown_contract(run_dir / "learning_path.md", learning_path_payload, "\n".join(learning_path_lines) + "\n")

    log_event(
        run_dir,
        "on_synthesis_written",
        check="SYNTHESIS_CHECK",
        status="ok",
        path=run_dir / "synthesis.md",
        message=f"Wrote synthesis for '{tree['slug']}'",
    )
    print(f"merge ok: {run_dir}")


def command_validate_synthesis(args):
    run_dir = Path(args.run_dir)
    tree = get_tree_and_validate(run_dir / "tree.md")
    framing, _ = load_valid_framing_brief(run_dir, expected_topic=tree["topic"])
    synthesis, synthesis_body = read_markdown_contract(
        run_dir / "synthesis.md",
        "SYNTHESIS_CHECK",
        "SYNTHESIS_UNCOVERED",
        run_dir=run_dir,
    )
    require_keys(
        synthesis,
        [
            "topic",
            "slug",
            "generated",
            "framing_brief",
            "nodes_covered",
            "nodes_skipped",
            "claim_ids",
            "open_contradictions",
            "open_gaps",
        ],
        "SYNTHESIS_CHECK",
        "SYNTHESIS_UNCOVERED",
        run_dir=run_dir,
        path=run_dir / "synthesis.md",
    )
    if synthesis["framing_brief"] != framing:
        fail("SYNTHESIS_CHECK", "SYNTHESIS_UNCOVERED", "synthesis.md dropped or changed framing_brief", run_dir=run_dir, path=run_dir / "synthesis.md")
    for field_name in ["learner_goal", "primary_confusion", "entry_point"]:
        if framing[field_name] not in synthesis_body:
            fail("SYNTHESIS_CHECK", "SYNTHESIS_UNCOVERED", f"synthesis.md body is missing framing field '{field_name}'", run_dir=run_dir, path=run_dir / "synthesis.md")
    covered = set(synthesis["nodes_covered"])
    skipped = set(synthesis["nodes_skipped"])
    expected_covered = {node["node_id"] for node in tree["nodes"] if node["status"] != "skipped"}
    expected_skipped = {node["node_id"] for node in tree["nodes"] if node["status"] == "skipped"}
    if covered != expected_covered:
        fail("SYNTHESIS_CHECK", "SYNTHESIS_UNCOVERED", "synthesis.md does not cover every non-skipped node", run_dir=run_dir, path=run_dir / "synthesis.md")
    if skipped != expected_skipped:
        fail("SYNTHESIS_CHECK", "SYNTHESIS_UNCOVERED", "synthesis.md does not list every skipped node", run_dir=run_dir, path=run_dir / "synthesis.md")
    skipped_nodes = [node for node in tree["nodes"] if node["status"] == "skipped"]
    if not ensure_skipped_nodes_in_body(synthesis_body, skipped_nodes):
        fail("SYNTHESIS_CHECK", "SYNTHESIS_UNCOVERED", "Skipped nodes or reasons are missing from synthesis body", run_dir=run_dir, path=run_dir / "synthesis.md")

    claim_rows = parse_claim_ledger(run_dir / "claim_ledger.md")
    source_rows = parse_source_ledger(run_dir / "source_ledger.jsonl")
    for claim_id in synthesis["claim_ids"]:
        if claim_id not in claim_rows:
            fail("SYNTHESIS_CHECK", "CLAIM_UNTRACEABLE", f"Claim '{claim_id}' is missing from claim_ledger.md", run_dir=run_dir, path=run_dir / "synthesis.md")
        for source_id in claim_rows[claim_id]["source_ids"]:
            if source_id not in source_rows:
                fail("SYNTHESIS_CHECK", "CLAIM_UNTRACEABLE", f"Claim '{claim_id}' references missing source '{source_id}'", run_dir=run_dir, path=run_dir / "synthesis.md")

    expected_gaps = set()
    expected_contradictions = set()
    for node in tree["nodes"]:
        if node["status"] == "skipped":
            continue
        artifact, _ = read_markdown_contract(
            run_dir / "agent_outputs" / f"{node['node_id']}.md",
            "ARTIFACT_CHECK",
            "ARTIFACT_INCOMPLETE",
            run_dir=run_dir,
            node_id=node["node_id"],
        )
        expected_gaps.update({f"{node['node_id']}: {item}" for item in artifact["coverage_gaps"]})
        expected_contradictions.update({f"{node['node_id']}: {item}" for item in artifact["contradictions"]})

    if not expected_gaps.issubset(set(synthesis["open_gaps"])):
        fail("SYNTHESIS_CHECK", "GAP_DROPPED", "synthesis.md dropped one or more coverage gaps", run_dir=run_dir, path=run_dir / "synthesis.md")
    if not expected_contradictions.issubset(set(synthesis["open_contradictions"])):
        fail("SYNTHESIS_CHECK", "GAP_DROPPED", "synthesis.md dropped one or more contradictions", run_dir=run_dir, path=run_dir / "synthesis.md")
    ensure_any_artifact_aligns_with_framing(run_dir, tree, framing, "SYNTHESIS_CHECK", run_dir / "synthesis.md")

    print(f"SYNTHESIS_CHECK ok: {len(covered)} covered, {len(skipped)} skipped")


def command_check_coverage(args):
    run_dir = Path(args.run_dir)
    tree = get_tree_and_validate(run_dir / "tree.md")
    framing, _ = load_valid_framing_brief(run_dir, expected_topic=tree["topic"])
    learning_path, learning_body = read_markdown_contract(
        run_dir / "learning_path.md",
        "COVERAGE_REVIEW",
        "SYNTHESIS_UNCOVERED",
        run_dir=run_dir,
    )
    require_keys(
        learning_path,
        ["topic", "slug", "generated", "framing_brief", "path"],
        "COVERAGE_REVIEW",
        "SYNTHESIS_UNCOVERED",
        run_dir=run_dir,
        path=run_dir / "learning_path.md",
    )
    if learning_path["framing_brief"] != framing:
        fail("COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", "learning_path.md dropped or changed framing_brief", run_dir=run_dir, path=run_dir / "learning_path.md")
    for field_name in ["learner_goal", "primary_confusion", "entry_point"]:
        if framing[field_name] not in learning_body:
            fail("COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", f"learning_path.md body is missing framing field '{field_name}'", run_dir=run_dir, path=run_dir / "learning_path.md")
    require_list(learning_path["path"], "path", "COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", run_dir=run_dir, path=run_dir / "learning_path.md")

    node_map = {node["node_id"]: node for node in tree["nodes"]}
    path_ids = [row["node_id"] for row in learning_path["path"]]
    expected_ids = [node["node_id"] for node in tree["nodes"] if node["status"] != "skipped"]
    if set(path_ids) != set(expected_ids):
        fail("COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", "learning_path.md has silent node omissions", run_dir=run_dir, path=run_dir / "learning_path.md")
    order_index = {node_id: index for index, node_id in enumerate(path_ids)}
    for row in learning_path["path"]:
        require_keys(row, ["node_id", "title", "summary", "claim_ids", "prerequisites"], "COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", run_dir=run_dir, path=run_dir / "learning_path.md")
        require_non_empty_string(row["title"], "title", "COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", run_dir=run_dir, path=run_dir / "learning_path.md", node_id=row["node_id"])
        require_non_empty_string(row["summary"], "summary", "COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", run_dir=run_dir, path=run_dir / "learning_path.md", node_id=row["node_id"])
        require_list(row["claim_ids"], "claim_ids", "COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", run_dir=run_dir, path=run_dir / "learning_path.md", node_id=row["node_id"])
        require_list(row["prerequisites"], "prerequisites", "COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", run_dir=run_dir, path=run_dir / "learning_path.md", node_id=row["node_id"])
        for prereq in row["prerequisites"]:
            if prereq not in order_index or order_index[prereq] >= order_index[row["node_id"]]:
                fail(
                    "COVERAGE_REVIEW",
                    "PREREQUISITE_CYCLE",
                    f"Prerequisite order is invalid for '{row['node_id']}'",
                    run_dir=run_dir,
                    path=run_dir / "learning_path.md",
                    node_id=row["node_id"],
                )

    for node in tree["nodes"]:
        if node["priority"] == "load-bearing" and node["status"] not in {"complete", "skipped"}:
            fail(
                "COVERAGE_REVIEW",
                "SYNTHESIS_UNCOVERED",
                f"Load-bearing node '{node['node_id']}' is neither complete nor skipped",
                run_dir=run_dir,
                path=run_dir / "learning_path.md",
                node_id=node["node_id"],
            )
    skipped_nodes = [node for node in tree["nodes"] if node["status"] == "skipped"]
    if not ensure_skipped_nodes_in_body(learning_body, skipped_nodes):
        fail("COVERAGE_REVIEW", "SYNTHESIS_UNCOVERED", "learning_path.md is missing skipped node disclosure", run_dir=run_dir, path=run_dir / "learning_path.md")
    ensure_any_artifact_aligns_with_framing(run_dir, tree, framing, "COVERAGE_REVIEW", run_dir / "learning_path.md")

    print(f"COVERAGE_REVIEW ok: {len(path_ids)} ordered nodes")


def command_status(args):
    run_dir = Path(args.run_dir)
    tree, _ = load_tree(run_dir / "tree.md")
    node_counts = defaultdict(int)
    for node in tree.get("nodes", []):
        node_counts[node.get("status", "unknown")] += 1
    artifact_dir = run_dir / "agent_outputs"
    present_artifacts = sorted(path.stem for path in artifact_dir.glob("*.md")) if artifact_dir.exists() else []
    summary = {
        "run_dir": str(run_dir),
        "topic": tree.get("topic", ""),
        "slug": tree.get("slug", ""),
        "node_counts": dict(node_counts),
        "files": {
            "framing_brief": (run_dir / "framing_brief.md").exists(),
            "tree": (run_dir / "tree.md").exists(),
            "dispatch": (run_dir / "dispatch.md").exists(),
            "synthesis": (run_dir / "synthesis.md").exists(),
            "learning_path": (run_dir / "learning_path.md").exists(),
            "failure_report": (run_dir / "failure_report.md").exists(),
        },
        "artifacts_present": present_artifacts,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def build_parser():
    parser = argparse.ArgumentParser(description="5.26 fallback helper for DeepResearch tree and dispatch mechanics.")
    parser.add_argument(
        "--allow-legacy-helper",
        action="store_true",
        help="Acknowledge this legacy helper is not a MasterZhuyan delivery route.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_tree = subparsers.add_parser("init-tree", help="Initialize a deep-topic run directory.")
    init_tree.add_argument("--topic", required=True)
    init_tree.add_argument("--out", required=True)
    init_tree.set_defaults(func=command_init_tree)

    validate_tree = subparsers.add_parser("validate-tree", help="Validate tree.md.")
    validate_tree.add_argument("tree")
    validate_tree.set_defaults(func=command_validate_tree)

    validate_dispatch = subparsers.add_parser("validate-dispatch", help="Validate dispatch.md against tree.md.")
    validate_dispatch.add_argument("dispatch")
    validate_dispatch.add_argument("--tree", required=True)
    validate_dispatch.set_defaults(func=command_validate_dispatch)

    validate_artifact = subparsers.add_parser("validate-artifact", help="Validate one branch artifact.")
    validate_artifact.add_argument("artifact")
    validate_artifact.set_defaults(func=command_validate_artifact)

    merge = subparsers.add_parser("merge", help="Merge accepted artifacts into ledgers and synthesis.")
    merge.add_argument("run_dir")
    merge.set_defaults(func=command_merge)

    validate_synthesis = subparsers.add_parser("validate-synthesis", help="Validate synthesis traceability.")
    validate_synthesis.add_argument("run_dir")
    validate_synthesis.set_defaults(func=command_validate_synthesis)

    check_coverage = subparsers.add_parser("check-coverage", help="Validate learning path coverage and order.")
    check_coverage.add_argument("run_dir")
    check_coverage.set_defaults(func=command_check_coverage)

    status = subparsers.add_parser("status", help="Summarize the current run package.")
    status.add_argument("run_dir")
    status.set_defaults(func=command_status)

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
        write_failure_report(error)
        print(f"{error.check} {error.code}: {error.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
