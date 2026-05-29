#!/usr/bin/env python3
"""Validate MasterZhuyan DeepResearch artifacts.

The validator checks semantic integration signals instead of treating file count,
chapter count, or agent count as proof of deep research. It verifies the artifact
spine: research tree, source/evidence state, locked knowledge model, integrator
decision, Knowledge-Model-derived chapter plan, citation audit, agent traces or
recorded runtime fallback, and final-output cleanliness.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

CANONICAL_FILES = [
    "manifest.yaml",
    "index.md",
    "final/final_merged.md",
    "notes/process_trace.md",
    "notes/research_brief.md",
    "notes/research_tree.md",
    "notes/source_map.md",
    "notes/evidence_ledger.md",
    "notes/knowledge_model.md",
    "notes/chapter_plan.md",
    "notes/integrator_decisions.md",
    "notes/citation_audit.md",
    "notes/continuation_map.md",
]

CANONICAL_DIRS = ["chapters"]

EVIDENCE_ID_RE = re.compile(r"\b(?:EL|EV)-[A-Za-z0-9_-]+\b|claim_id:\s*([A-Za-z0-9_-]+)", re.IGNORECASE)
EVIDENCE_FIELD_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")
SOURCE_FIELD_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")
VALUE_FIELD_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")
SOURCE_REQUIRED_FIELDS = (
    "source_id",
    "source_type",
    "locator",
    "access_method",
    "read_state",
    "supports_questions",
)
SOURCE_READ_STATES = {"full", "partial", "snippet_only", "unavailable"}
EVIDENCE_REQUIRED_FIELDS = (
    "claim_id",
    "claim",
    "locator",
    "evidence_type",
    "confidence",
    "teaching_use",
)
EVIDENCE_STATUS_STATES = {"accepted", "uncertain", "contradicted", "missing"}
EVIDENCE_SUPPORT_STATES = {"strong", "partial", "inferred", "contradicted", "missing"}
EVIDENCE_CONFIDENCE_STATES = {"high", "med", "medium", "low", "inferred", "unknown"}
EVIDENCE_TYPES = {
    "definition",
    "mechanism",
    "classification",
    "threshold",
    "formula",
    "step",
    "procedure",
    "example",
    "exception",
    "risk",
    "warning",
    "contrast",
    "case",
    "data",
    "quote",
    "counterpoint",
    "other",
}
MUST_PRESERVE_EVIDENCE_TYPES = {
    "definition",
    "mechanism",
    "classification",
    "threshold",
    "formula",
    "step",
    "procedure",
    "exception",
    "risk",
    "warning",
    "contrast",
}
EVIDENCE_TEACHING_USES = {
    "core_explanation",
    "memory_anchor",
    "comparison",
    "easy_error_repair",
    "boundary",
    "example",
    "quality_check",
}
CITATION_REQUIRED_FIELDS = (
    "claim_or_section",
    "evidence_ids",
    "source_ids",
    "locator_check",
    "support_state",
    "integrator_action",
)
CITATION_SUPPORT_STATES = {"supported", "partial", "inferred", "contradicted", "missing"}
CITATION_ACTIONS = {
    "accept",
    "revise",
    "soften_claim",
    "omit_claim",
    "mark_unavailable",
    "dispatch_agent",
    "record_continuation",
}
CITATION_RESOLUTION_ACTIONS = CITATION_ACTIONS - {"accept"}
RESEARCH_BRIEF_REQUIRED_FIELDS = ("primary_confusion", "success_criteria")
KNOWLEDGE_SUPPORT_STATES = {"supported", "partial", "inferred", "missing"}
PROMOTION_RE = re.compile(r"\b(promot|accept|reject|revise|discard|采纳|拒绝|修订|废弃)", re.IGNORECASE)
SUPPORT_RE = re.compile(r"\b(support_state|supported|partial|inferred|contradicted|missing|支持|部分|推断|矛盾|缺失)\b", re.IGNORECASE)
TREE_RE = re.compile(r"\b(node_id|question|status|next_action|stop_condition|节点|问题|状态|下一步|停止条件)\b", re.IGNORECASE)
FALLBACK_ARTIFACT_RE = re.compile(
    r"(?im)^\s*(?:fallback_artifact|proposed_artifact|source_artifact|output_artifact|artifacts_written)\s*:\s*"
    r"(notes/agent_outputs/[^\s]+\.md)\s*$"
)
CANONICAL_TARGET_RE = re.compile(
    r"(?im)^\s*(?:canonical_target|canonical_targets|promoted_to|target_file)\s*:\s*"
    r"((?:notes/(?!agent_outputs/)[^\s]+\.md|chapters/[^\s]+\.md|final/final_merged\.md))\s*$"
)
AGENT_FALLBACK_RE = re.compile(
    r"\b(agent_runtime_unavailable|agent_worker_failed|sub-?agent\w*\s+(?:unavailable|blocked|failed)|"
    r"native agents?\s+(?:unavailable|blocked|failed)|runtime\s+unavailable|worker\s+failed|"
    r"tool_failed|host\s+(?:blocked|denied)|fallback\s+to\s+(?:5\.26|sequential)|5\.26\s+fallback|"
    r"agenticresearch\s+fallback|无法启动|启动失败|不可用|工具失败|宿主限制|运行时失败|降级到\s*5\.26|"
    r"顺序fallback|顺序回退)\b",
    re.IGNORECASE,
)
CHAPTER_ID_RE = re.compile(r"(?im)^\s*chapter_id\s*:\s*([A-Za-z0-9][A-Za-z0-9_.-]*)\s*$")
CHAPTER_FIELD_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")
CHAPTER_REQUIRED_FIELDS = (
    "chapter_id",
    "title",
    "purpose",
    "input_refs",
    "required_anchors",
    "output_path",
    "completion_criteria",
)
CHAPTER_00_RE = re.compile(r"(?im)^\s*(?:chapter_id\s*:\s*)?(?:0?0(?:$|[_\-\s])|chapter[_\-\s]?0?0\b)")
METADATA_CHAPTER_RE = re.compile(
    r"(?im)^\s*(?:title|purpose)\s*:\s*.*(阅读地图|证据地图|来源说明|阅读顺序|如何使用|"
    r"reading\s+map|evidence\s+map|source\s+map|source\s+inventory|delivery\s+note|"
    r"artifact\s+inventory|process\s+(?:summary|note)|usage\s+instructions)"
)
TRACE_UPDATE_RE = re.compile(r"(?im)(^###\s+Trace Update\b|^\s*trace_update\s*:)")
REFERENCE_FRAME_RE = re.compile(
    r"\b(reference_frame|baseline|normal\s+range|default\s+rule|null\s+model|comparator|unit|scale|"
    r"version\s+contract|nominal|starting\s+point|ordinary\s+meaning|参照系|基线|正常范围|默认规则|"
    r"对照|单位|尺度|版本|额定|起点|通常含义)\b",
    re.IGNORECASE,
)
PLACEHOLDER_RE = re.compile(
    r"TODO|TBD|FIXME|\[SOURCE\]|\[CITATION\]|待补充|占位|引用待补|来源待补",
    re.IGNORECASE,
)
WEAK_EVIDENCE_ACTION_RE = re.compile(
    r"\b(inferred|uncertain|contradicted|missing|unavailable|weaken|soften|omit|scope(?:d)?\s*out|"
    r"dispatch|continuation|mark_unavailable|需要进一步核验|不能确定|不确定|矛盾|缺失|弱化|省略|出范围|后续)\b",
    re.IGNORECASE,
)
REFERENCE_GAP_ACTION_RE = re.compile(
    r"\b(unavailable|weaken|soften|omit|scope(?:d)?\s*out|dispatch|continuation|mark_unavailable|"
    r"需要进一步核验|不能确定|弱化|省略|出范围|后续)\b",
    re.IGNORECASE,
)
ANCHOR_RESOLUTION_ACTION_RE = re.compile(
    r"\b(revise|soften_claim|omit_claim|mark_unavailable|dispatch_agent|record_continuation|"
    r"修订|弱化|省略|不可用|派发|继续|后续)\b",
    re.IGNORECASE,
)
CLAIM_CONTENT_RESOLUTION_ACTION_RE = re.compile(
    r"\b(soften_claim|omit_claim|mark_unavailable|dispatch_agent|record_continuation|"
    r"弱化|省略|不可用|派发|继续|后续)\b",
    re.IGNORECASE,
)
CLAIM_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{3,}|[\u4e00-\u9fff]{2,}")
CLAIM_TOKEN_STOPWORDS = {
    "about",
    "after",
    "also",
    "before",
    "chapter",
    "claim",
    "claims",
    "could",
    "does",
    "evidence",
    "from",
    "into",
    "only",
    "should",
    "that",
    "their",
    "there",
    "these",
    "this",
    "those",
    "through",
    "when",
    "where",
    "with",
    "without",
}


def rel_files(root: Path, base: Path) -> list[str]:
    if not base.exists():
        return []
    return sorted(path.relative_to(root).as_posix() for path in base.rglob("*.md") if path.is_file())


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def count_present(required: Iterable[str], root: Path, *, directory: bool = False) -> list[str]:
    present = []
    for item in required:
        path = root / item
        if path.is_dir() if directory else path.is_file():
            present.append(item + "/" if directory else item)
    return present


def evidence_ids(text: str) -> set[str]:
    ids: set[str] = set()
    for match in EVIDENCE_ID_RE.finditer(text):
        token = match.group(0)
        if token.lower().startswith("claim_id:"):
            value = match.group(1)
            if value:
                ids.add(value)
        else:
            ids.add(token)
    return ids


def evidence_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = EVIDENCE_FIELD_RE.match(line)
        if not match:
            if current is not None:
                current["__text__"] = current.get("__text__", "") + "\n" + line
            continue
        key = match.group(1).lower()
        value = match.group(2).strip()
        if key == "claim_id":
            if current is not None:
                entries.append(current)
            current = {"__line__": str(lineno), "__text__": line, "claim_id": value}
        elif current is not None:
            current[key] = value
            current["__text__"] = current.get("__text__", "") + "\n" + line
    if current is not None:
        entries.append(current)
    return entries


def citation_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = VALUE_FIELD_RE.match(line)
        if not match:
            if current is not None:
                current["__text__"] = current.get("__text__", "") + "\n" + line
            continue
        key = match.group(1).lower()
        value = match.group(2).strip()
        if key == "claim_or_section":
            if current is not None:
                entries.append(current)
            current = {"__line__": str(lineno), "__text__": line, "claim_or_section": value}
        elif current is not None:
            current[key] = value
            current["__text__"] = current.get("__text__", "") + "\n" + line
    if current is not None:
        entries.append(current)
    return entries


def value_rows(text: str, start_keys: set[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = VALUE_FIELD_RE.match(line)
        if not match:
            if current is not None:
                current["__text__"] = current.get("__text__", "") + "\n" + line
            continue
        key = match.group(1).lower()
        value = match.group(2).strip()
        if key in start_keys:
            if current is not None:
                rows.append(current)
            current = {"__line__": str(lineno), "__text__": line, key: value, "__start_key__": key}
        elif current is not None:
            current[key] = value
            current["__text__"] = current.get("__text__", "") + "\n" + line
    if current is not None:
        rows.append(current)
    return rows


def source_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = SOURCE_FIELD_RE.match(line)
        if not match:
            if current is not None:
                current["__text__"] = current.get("__text__", "") + "\n" + line
            continue
        key = match.group(1).lower()
        value = match.group(2).strip()
        if key == "source_id":
            if current is not None:
                entries.append(current)
            current = {"__line__": str(lineno), "__text__": line, "source_id": value}
        elif current is not None:
            current[key] = value
            current["__text__"] = current.get("__text__", "") + "\n" + line
    if current is not None:
        entries.append(current)
    return entries


def split_id_values(raw: str) -> set[str]:
    cleaned = raw.strip().strip("[]")
    if not cleaned:
        return set()
    values: set[str] = set()
    for item in re.split(r"[,;]", cleaned):
        value = item.strip().strip("'\"")
        if value:
            values.add(value)
    return values


def field_block_value(entry: dict[str, str], key: str) -> str:
    value = entry.get(key, "").strip()
    if value:
        return value
    lines = entry.get("__text__", "").splitlines()
    collected: list[str] = []
    in_block = False
    field_re = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")
    for line in lines:
        match = field_re.match(line)
        if match:
            current_key = match.group(1).lower()
            if current_key == key:
                in_block = True
                inline_value = match.group(2).strip()
                if inline_value:
                    collected.append(inline_value)
                continue
            if in_block:
                break
        elif in_block:
            cleaned = line.strip().lstrip("-").strip()
            if cleaned:
                collected.append(cleaned)
    return "\n".join(collected).strip()


def claim_core_tokens(claim: str) -> set[str]:
    tokens = {match.group(0).lower() for match in CLAIM_TOKEN_RE.finditer(claim)}
    tokens = {token for token in tokens if token not in CLAIM_TOKEN_STOPWORDS}
    for run in re.findall(r"[\u4e00-\u9fff]{4,}", claim):
        tokens.update(run[index : index + 2] for index in range(len(run) - 1))
    return tokens


def carries_claim_content(claim: str, text: str) -> bool:
    tokens = claim_core_tokens(claim)
    if not tokens:
        return True
    lowered = text.lower()
    found = {token for token in tokens if token in lowered}
    threshold = min(3, max(1, (len(tokens) + 1) // 2))
    return len(found) >= threshold


def knowledge_model_evidence_ids(text: str) -> set[str]:
    ids: set[str] = set()
    for line in text.splitlines():
        match = VALUE_FIELD_RE.match(line)
        if not match:
            continue
        key = match.group(1).lower()
        if key in {"evidence_ids", "core_spine_evidence_ids"}:
            ids.update(split_id_values(match.group(2)))
    return ids


def weak_evidence_ids(entries: Iterable[dict[str, str]]) -> set[str]:
    weak: set[str] = set()
    for entry in entries:
        claim_id = entry.get("claim_id")
        if not claim_id:
            continue
        status = (entry.get("status") or entry.get("support_state") or "").lower()
        confidence = entry.get("confidence", "").lower()
        if status in {"uncertain", "contradicted", "missing", "partial", "inferred"} or confidence in {
            "low",
            "inferred",
            "unknown",
        }:
            weak.add(claim_id)
    return weak


def unresolved_weak_evidence_refs(refs: set[str], weak_ids: set[str], text: str) -> set[str]:
    used_weak = refs & weak_ids
    if not used_weak:
        return set()
    if WEAK_EVIDENCE_ACTION_RE.search(text):
        return set()
    return used_weak


def unresolved_reference_frame_gap_ids(entries: Iterable[dict[str, str]], resolution_text: str) -> set[str]:
    unresolved: set[str] = set()
    if REFERENCE_GAP_ACTION_RE.search(resolution_text):
        return unresolved
    for entry in entries:
        claim_id = entry.get("claim_id")
        if not claim_id:
            continue
        evidence_type = entry.get("evidence_type", "").lower()
        status = (entry.get("status") or entry.get("support_state") or "").lower()
        confidence = entry.get("confidence", "").lower()
        teaching_use = entry.get("teaching_use", "").lower()
        if evidence_type not in {"threshold", "risk", "formula", "contrast"}:
            continue
        if status not in {"missing", "uncertain", "partial"} and confidence not in {"low", "unknown"}:
            continue
        if not any(token in teaching_use for token in ("boundary", "quality_check", "core_explanation")):
            continue
        unresolved.add(claim_id)
    return unresolved


def accepted_must_preserve_ids(entries: Iterable[dict[str, str]], source_refs: dict[str, set[str]]) -> set[str]:
    ids: set[str] = set()
    for entry in entries:
        claim_id = entry.get("claim_id")
        source_ref = entry.get("source_ref") or entry.get("source_id")
        if not claim_id or not source_ref:
            continue
        if claim_id not in source_refs.get(source_ref, set()):
            continue
        evidence_type = entry.get("evidence_type", "").lower()
        status = (entry.get("status") or entry.get("support_state") or "").lower()
        if evidence_type in MUST_PRESERVE_EVIDENCE_TYPES and status in {"accepted", "strong"}:
            ids.add(claim_id)
    return ids


def has_recorded_fallback(text: str) -> bool:
    return bool(
        AGENT_FALLBACK_RE.search(text)
        and FALLBACK_ARTIFACT_RE.search(text)
        and CANONICAL_TARGET_RE.search(text)
        and PROMOTION_RE.search(text)
    )


def has_integrator_decision(text: str, *, source_artifact: str = "", target: str = "", section_id: str = "") -> bool:
    for block in re.split(r"(?:\r?\n){2,}", text):
        if not PROMOTION_RE.search(block):
            continue
        required_tokens = [token for token in (source_artifact, target, section_id) if token]
        if required_tokens and all(token in block for token in required_tokens):
            return True
    return False


def has_chapter_fallback_decision(text: str, *, target: str, section_id: str) -> bool:
    for block in re.split(r"(?:\r?\n){2,}", text):
        if (
            AGENT_FALLBACK_RE.search(block)
            and FALLBACK_ARTIFACT_RE.search(block)
            and PROMOTION_RE.search(block)
            and target in block
            and section_id in block
        ):
            return True
    return False


def section_resolution_ids(entries: Iterable[dict[str, str]], candidates: Iterable[str]) -> tuple[set[str], str]:
    ids: set[str] = set()
    text_blocks: list[str] = []
    tokens = [candidate for candidate in candidates if candidate]
    for entry in entries:
        block = entry.get("__text__", "")
        section = entry.get("claim_or_section", "")
        searchable = block + "\n" + section
        if not any(token in searchable for token in tokens):
            continue
        ids.update(split_id_values(entry.get("evidence_ids", "")))
        text_blocks.append(block)
    return ids, "\n".join(text_blocks)


def has_anchor_resolution(text: str, *, evidence_id: str, candidates: Iterable[str]) -> bool:
    if evidence_id not in text or not ANCHOR_RESOLUTION_ACTION_RE.search(text):
        return False
    tokens = [candidate for candidate in candidates if candidate]
    if not tokens:
        return False
    for block in re.split(r"(?:\r?\n){2,}", text):
        if evidence_id in block and ANCHOR_RESOLUTION_ACTION_RE.search(block) and any(token in block for token in tokens):
            return True
    return False


def has_claim_content_resolution(text: str, *, evidence_id: str, candidates: Iterable[str] = ()) -> bool:
    tokens = [candidate for candidate in candidates if candidate]
    for block in re.split(r"(?:\r?\n){2,}", text):
        if evidence_id not in block or not CLAIM_CONTENT_RESOLUTION_ACTION_RE.search(block):
            continue
        if tokens and not any(token in block for token in tokens):
            continue
        return True
    return False


def evidence_resolution_text(
    entries: Iterable[dict[str, str]],
    evidence_id: str,
    candidates: Iterable[str] = (),
) -> str:
    tokens = [candidate for candidate in candidates if candidate]
    blocks: list[str] = []
    for entry in entries:
        block = entry.get("__text__", "")
        if evidence_id not in split_id_values(entry.get("evidence_ids", "")):
            continue
        if tokens:
            searchable = block + "\n" + entry.get("claim_or_section", "")
            if not any(token in searchable for token in tokens):
                continue
        blocks.append(block)
    return "\n".join(blocks)


def target_text_for_evidence(
    root: Path,
    *,
    citation_entries_: Iterable[dict[str, str]],
    evidence_id: str,
    output_path: str = "",
    candidates: Iterable[str] = (),
    chapters: Iterable[str] = (),
    final_text: str = "",
) -> str:
    tokens = [candidate for candidate in candidates if candidate]
    texts: list[str] = []
    for entry in citation_entries_:
        if evidence_id not in split_id_values(entry.get("evidence_ids", "")):
            continue
        block = entry.get("__text__", "")
        section = entry.get("claim_or_section", "")
        searchable = block + "\n" + section
        if tokens and not any(token in searchable for token in tokens):
            continue
        if section.startswith("chapters/") and (root / section).is_file():
            texts.append(read_text(root / section))
        elif section == "final/final_merged.md":
            texts.append(final_text)
        elif output_path and any(token in searchable for token in [output_path, *tokens]) and (root / output_path).is_file():
            texts.append(read_text(root / output_path))
    if not texts:
        texts.extend(read_text(root / chapter) for chapter in chapters if (root / chapter).is_file())
        texts.append(final_text)
    return "\n".join(texts)


def chapter_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = CHAPTER_FIELD_RE.match(line)
        if not match:
            if current is not None:
                current["__text__"] = current.get("__text__", "") + "\n" + line
            continue
        key = match.group(1).lower()
        value = match.group(2).strip()
        if key == "chapter_id":
            if current is not None:
                rows.append(current)
            current = {"__line__": str(lineno), "__text__": line, "chapter_id": value}
        elif current is not None:
            current[key] = value
            current["__text__"] = current.get("__text__", "") + "\n" + line
    if current is not None:
        rows.append(current)
    return rows


def manifest_chapter_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_chapters = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^chapters\s*:\s*$", line):
            in_chapters = True
            current = None
            continue
        if in_chapters and re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*:", line):
            break
        if not in_chapters:
            continue
        if line.startswith("  - "):
            if current is not None:
                rows.append(current)
            current = {}
            rest = line[4:].strip()
            if ":" in rest:
                key, value = rest.split(":", 1)
                current[key.strip().lower()] = value.strip().strip("'\"")
        elif line.startswith("    ") and current is not None and ":" in line:
            key, value = line.strip().split(":", 1)
            current[key.strip().lower()] = value.strip().strip("'\"")
    if current is not None:
        rows.append(current)
    return rows


def plan_chapter_signature(rows: Iterable[dict[str, str]]) -> list[tuple[str, str, str]]:
    return [
        (row.get("chapter_id", ""), row.get("title", ""), row.get("output_path", ""))
        for row in rows
    ]


def manifest_chapter_signature(rows: Iterable[dict[str, str]]) -> list[tuple[str, str, str]]:
    return [
        (row.get("id", ""), row.get("title", ""), row.get("file", ""))
        for row in rows
    ]


def validate_root(root: Path) -> dict:
    root = root.resolve()

    missing: list[str] = []
    empty_files: list[str] = []
    warnings: list[str] = []
    semantic_failures: list[str] = []

    for item in CANONICAL_FILES:
        path = root / item
        if not path.is_file():
            missing.append(item)
        elif path.stat().st_size == 0:
            empty_files.append(item)

    for item in CANONICAL_DIRS:
        path = root / item
        if not path.is_dir():
            missing.append(item + "/")

    chapters = rel_files(root, root / "chapters")
    agent_outputs = rel_files(root, root / "notes" / "agent_outputs")

    if (root / "chapters").is_dir() and not chapters:
        missing.append("chapters/*.md")
    source_path = root / "notes" / "source_map.md"
    evidence_path = root / "notes" / "evidence_ledger.md"
    knowledge_path = root / "notes" / "knowledge_model.md"
    research_path = root / "notes" / "research_brief.md"
    decisions_path = root / "notes" / "integrator_decisions.md"
    tree_path = root / "notes" / "research_tree.md"
    chapter_plan_path = root / "notes" / "chapter_plan.md"
    citation_path = root / "notes" / "citation_audit.md"
    trace_path = root / "notes" / "process_trace.md"
    final_path = root / "final" / "final_merged.md"
    manifest_path = root / "manifest.yaml"
    index_path = root / "index.md"

    manifest_text = read_text(manifest_path) if manifest_path.is_file() else ""
    index_text = read_text(index_path) if index_path.is_file() else ""
    research_text = read_text(research_path) if research_path.is_file() else ""
    source_text = read_text(source_path) if source_path.is_file() else ""
    evidence_text = read_text(evidence_path) if evidence_path.is_file() else ""
    knowledge_text = read_text(knowledge_path) if knowledge_path.is_file() else ""
    decisions_text = read_text(decisions_path) if decisions_path.is_file() else ""
    tree_text = read_text(tree_path) if tree_path.is_file() else ""
    chapter_plan_text = read_text(chapter_plan_path) if chapter_plan_path.is_file() else ""
    citation_text = read_text(citation_path) if citation_path.is_file() else ""
    trace_text = read_text(trace_path) if trace_path.is_file() else ""
    final_text = read_text(final_path) if final_path.is_file() else ""

    source_map_entries: list[dict[str, str]] = []
    source_map_ids: set[str] = set()
    source_map_evidence_card_refs: dict[str, set[str]] = {}
    ledger_ids = evidence_ids(evidence_text)
    model_ids = knowledge_model_evidence_ids(knowledge_text)
    ledger_entries: list[dict[str, str]] = []
    structured_ledger_ids: set[str] = set()
    citation_entry_rows: list[dict[str, str]] = []
    accepted_must_preserve_evidence_ids: set[str] = set()
    ledger_claims: dict[str, str] = {}

    if source_path.is_file():
        source_map_entries = source_entries(source_text)
        source_map_ids = {entry["source_id"] for entry in source_map_entries if entry.get("source_id")}
        if not source_map_entries:
            semantic_failures.append("notes/source_map.md has no source_id rows")
        for entry in source_map_entries:
            entry_label = entry.get("source_id") or f"line {entry.get('__line__', '?')}"
            for required_field in SOURCE_REQUIRED_FIELDS:
                if not entry.get(required_field):
                    semantic_failures.append(
                        f"notes/source_map.md entry {entry_label} missing source field: {required_field}"
                    )
            read_state = entry.get("read_state", "").lower()
            if read_state and read_state not in SOURCE_READ_STATES:
                semantic_failures.append(
                    f"notes/source_map.md entry {entry_label} has unsupported read_state: {entry.get('read_state')}"
                )
            if entry.get("evidence_ids"):
                semantic_failures.append(
                    f"notes/source_map.md entry {entry_label} uses evidence_ids; use evidence_card_ids for source-to-ledger links"
                )
            source_evidence_refs = split_id_values(entry.get("evidence_card_ids", ""))
            if source_evidence_refs:
                source_map_evidence_card_refs[entry_label] = source_evidence_refs

    if research_path.is_file():
        for required_field in RESEARCH_BRIEF_REQUIRED_FIELDS:
            if not re.search(rf"(?im)^\s*{re.escape(required_field)}\s*:\s*\S+", research_text):
                semantic_failures.append(f"notes/research_brief.md missing planning field: {required_field}")

    if evidence_path.is_file():
        ledger_entries = evidence_entries(evidence_text)
        structured_ledger_ids = {entry["claim_id"] for entry in ledger_entries if entry.get("claim_id")}
        ledger_claims = {
            entry["claim_id"]: entry.get("claim", "")
            for entry in ledger_entries
            if entry.get("claim_id")
        }
        ledger_ids_by_source: dict[str, set[str]] = {}
        if not ledger_ids or not ledger_entries:
            semantic_failures.append("notes/evidence_ledger.md has no claim_id or EL-/EV-style evidence id")
        for entry in ledger_entries:
            entry_label = entry.get("claim_id") or f"line {entry.get('__line__', '?')}"
            for required_field in EVIDENCE_REQUIRED_FIELDS:
                if not entry.get(required_field):
                    semantic_failures.append(
                        f"notes/evidence_ledger.md entry {entry_label} missing evidence field: {required_field}"
                    )
            if not (entry.get("source_ref") or entry.get("source_id")):
                semantic_failures.append(
                    f"notes/evidence_ledger.md entry {entry_label} missing evidence field: source_ref/source_id"
                )
            source_ref = entry.get("source_ref") or entry.get("source_id")
            if source_ref and source_map_ids and source_ref not in source_map_ids:
                semantic_failures.append(
                    f"notes/evidence_ledger.md entry {entry_label} references source not in notes/source_map.md: {source_ref}"
                )
            if source_ref and entry.get("claim_id"):
                ledger_ids_by_source.setdefault(source_ref, set()).add(entry["claim_id"])
            status = entry.get("status", "").lower()
            support_state = entry.get("support_state", "").lower()
            support_value = status or support_state
            if not support_value:
                semantic_failures.append(
                    f"notes/evidence_ledger.md entry {entry_label} missing evidence field: status/support_state"
                )
            confidence = entry.get("confidence", "").lower()
            evidence_type = entry.get("evidence_type", "").lower()
            teaching_uses = [
                value.strip().lstrip("- ")
                for value in entry.get("teaching_use", "").split(",")
                if value.strip()
            ]
            if status and status not in EVIDENCE_STATUS_STATES:
                semantic_failures.append(
                    f"notes/evidence_ledger.md entry {entry_label} has unsupported status: {entry.get('status')}"
                )
            if support_state and support_state not in EVIDENCE_SUPPORT_STATES:
                semantic_failures.append(
                    f"notes/evidence_ledger.md entry {entry_label} has unsupported support_state: {entry.get('support_state')}"
                )
            if confidence and confidence not in EVIDENCE_CONFIDENCE_STATES:
                semantic_failures.append(
                    f"notes/evidence_ledger.md entry {entry_label} has unsupported confidence: {entry.get('confidence')}"
                )
            if evidence_type and evidence_type not in EVIDENCE_TYPES:
                semantic_failures.append(
                    f"notes/evidence_ledger.md entry {entry_label} has unsupported evidence_type: {entry.get('evidence_type')}"
                )
            for teaching_use in teaching_uses:
                if teaching_use not in EVIDENCE_TEACHING_USES:
                    semantic_failures.append(
                        f"notes/evidence_ledger.md entry {entry_label} has unsupported teaching_use: {teaching_use}"
                    )
            if support_value in {"accepted", "strong"} and confidence in {"inferred", "unknown"}:
                semantic_failures.append(
                    f"notes/evidence_ledger.md entry {entry_label} cannot be accepted with confidence: {entry.get('confidence')}"
                )
        for source_label, source_evidence_refs in source_map_evidence_card_refs.items():
            for evidence_card_id in source_evidence_refs:
                if structured_ledger_ids and evidence_card_id not in structured_ledger_ids:
                    semantic_failures.append(
                        "notes/source_map.md entry "
                        f"{source_label} references evidence_card_id not in notes/evidence_ledger.md: {evidence_card_id}"
                    )
        for source_entry in source_map_entries:
            source_id = source_entry.get("source_id")
            if not source_id:
                continue
            must_preserve = field_block_value(source_entry, "must_preserve")
            if not must_preserve:
                continue
            source_evidence_refs = source_map_evidence_card_refs.get(source_id, set())
            source_ledger_ids = ledger_ids_by_source.get(source_id, set())
            if not source_evidence_refs:
                semantic_failures.append(
                    "notes/source_map.md entry "
                    f"{source_id} has must_preserve details but no evidence_card_ids"
                )
                continue
            if not (source_evidence_refs & source_ledger_ids):
                semantic_failures.append(
                    "notes/source_map.md entry "
                    f"{source_id} must_preserve details are not linked to same-source Evidence Ledger claims"
                )
        accepted_must_preserve_evidence_ids = accepted_must_preserve_ids(
            ledger_entries, source_map_evidence_card_refs
        )

    if citation_path.is_file():
        citation_entry_rows = citation_entries(citation_text)
        citation_ids = set()
        for entry in citation_entry_rows:
            citation_ids.update(split_id_values(entry.get("evidence_ids", "")))
        visible_delivery_ids = evidence_ids(
            final_text
            + "\n"
            + "\n".join(read_text(root / chapter) for chapter in chapters if (root / chapter).is_file())
        )
        missing_from_audit = accepted_must_preserve_evidence_ids - citation_ids - visible_delivery_ids
        if missing_from_audit:
            semantic_failures.append(
                "accepted must_preserve evidence is missing from notes/citation_audit.md or visible final delivery: "
                + ", ".join(sorted(missing_from_audit))
            )
        for evidence_id in sorted(accepted_must_preserve_evidence_ids):
            if has_claim_content_resolution(
                evidence_resolution_text(citation_entry_rows, evidence_id) + "\n" + decisions_text,
                evidence_id=evidence_id,
            ):
                continue
            claim = ledger_claims.get(evidence_id, "")
            target_text = target_text_for_evidence(
                root,
                citation_entries_=citation_entry_rows,
                evidence_id=evidence_id,
                chapters=chapters,
                final_text=final_text,
            )
            if claim and not carries_claim_content(claim, target_text):
                semantic_failures.append(
                    "accepted must_preserve evidence lacks claim content in cited chapter/final target: "
                    f"{evidence_id}"
                )

    if tree_path.is_file() and not TREE_RE.search(tree_text):
        semantic_failures.append("notes/research_tree.md does not record research nodes, status, next action, or stop condition")

    if knowledge_path.is_file():
        if not re.search(r"\b(lock|locked|ready|core|spine|mechanism|model|evidence_ids|知识|机制|主干)\b", knowledge_text, re.I):
            semantic_failures.append("notes/knowledge_model.md does not show a locked/core model state")
        if structured_ledger_ids and not (model_ids & structured_ledger_ids):
            semantic_failures.append("notes/knowledge_model.md does not reference any evidence id from notes/evidence_ledger.md")
        for evidence_id in model_ids:
            if structured_ledger_ids and evidence_id not in structured_ledger_ids:
                semantic_failures.append(
                    f"notes/knowledge_model.md references evidence not in notes/evidence_ledger.md: {evidence_id}"
                )
        for row in value_rows(
            knowledge_text,
            {
                "spine",
                "core_spine",
                "concept",
                "mechanism",
                "comparison_set",
                "misconception",
                "anchor",
                "can_transfer_to",
            },
        ):
            row_label = (
                row.get("spine")
                or row.get("core_spine")
                or row.get("concept")
                or row.get("mechanism")
                or row.get("comparison_set")
                or row.get("misconception")
                or row.get("anchor")
                or row.get("can_transfer_to")
                or f"line {row.get('__line__', '?')}"
            )
            support_state = (row.get("support_state") or row.get("core_spine_support_state") or "").lower()
            if support_state and support_state not in KNOWLEDGE_SUPPORT_STATES:
                semantic_failures.append(
                    f"notes/knowledge_model.md entry {row_label} has unsupported support_state: {support_state}"
                )
            row_ids = split_id_values(row.get("evidence_ids") or row.get("core_spine_evidence_ids") or "")
            if support_state == "supported" and not row_ids:
                semantic_failures.append(
                    f"notes/knowledge_model.md entry {row_label} is supported but has no evidence_ids"
                )
            for evidence_id in row_ids:
                if structured_ledger_ids and evidence_id not in structured_ledger_ids:
                    semantic_failures.append(
                        f"notes/knowledge_model.md entry {row_label} references evidence not in notes/evidence_ledger.md: {evidence_id}"
                    )
        unresolved = unresolved_weak_evidence_refs(model_ids, weak_evidence_ids(ledger_entries), knowledge_text)
        if unresolved:
            semantic_failures.append(
                "notes/knowledge_model.md uses weak evidence without uncertainty or integrator action: "
                + ", ".join(sorted(unresolved))
            )
        missing_from_model = accepted_must_preserve_evidence_ids - model_ids
        if missing_from_model:
            semantic_failures.append(
                "accepted must_preserve evidence is missing from notes/knowledge_model.md: "
                + ", ".join(sorted(missing_from_model))
            )

    if chapter_plan_path.is_file():
        rows = chapter_rows(chapter_plan_text)
        if not rows:
            semantic_failures.append("notes/chapter_plan.md has no chapter_id rows")
        manifest_rows = manifest_chapter_rows(manifest_text)
        if rows and not manifest_rows:
            semantic_failures.append("manifest.yaml has no chapters projection from notes/chapter_plan.md")
        elif rows and manifest_chapter_signature(manifest_rows) != plan_chapter_signature(rows):
            semantic_failures.append("manifest.yaml chapters do not match notes/chapter_plan.md rows")
        for _, _, output_path in manifest_chapter_signature(manifest_rows):
            if output_path and output_path not in index_text:
                semantic_failures.append(f"index.md reading order missing manifest chapter link: {output_path}")
        for row in rows:
            row_label = row.get("chapter_id") or f"line {row.get('__line__', '?')}"
            for required_field in CHAPTER_REQUIRED_FIELDS:
                if not row.get(required_field):
                    semantic_failures.append(
                        f"notes/chapter_plan.md row {row_label} missing lesson-plan field: {required_field}"
                    )
            if METADATA_CHAPTER_RE.search(row.get("__text__", "")):
                semantic_failures.append(
                    f"notes/chapter_plan.md row {row_label} appears to allocate delivery metadata as a chapter"
                )
            elif CHAPTER_00_RE.search(row.get("chapter_id", "")):
                warnings.append(
                    f"notes/chapter_plan.md row {row_label} uses a leading chapter id; keep it only when it teaches a substantive reference frame or knowledge overview"
                )
            output_path = row.get("output_path", "")
            if output_path and (not output_path.startswith("chapters/") or output_path not in chapters):
                semantic_failures.append(
                    f"notes/chapter_plan.md row {row_label} output_path is not an existing chapter file: {output_path}"
                )
        if REFERENCE_FRAME_RE.search(evidence_text) and not REFERENCE_FRAME_RE.search(chapter_plan_text):
            warnings.append(
                "reference frame appears in evidence ledger but is not visible in notes/chapter_plan.md"
            )
        unresolved_reference_gaps = unresolved_reference_frame_gap_ids(
            ledger_entries, chapter_plan_text + "\n" + citation_text + "\n" + decisions_text
        )
        if unresolved_reference_gaps:
            semantic_failures.append(
                "load-bearing reference-frame or precision gap lacks chapter/citation/integrator action: "
                + ", ".join(sorted(unresolved_reference_gaps))
            )
        chapter_plan_ids = evidence_ids(chapter_plan_text)
        missing_from_plan = accepted_must_preserve_evidence_ids - chapter_plan_ids
        if missing_from_plan:
            semantic_failures.append(
                "accepted must_preserve evidence is missing from notes/chapter_plan.md: "
                + ", ".join(sorted(missing_from_plan))
            )
        for row in rows:
            chapter_id = row.get("chapter_id", "")
            if not chapter_id:
                continue
            output_path = row.get("output_path", "")
            sidecar_dir = root / "notes" / "agent_outputs" / "teaching_composer" / chapter_id
            sidecar_files = sorted(path for path in sidecar_dir.glob("*.md") if path.is_file()) if sidecar_dir.is_dir() else []
            sidecar_refs = [
                path.relative_to(root).as_posix()
                for path in sidecar_files
            ]
            has_chapter_decision = any(
                has_integrator_decision(
                    decisions_text,
                    source_artifact=ref,
                    target=output_path,
                    section_id=chapter_id,
                )
                for ref in sidecar_refs
            )
            has_chapter_fallback = has_chapter_fallback_decision(
                decisions_text + "\n" + trace_text,
                target=output_path,
                section_id=chapter_id,
            )
            if not sidecar_files and not has_chapter_fallback:
                semantic_failures.append(
                    "chapter_id has no Teaching Composer sidecar under "
                    f"notes/agent_outputs/teaching_composer/{chapter_id}/: {chapter_id}"
                )
            for sidecar_file, sidecar_ref in zip(sidecar_files, sidecar_refs):
                sidecar_text = read_text(sidecar_file)
                if not re.search(r"(?im)^\s*agent_type\s*:\s*teaching_composer\s*$", sidecar_text):
                    semantic_failures.append(f"Teaching Composer sidecar missing agent_type: teaching_composer: {sidecar_ref}")
                for input_artifact in ("notes/knowledge_model.md", "notes/chapter_plan.md", "notes/evidence_ledger.md"):
                    if input_artifact not in sidecar_text:
                        semantic_failures.append(
                            f"Teaching Composer sidecar missing required input artifact {input_artifact}: {sidecar_ref}"
                        )
                if output_path and output_path not in sidecar_text:
                    semantic_failures.append(
                        f"Teaching Composer sidecar does not target chapter output_path {output_path}: {sidecar_ref}"
                    )
            if sidecar_files and not has_chapter_decision and not has_chapter_fallback:
                semantic_failures.append(
                    f"Teaching Composer sidecar lacks integrator decision for chapter_id {chapter_id}: "
                    + ", ".join(sidecar_refs)
                )
            row_required_ids = evidence_ids(row.get("__text__", ""))
            if structured_ledger_ids:
                row_required_ids &= structured_ledger_ids
            if row.get("required_anchors") and not row_required_ids:
                warnings.append(
                    "notes/chapter_plan.md row "
                    f"{chapter_id} has required_anchors without evidence ids; "
                    "sidecar and final coverage checks are limited to explicit resolutions"
                )
            if row_required_ids:
                sidecar_text = "\n".join(read_text(path) for path in sidecar_files)
                sidecar_ids = evidence_ids(sidecar_text)
                missing_from_sidecar = row_required_ids - sidecar_ids
                if missing_from_sidecar and not has_chapter_fallback:
                    semantic_failures.append(
                        f"Teaching Composer sidecar does not cover chapter_plan required evidence for {chapter_id}: "
                        + ", ".join(sorted(missing_from_sidecar))
                    )

                title = row.get("title", "")
                section_tokens = [chapter_id, output_path, title, "final/final_merged.md"]
                citation_ids, citation_resolution_text = section_resolution_ids(citation_entry_rows, section_tokens)
                chapter_text = read_text(root / output_path) if output_path and (root / output_path).is_file() else ""
                visible_ids = evidence_ids(chapter_text + "\n" + final_text)
                resolved_ids = citation_ids | visible_ids
                missing_from_final_resolution = row_required_ids - resolved_ids
                unresolved_ids = [
                    evidence_id
                    for evidence_id in sorted(missing_from_final_resolution)
                    if not has_anchor_resolution(
                        citation_resolution_text + "\n" + decisions_text,
                        evidence_id=evidence_id,
                        candidates=section_tokens,
                    )
                ]
                if unresolved_ids:
                    semantic_failures.append(
                        f"chapter_plan required evidence lacks chapter/final citation or integrator resolution for {chapter_id}: "
                        + ", ".join(unresolved_ids)
                    )
                content_unresolved_ids = []
                for evidence_id in sorted(row_required_ids):
                    if has_claim_content_resolution(
                        citation_resolution_text + "\n" + decisions_text,
                        evidence_id=evidence_id,
                        candidates=section_tokens,
                    ):
                        continue
                    claim = ledger_claims.get(evidence_id, "")
                    target_text = target_text_for_evidence(
                        root,
                        citation_entries_=citation_entry_rows,
                        evidence_id=evidence_id,
                        output_path=output_path,
                        candidates=section_tokens,
                        chapters=[output_path] if output_path else [],
                        final_text=final_text,
                    )
                    if claim and not carries_claim_content(claim, target_text):
                        content_unresolved_ids.append(evidence_id)
                if content_unresolved_ids:
                    semantic_failures.append(
                        f"chapter_plan required evidence lacks claim content in cited chapter/final target for {chapter_id}: "
                        + ", ".join(content_unresolved_ids)
                    )

    for chapter in chapters:
        chapter_path = root / chapter
        chapter_head = read_text(chapter_path)[:800]
        if METADATA_CHAPTER_RE.search(chapter_head):
            semantic_failures.append(f"chapter appears to be delivery metadata rather than knowledge content: {chapter}")
        elif re.match(r"chapters/0?0(?:[_\-.]|$)", chapter, re.I):
            warnings.append(
                f"leading chapter path should teach a substantive reference frame or route metadata to index/notes: {chapter}"
            )

    if decisions_path.is_file():
        if not PROMOTION_RE.search(decisions_text):
            semantic_failures.append(
                "notes/integrator_decisions.md does not record promotion, acceptance, rejection, revision, or discard"
            )
        if not agent_outputs and not has_recorded_fallback(decisions_text + "\n" + trace_text):
            semantic_failures.append(
                "notes/agent_outputs/ has no agent outputs, but no traceable agent runtime/tool/worker fallback artifact and integrator decision were recorded"
            )
        for agent_output in agent_outputs:
            name = Path(agent_output).name
            stem = Path(agent_output).stem
            if name not in decisions_text and stem not in decisions_text:
                warnings.append(f"agent output not explicitly referenced by integrator decisions: {agent_output}")

    if citation_path.is_file():
        citation_entry_rows = citation_entries(citation_text)
        if not citation_entry_rows:
            semantic_failures.append("notes/citation_audit.md has no claim_or_section rows")
        if structured_ledger_ids and not any(
            split_id_values(entry.get("evidence_ids", "")) & structured_ledger_ids for entry in citation_entry_rows
        ):
            semantic_failures.append("notes/citation_audit.md does not reference any evidence id from notes/evidence_ledger.md")
        for entry in citation_entry_rows:
            entry_label = entry.get("claim_or_section") or f"line {entry.get('__line__', '?')}"
            for required_field in CITATION_REQUIRED_FIELDS:
                if not entry.get(required_field):
                    semantic_failures.append(
                        f"notes/citation_audit.md entry {entry_label} missing citation field: {required_field}"
                    )
            support_state = entry.get("support_state", "").lower()
            integrator_action = entry.get("integrator_action", "").lower()
            if support_state and support_state not in CITATION_SUPPORT_STATES:
                semantic_failures.append(
                    f"notes/citation_audit.md entry {entry_label} has unsupported support_state: {entry.get('support_state')}"
                )
            if integrator_action and integrator_action not in CITATION_ACTIONS:
                semantic_failures.append(
                    f"notes/citation_audit.md entry {entry_label} has unsupported integrator_action: {entry.get('integrator_action')}"
                )
            if support_state in {"partial", "inferred", "contradicted", "missing"} and integrator_action == "accept":
                semantic_failures.append(
                    f"notes/citation_audit.md entry {entry_label} cannot accept unsupported citation state: {support_state}"
                )
            if support_state == "supported" and integrator_action not in {"accept", "revise"}:
                semantic_failures.append(
                    f"notes/citation_audit.md entry {entry_label} has resolution action despite supported citation state: {integrator_action}"
                )
            for evidence_id in split_id_values(entry.get("evidence_ids", "")):
                if structured_ledger_ids and evidence_id not in structured_ledger_ids:
                    semantic_failures.append(
                        f"notes/citation_audit.md entry {entry_label} references evidence not in notes/evidence_ledger.md: {evidence_id}"
                    )
            for source_id in split_id_values(entry.get("source_ids", "")):
                if source_map_ids and source_id not in source_map_ids:
                    semantic_failures.append(
                        f"notes/citation_audit.md entry {entry_label} references source not in notes/source_map.md: {source_id}"
                    )
            unresolved = unresolved_weak_evidence_refs(
                split_id_values(entry.get("evidence_ids", "")),
                weak_evidence_ids(ledger_entries),
                entry.get("__text__", "") + "\n" + integrator_action,
            )
            if unresolved and integrator_action not in CITATION_RESOLUTION_ACTIONS:
                semantic_failures.append(
                    "notes/citation_audit.md uses weak evidence without support-state action: "
                    + ", ".join(sorted(unresolved))
                )

    if final_path.is_file() and PLACEHOLDER_RE.search(final_text):
        semantic_failures.append("final/final_merged.md contains placeholder source or citation markers")

    missing_trace_outputs: list[str] = []
    for agent_output in agent_outputs:
        text = read_text(root / agent_output)
        if not TRACE_UPDATE_RE.search(text):
            missing_trace_outputs.append(agent_output)
        if not re.search(r"\bagent_type\s*:", text):
            semantic_failures.append(f"agent output missing agent_type: {agent_output}")
    if missing_trace_outputs:
        semantic_failures.append("agent outputs missing Trace Update: " + ", ".join(missing_trace_outputs))

    if trace_path.is_file() and not re.search(r"\b(route|phase|agent|current_state|trace)\b", trace_text, re.I):
        semantic_failures.append("notes/process_trace.md does not record route, phase, agent, or trace state")

    present = count_present(CANONICAL_FILES, root)
    present.extend(count_present(CANONICAL_DIRS, root, directory=True))

    ok = not missing and not empty_files and not semantic_failures
    return {
        "root": str(root),
        "ok": ok,
        "missing": missing,
        "present": present,
        "empty_files": empty_files,
        "semantic_failures": semantic_failures,
        "warnings": warnings,
        "chapters": chapters,
        "agent_outputs": agent_outputs,
        "evidence_ids": sorted(ledger_ids),
        "diagnostics": {
            "canonical_files": len(CANONICAL_FILES),
            "canonical_dirs": len(CANONICAL_DIRS),
            "canonical_items_present": len(present),
            "chapters": len(chapters),
            "agent_outputs": len(agent_outputs),
        },
    }


def print_text(result: dict) -> None:
    print(f"root: {result['root']}")
    print(f"canonical_items: {result['diagnostics']['canonical_items_present']}")
    print(f"chapters: {result['diagnostics']['chapters']}")
    print(f"agent_outputs: {result['diagnostics']['agent_outputs']}")
    print(f"evidence_ids: {len(result['evidence_ids'])}")
    for label in ("warnings", "missing", "empty_files", "semantic_failures"):
        if result[label]:
            print(f"{label}:")
            for item in result[label]:
                print(f"  - {item}")
    print("ok" if result["ok"] else "not ok")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate MasterZhuyan DeepResearch artifacts for semantic integration."
    )
    parser.add_argument("--root", required=True, help="Longform root directory to validate.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable validation JSON.")
    args = parser.parse_args(argv)

    result = validate_root(Path(args.root))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
