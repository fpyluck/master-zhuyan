#!/usr/bin/env python3
"""Create, validate, and merge MasterZhuyan longform projects.

This helper is intentionally small. It gives filesystem-capable environments a deterministic
fallback when longform-composer is unavailable.
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
    "待根据用户资料写入",
]


@dataclass
class Chapter:
    id: str
    title: str
    file: str
    status: str = "planned"


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
            data[key.strip()] = value.strip().strip('"')
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


def init_project(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    chapters = parse_chapters(args.chapters)
    for subdir in ["chapters", "final", "logs", "sources"]:
        (root / subdir).mkdir(parents=True, exist_ok=True)

    manifest = {
        "title": args.title,
        "mode": args.mode,
        "audience": args.audience,
        "depth": args.depth,
        "language": args.language,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "drafting",
        "chapters": [chapter.__dict__ for chapter in chapters],
    }
    (root / "manifest.yaml").write_text(dump_manifest(manifest), encoding="utf-8")

    index_lines = [
        f"# {args.title}",
        "",
        "## 阅读顺序",
        "",
    ]
    for chapter in chapters:
        index_lines.append(f"- [{chapter.title}]({chapter.file})")
    index_lines += [
        "",
        "## 交付说明",
        "",
        f"模式：{args.mode}",
        f"深度：{args.depth}",
        f"受众：{args.audience}",
        "",
    ]
    (root / "index.md").write_text("\n".join(index_lines), encoding="utf-8")

    for chapter in chapters:
        chapter_path = root / chapter.file
        chapter_path.write_text(
            "\n".join(
                [
                    f"# {chapter.title}",
                    "",
                    "> chapter objective: 本章用于承载 MasterZhuyan 的系统学习内容。",
                    "",
                    "本章正文结构由 MasterZhuyan chapter_plan 决定，待根据用户资料写入。",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    (root / "logs" / "progress.md").write_text(
        f"# progress\n\n- initialized at {datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )
    print(f"initialized: {root}")
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

    for rel in ["manifest.yaml", "index.md", "chapters", "final", "logs"]:
        if not (root / rel).exists():
            errors.append(f"missing {rel}")

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
                warnings.append(f"chapter still contains scaffold text: {file_rel}")
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
        lines.append("\n---\n")
        lines.append(path.read_text(encoding="utf-8").strip())
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
    init.add_argument("--mode", default="understanding")
    init.add_argument("--chapters", required=True, help="chapter titles separated by |")
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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
