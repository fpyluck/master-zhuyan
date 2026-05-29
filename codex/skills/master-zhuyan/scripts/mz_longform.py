#!/usr/bin/env python3
"""Create, validate, and merge MasterZhuyan longform projects.

This helper is intentionally small. It gives Codex-like environments a deterministic
fallback container when longform-composer is unavailable and materializes the same
chapter_plan -> Teaching Composer sidecar contract. MasterZhuyan still owns the
DeepResearch notes and teaching synthesis.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

PLACEHOLDER_MARKERS = [
    "本章内容待根据用户资料写入。",
    "本章正文结构由 MasterZhuyan chapter_plan 决定，待根据用户资料写入。",
    "本章正文待根据 locked Knowledge Model 和 required_anchors 写入。",
    "待根据用户资料写入",
    "待根据 locked Knowledge Model",
]
CHAPTER_ID_SAFE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


@dataclass
class Chapter:
    id: str
    title: str
    file: str
    status: str = "planned"


@dataclass
class ChapterPlanRow:
    chapter_id: str
    title: str
    purpose: str
    input_refs: str
    required_anchors: str
    output_path: str
    completion_criteria: str


def slugify(value: str, fallback: str = "chapter") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or fallback


def load_manifest(root: Path) -> dict[str, Any]:
    path = root / "manifest.yaml"
    if not path.exists():
        raise FileNotFoundError(f"manifest not found: {path}")
    text = path.read_text(encoding="utf-8")
    if yaml is None:
        return parse_simple_manifest(text)
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("manifest.yaml must contain a mapping")
    return data


def dump_manifest(data: dict[str, Any]) -> str:
    if yaml is not None:
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    return dump_simple_yaml(data)


def parse_simple_manifest(text: str) -> dict[str, Any]:
    # Fallback parser for the exact shape produced by this script.
    data: dict[str, Any] = {"chapters": []}
    current: dict[str, str] | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            current = {}
            data["chapters"].append(current)
            rest = line[4:]
            if ":" in rest:
                key, value = rest.split(":", 1)
                current[key.strip()] = value.strip().strip('"')
        elif line.startswith("    ") and current is not None and ":" in line:
            key, value = line.strip().split(":", 1)
            current[key.strip()] = value.strip().strip('"')
        elif ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "chapters" and value == "":
                data.setdefault("chapters", [])
                current = None
                continue
            data[key] = value.strip('"')
    return data


def dump_simple_yaml(data: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if key == "chapters" and isinstance(value, list):
            lines.append("chapters:")
            for chapter in value:
                lines.append(f"  - id: {chapter['id']}")
                lines.append(f"    title: {chapter['title']}")
                lines.append(f"    file: {chapter['file']}")
                lines.append(f"    status: {chapter.get('status', 'planned')}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def parse_chapters(raw: str) -> list[Chapter]:
    titles = [part.strip() for part in raw.split("|") if part.strip()]
    if not titles:
        raise ValueError("at least one chapter title is required")
    chapters: list[Chapter] = []
    seen: set[str] = set()
    for index, title in enumerate(titles, start=1):
        base = slugify(title, fallback=f"chapter-{index}")
        slug = base
        suffix = 2
        while slug in seen:
            slug = f"{base}-{suffix}"
            suffix += 1
        seen.add(slug)
        chapter_id = f"ch{index:02d}"
        file = f"chapters/{index:02d}-{slug}.md"
        chapters.append(Chapter(id=chapter_id, title=title, file=file))
    return chapters


def parse_chapter_plan_rows(text: str) -> list[ChapterPlanRow]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    field_re = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")
    for line in text.splitlines():
        match = field_re.match(line)
        if not match:
            continue
        key = match.group(1).lower()
        value = match.group(2).strip()
        if key == "chapter_id":
            if current is not None:
                rows.append(current)
            current = {"chapter_id": value}
        elif current is not None:
            current[key] = value
    if current is not None:
        rows.append(current)

    parsed: list[ChapterPlanRow] = []
    required = (
        "chapter_id",
        "title",
        "purpose",
        "input_refs",
        "required_anchors",
        "output_path",
        "completion_criteria",
    )
    for row in rows:
        missing = [field for field in required if not row.get(field)]
        label = row.get("chapter_id") or "unknown"
        if missing:
            raise ValueError(f"chapter_plan row {label} missing fields: {', '.join(missing)}")
        if not CHAPTER_ID_SAFE_RE.match(row["chapter_id"]):
            raise ValueError(f"chapter_plan row {label} has unsafe chapter_id")
        parsed.append(
            ChapterPlanRow(
                chapter_id=row["chapter_id"],
                title=row["title"],
                purpose=row["purpose"],
                input_refs=row["input_refs"],
                required_anchors=row["required_anchors"],
                output_path=row["output_path"],
                completion_criteria=row["completion_criteria"],
            )
        )
    return parsed


def normalize_input_artifacts(raw: str) -> str:
    artifacts: list[str] = []
    for value in [*raw.split(","), "notes/knowledge_model.md", "notes/chapter_plan.md", "notes/evidence_ledger.md"]:
        item = value.strip()
        if item and item not in artifacts:
            artifacts.append(item)
    return ", ".join(artifacts)


def manifest_chapter_entry(row: ChapterPlanRow, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    status = "planned"
    if existing and isinstance(existing.get("status"), str) and existing["status"]:
        status = existing["status"]
    return {
        "id": row.chapter_id,
        "title": row.title,
        "file": row.output_path,
        "status": status,
    }


def sync_manifest_chapters(manifest: dict[str, Any], rows: list[ChapterPlanRow]) -> dict[str, Any]:
    existing_chapters = manifest.get("chapters", [])
    existing_by_id: dict[str, dict[str, Any]] = {}
    existing_by_file: dict[str, dict[str, Any]] = {}
    if isinstance(existing_chapters, list):
        for chapter in existing_chapters:
            if not isinstance(chapter, dict):
                continue
            chapter_id = chapter.get("id")
            file_rel = chapter.get("file")
            if isinstance(chapter_id, str) and chapter_id:
                existing_by_id[chapter_id] = chapter
            if isinstance(file_rel, str) and file_rel:
                existing_by_file[file_rel] = chapter

    synced = []
    matched_existing_keys: set[tuple[str, str]] = set()
    for row in rows:
        existing = existing_by_id.get(row.chapter_id) or existing_by_file.get(row.output_path)
        if existing:
            matched_existing_keys.add((str(existing.get("id", "")), str(existing.get("file", ""))))
        synced.append(manifest_chapter_entry(row, existing))

    orphaned_non_planned = []
    for chapter in existing_chapters if isinstance(existing_chapters, list) else []:
        if not isinstance(chapter, dict):
            continue
        chapter_id = str(chapter.get("id", ""))
        file_rel = str(chapter.get("file", ""))
        if (chapter_id, file_rel) in matched_existing_keys:
            continue
        if chapter.get("status", "planned") != "planned":
            orphaned_non_planned.append(f"{chapter_id or file_rel or 'unknown'}")
    if orphaned_non_planned:
        raise ValueError(
            "cannot drop non-planned manifest chapter entries: " + ", ".join(sorted(orphaned_non_planned))
        )

    synced_manifest = dict(manifest)
    synced_manifest["chapters"] = synced
    return synced_manifest


def render_index(manifest: dict[str, Any], *, preserve_tail: str | None = None) -> str:
    title = manifest.get("title", "MasterZhuyan Longform Project")
    chapter_emphasis = manifest.get("chapter_emphasis", "understanding")
    depth = manifest.get("depth", "systematic")
    audience = manifest.get("audience", "general learner")
    chapters = manifest.get("chapters", [])

    lines = [
        f"# {title}",
        "",
        "## 阅读顺序",
        "",
    ]
    if isinstance(chapters, list):
        for chapter in chapters:
            if isinstance(chapter, dict):
                lines.append(f"- [{chapter.get('title', 'untitled')}]({chapter.get('file', 'chapters/unknown.md')})")
    if preserve_tail is not None:
        tail = preserve_tail.rstrip()
        if tail:
            lines.append("")
            lines.append(tail)
    else:
        lines += [
            "",
            "## 交付说明",
            "",
            f"章节重点：{chapter_emphasis}",
            f"深度：{depth}",
            f"受众：{audience}",
            "",
        ]
    return "\n".join(lines)


def write_index(root: Path, manifest: dict[str, Any], *, preserve_tail: str | None = None) -> None:
    (root / "index.md").write_text(render_index(manifest, preserve_tail=preserve_tail), encoding="utf-8")


def chapter_shell_text(row: ChapterPlanRow) -> str:
    return "\n".join(
        [
            f"# {row.title}",
            "",
            "> purpose: 待由 notes/chapter_plan.md 的 purpose / required_anchors / completion_criteria 写入。",
            "",
            "本章正文待根据 locked Knowledge Model 和 required_anchors 写入。",
            "",
        ]
    )


def ensure_chapter_shell(root: Path, row: ChapterPlanRow) -> Path:
    chapter_path = root / row.output_path
    chapter_path.parent.mkdir(parents=True, exist_ok=True)
    if not chapter_path.exists():
        chapter_path.write_text(chapter_shell_text(row), encoding="utf-8")
    return chapter_path


def manifest_chapter_signature(manifest: dict[str, Any]) -> list[tuple[str, str, str]]:
    chapters = manifest.get("chapters", [])
    if not isinstance(chapters, list):
        return []
    signature: list[tuple[str, str, str]] = []
    for chapter in chapters:
        if not isinstance(chapter, dict):
            return []
        chapter_id = chapter.get("id")
        title = chapter.get("title")
        file_rel = chapter.get("file")
        if not all(isinstance(value, str) for value in (chapter_id, title, file_rel)):
            return []
        signature.append((chapter_id, title, file_rel))
    return signature


def chapter_plan_signature(rows: list[ChapterPlanRow]) -> list[tuple[str, str, str]]:
    return [(row.chapter_id, row.title, row.output_path) for row in rows]


def manifest_matches_chapter_plan(manifest: dict[str, Any], rows: list[ChapterPlanRow]) -> bool:
    return manifest_chapter_signature(manifest) == chapter_plan_signature(rows)


def load_chapter_plan_rows_if_present(root: Path) -> list[ChapterPlanRow]:
    plan_path = root / "notes" / "chapter_plan.md"
    if not plan_path.is_file():
        return []
    return parse_chapter_plan_rows(plan_path.read_text(encoding="utf-8"))


def write_teaching_composer_package(root: Path, row: ChapterPlanRow, *, overwrite: bool = False) -> Path:
    agent_suffix = re.sub(r"[^A-Za-z0-9_.-]+", "-", row.chapter_id).strip("-") or "chapter"
    agent_id = f"teaching_composer_{agent_suffix}"
    output = root / "notes" / "agent_outputs" / "teaching_composer" / row.chapter_id / f"{agent_id}.md"
    if output.exists() and not overwrite:
        return output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "\n".join(
            [
                f"agent_id: {agent_id}",
                "agent_type: teaching_composer",
                f"mission: draft chapter {row.chapter_id} from its locked chapter_plan row",
                f"input_artifacts: {normalize_input_artifacts(row.input_refs)}",
                f"output_targets: {row.output_path}",
                "",
                f"## Teaching Composer Work Package: {row.chapter_id}",
                "",
                f"title: {row.title}",
                f"purpose: {row.purpose}",
                f"required_anchors: {row.required_anchors}",
                f"completion_criteria: {row.completion_criteria}",
                "",
                "draft_status: pending_agent_or_fallback",
                "evidence_ids_used: pending",
                "required_anchors_covered: pending",
                "required_anchors_omitted: none",
                "integrator_action: pending_integrator_review",
                "",
                "canonical_promotion_hints:",
                f"  promote_to: {row.output_path}",
                f"  sections_or_entries: {row.chapter_id}",
                "  edits_needed: integrator review before canonical chapter write",
                "trace_update:",
                f"  artifacts_read: {normalize_input_artifacts(row.input_refs)}",
                f"  artifacts_written: notes/agent_outputs/teaching_composer/{row.chapter_id}/{agent_id}.md",
                f"  canonical_targets: {row.output_path}",
                f"  strong_findings: {row.required_anchors}",
                "  open_branches: none",
                "  handoff_suggestion: integrator",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return output


def init_project(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    chapters = parse_chapters(args.chapters)
    for subdir in ["chapters", "final", "notes"]:
        (root / subdir).mkdir(parents=True, exist_ok=True)

    manifest = {
        "title": args.title,
        "chapter_emphasis": args.chapter_emphasis,
        "audience": args.audience,
        "depth": args.depth,
        "language": args.language,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "drafting",
        "chapters": [chapter.__dict__ for chapter in chapters],
    }
    (root / "manifest.yaml").write_text(dump_manifest(manifest), encoding="utf-8")
    write_index(root, manifest)

    for chapter in chapters:
        chapter_path = root / chapter.file
        chapter_path.write_text(chapter_shell_text(ChapterPlanRow(
            chapter_id=chapter.id,
            title=chapter.title,
            purpose="待由 notes/chapter_plan.md 的 purpose / required_anchors / completion_criteria 写入。",
            input_refs="notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md",
            required_anchors="待由 notes/chapter_plan.md 的 required_anchors 写入",
            output_path=chapter.file,
            completion_criteria="待由 notes/chapter_plan.md 的 completion_criteria 写入",
        )), encoding="utf-8")

    (root / "notes" / "process_trace.md").write_text(
        f"# Process Trace\n\n- fallback container initialized at {datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )
    print(f"initialized: {root}")
    return 0


def materialize_chapter_agents(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    plan_path = root / "notes" / "chapter_plan.md"
    if not plan_path.is_file():
        print(f"materialize failed: missing {plan_path}")
        return 1
    try:
        rows = parse_chapter_plan_rows(plan_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(f"materialize failed: {exc}")
        return 1
    if not rows:
        print("materialize failed: notes/chapter_plan.md has no chapter_id rows")
        return 1

    manifest_path = root / "manifest.yaml"
    if not manifest_path.is_file():
        print(f"materialize failed: missing {manifest_path}")
        return 1
    try:
        manifest = load_manifest(root)
    except Exception as exc:  # noqa: BLE001
        print(f"materialize failed: {exc}")
        return 1

    try:
        synced_manifest = sync_manifest_chapters(manifest, rows)
    except ValueError as exc:
        print(f"materialize failed: {exc}")
        return 1

    written = [write_teaching_composer_package(root, row, overwrite=args.overwrite) for row in rows]
    manifest_path.write_text(dump_manifest(synced_manifest), encoding="utf-8")
    existing_index_text = (root / "index.md").read_text(encoding="utf-8") if (root / "index.md").is_file() else ""
    preserve_tail = None
    if "## 交付说明" in existing_index_text:
        preserve_tail = "## 交付说明" + existing_index_text.split("## 交付说明", 1)[1]
    write_index(root, synced_manifest, preserve_tail=preserve_tail)
    shell_paths = [ensure_chapter_shell(root, row) for row in rows]
    trace_path = root / "notes" / "process_trace.md"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with trace_path.open("a", encoding="utf-8") as handle:
        handle.write("\n## Chapter Agent Work Packages\n\n")
        handle.write("default_flow: chapter_plan_row -> teaching_composer_sidecar -> integrator_promotion\n")
        handle.write(f"manifest_projection: {len(rows)} chapter_plan rows -> manifest.yaml + index.md\n")
        for path in written:
            rel = path.relative_to(root).as_posix()
            handle.write(f"- materialized: {rel}\n")
        for path in shell_paths:
            rel = path.relative_to(root).as_posix()
            handle.write(f"- chapter_shell: {rel}\n")

    for path in written:
        print(f"materialized: {path.relative_to(root).as_posix()}")
    for path in shell_paths:
        print(f"chapter shell ready: {path.relative_to(root).as_posix()}")
    return 0


def validate_project(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = load_manifest(root)
    except Exception as exc:  # noqa: BLE001
        print(f"validation failed: {exc}")
        return 1

    chapter_plan_rows: list[ChapterPlanRow] = []
    try:
        chapter_plan_rows = load_chapter_plan_rows_if_present(root)
    except ValueError as exc:
        errors.append(str(exc))

    for rel in ["manifest.yaml", "index.md", "chapters", "final", "notes"]:
        if not (root / rel).exists():
            errors.append(f"missing {rel}")
    if (root / "notes" / "chapter_plan.md").is_file():
        warnings.append(
            "semantic DeepResearch checks require: "
            f"python scripts/validate_deep_research_artifacts.py --root {root}"
        )
        if chapter_plan_rows and not manifest_matches_chapter_plan(manifest, chapter_plan_rows):
            errors.append("manifest chapters do not match notes/chapter_plan.md; run materialize-chapter-agents")

    chapters = manifest.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        errors.append("manifest has no chapters")
        chapters = []

    for chapter in chapters:
        if not isinstance(chapter, dict):
            errors.append("chapter entry is not a mapping")
            continue
        file_rel = chapter.get("file")
        title = chapter.get("title", "untitled")
        status = chapter.get("status", "planned")
        if not isinstance(file_rel, str):
            errors.append(f"chapter {title} has no file")
            continue
        path = root / file_rel
        if not path.exists():
            errors.append(f"missing chapter file: {file_rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"empty chapter file: {file_rel}")
        for marker in PLACEHOLDER_MARKERS:
            if marker in text:
                errors.append(f"chapter still contains scaffold text: {file_rel}")
                break
        if status not in {"planned", "draft", "reviewed", "done", "needs_revision"}:
            errors.append(f"invalid chapter status {status!r}: {file_rel}")

    if errors:
        print("validation failed")
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"warning: {warning}")
        return 1

    print("validation passed")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


def merge_project(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    manifest = load_manifest(root)
    try:
        chapter_plan_rows = load_chapter_plan_rows_if_present(root)
    except ValueError as exc:
        print(f"merge failed: {exc}")
        return 1
    if chapter_plan_rows and not manifest_matches_chapter_plan(manifest, chapter_plan_rows):
        print("merge failed: manifest chapters do not match notes/chapter_plan.md; run materialize-chapter-agents")
        return 1
    chapters = manifest.get("chapters", [])
    if not isinstance(chapters, list) or not chapters:
        print("merge failed: manifest has no chapters")
        return 1

    title = manifest.get("title", root.name)
    lines: list[str] = [f"# {title}", "", "## 目录", ""]
    for chapter in chapters:
        if isinstance(chapter, dict):
            lines.append(f"- {chapter.get('title', 'untitled')}")
    lines.append("")

    for chapter in chapters:
        if not isinstance(chapter, dict):
            continue
        file_rel = chapter.get("file")
        if not isinstance(file_rel, str):
            continue
        path = root / file_rel
        if not path.exists():
            print(f"merge failed: missing chapter file {file_rel}")
            return 1
        chapter_text = path.read_text(encoding="utf-8").strip()
        for marker in PLACEHOLDER_MARKERS:
            if marker in chapter_text:
                print(f"merge failed: chapter still contains scaffold text: {file_rel}")
                return 1
        lines.append("\n---\n")
        lines.append(chapter_text)
        lines.append("")

    final_dir = root / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    final_path = final_dir / "final_merged.md"
    final_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"merged: {final_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="initialize a longform project")
    init.add_argument("--root", required=True)
    init.add_argument("--title", required=True)
    init.add_argument("--chapter-emphasis", default="understanding")
    init.add_argument(
        "--chapters",
        required=True,
        help="initial Knowledge-Model-derived chapter titles separated by |; notes/chapter_plan.md is authoritative",
    )
    init.add_argument("--audience", default="general learner")
    init.add_argument("--depth", default="systematic")
    init.add_argument("--language", default="zh")
    init.set_defaults(func=init_project)

    validate = subparsers.add_parser("validate", help="validate a longform project")
    validate.add_argument("--root", required=True)
    validate.set_defaults(func=validate_project)

    merge = subparsers.add_parser("merge", help="merge chapters into final/final_merged.md")
    merge.add_argument("--root", required=True)
    merge.set_defaults(func=merge_project)

    materialize = subparsers.add_parser(
        "materialize-chapter-agents",
        help="create Teaching Composer sidecar work packages from notes/chapter_plan.md",
    )
    materialize.add_argument("--root", required=True)
    materialize.add_argument("--overwrite", action="store_true")
    materialize.set_defaults(func=materialize_chapter_agents)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
