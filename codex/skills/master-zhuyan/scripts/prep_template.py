#!/usr/bin/env python3
"""Create, list, and explicitly match MasterZhuyan named prep-template files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
UNSAFE_FILENAME_RE = re.compile(r"[\\/\0<>:\"|?*]+")


@dataclass
class PrepTemplate:
    name: str
    path: Path
    aliases: list[str]
    source: str = "local"
    status: str = "active"


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, object] = {}
    current_key: str | None = None
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current_key:
            value = strip_quotes(raw[4:])
            bucket = data.setdefault(current_key, [])
            if isinstance(bucket, list):
                bucket.append(value)
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = strip_quotes(value)
            current_key = None
        else:
            data[key] = []
            current_key = key
    return data


def safe_filename(name: str) -> str:
    name = UNSAFE_FILENAME_RE.sub("-", name.strip())
    name = re.sub(r"\s+", "-", name).strip("-. ")
    return name or "prep-template"


def default_aliases(name: str) -> list[str]:
    """Return explicit activation aliases only; never include the bare name."""
    compact = name.strip()
    aliases = [
        f"{compact}式讲解",
        f"{compact}式",
        f"{compact}式输出",
        f"{compact}式备课",
        f"{compact}教案",
        f"{compact}模板",
        f"{compact}风格",
        f"按{compact}讲",
        f"按{compact}讲解",
        f"按{compact}教案",
        f"按{compact}风格",
        f"用{compact}讲",
        f"用{compact}讲解",
        f"用{compact}教案",
        f"用{compact}风格",
        f"以{compact}风格",
    ]
    seen: set[str] = set()
    unique: list[str] = []
    for alias in aliases:
        if alias and alias not in seen:
            seen.add(alias)
            unique.append(alias)
    return unique


def render_template(name: str, prompt: str) -> str:
    aliases = default_aliases(name)
    created_at = datetime.now(timezone.utc).isoformat()
    alias_lines = "\n".join(f"  - {alias}" for alias in aliases)
    return f"""---
template_name: {name}
aliases:
{alias_lines}
status: active
created_at: {created_at}
format: masterzhuyan-prep-template-v1
---

# 命名备课模板：{name}

## 核心意图

这份文件保存用户提供的讲课前备课 prompt。使用时先从原始 prompt 中提炼最有用的注意力方向，再进入 MasterZhuyan 的默认 longform 输出流程。

## 激活方式

仅当用户在当前请求中明确提到本模板，例如“{name}式讲解”“{name}模板”“用{name}风格”“按{name}教案”时，才加载本文件作为备课模板。不要因为普通话题里出现“{name}”这个裸词而自动激活。

## 备课注意力

1. 抓住用户想强化的角色定位、资料优先级、学习目标、解释风格和安全边界。
2. 把 prompt 作为软性注意力配置，不把它变成死板分支或必填表格。
3. 当前用户请求和本轮材料优先于本模板。
4. 如果 prompt 与 longform-first 冲突，默认保留 longform 容器，只调整章节内部写法。
5. 如果 prompt 涉及医学、法律、金融、工程安全等高风险内容，继续保留来源核对和不确定性标注。

## 用户原始 prompt

<<<masterzhuyan-prep-prompt
{prompt.strip()}
masterzhuyan-prep-prompt
"""


def create_template(name: str, prompt: str, out_dir: Path, force: bool = False) -> Path:
    if not name.strip():
        raise ValueError("template name is required")
    if not prompt.strip():
        raise ValueError("prompt text is required")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{safe_filename(name)}.md"
    if path.exists() and not force:
        raise FileExistsError(f"template already exists: {path}")
    path.write_text(render_template(name.strip(), prompt), encoding="utf-8")
    return path


def load_template(path: Path) -> PrepTemplate | None:
    if not path.is_file() or path.suffix.lower() != ".md":
        return None
    text = path.read_text(encoding="utf-8", errors="ignore")
    meta = parse_frontmatter(text)
    name_value = meta.get("template_name") or path.stem
    if not isinstance(name_value, str) or not name_value.strip():
        return None
    aliases_value = meta.get("aliases", [])
    aliases: list[str] = []
    if isinstance(aliases_value, list):
        aliases = [str(item).strip() for item in aliases_value if str(item).strip()]
    elif isinstance(aliases_value, str) and aliases_value.strip():
        aliases = [aliases_value.strip()]
    status_value = meta.get("status", "active")
    status = str(status_value).strip() or "active"
    return PrepTemplate(name=name_value.strip(), path=path, aliases=aliases, status=status)


def iter_template_files(directory: Path) -> Iterable[PrepTemplate]:
    if not directory.exists() or not directory.is_dir():
        return
    for path in sorted(directory.glob("*.md")):
        template = load_template(path)
        if template is not None:
            yield template


def normalize_for_match(value: str) -> str:
    return re.sub(r"\s+", "", value).lower()


def template_score(template: PrepTemplate, query: str) -> int:
    normalized_query = normalize_for_match(query)
    candidates = [*template.aliases, *default_aliases(template.name)]
    best = 0
    for candidate in candidates:
        normalized_candidate = normalize_for_match(candidate)
        if not normalized_candidate:
            continue
        if normalized_candidate in normalized_query:
            best = max(best, len(normalized_candidate))
    return best


def find_matches(query: str, local_dir: Path) -> list[PrepTemplate]:
    scored: list[tuple[int, int, PrepTemplate]] = []
    for order, template in enumerate(iter_template_files(local_dir)):
        if template.status.lower() not in {"active", "enabled"}:
            continue
        score = template_score(template, query)
        if score > 0:
            scored.append((score, -order, template))
    scored.sort(key=lambda item: (item[0], item[1], -len(str(item[2].path))), reverse=True)
    return [item[2] for item in scored]


def template_to_dict(template: PrepTemplate) -> dict[str, object]:
    return {
        "name": template.name,
        "path": str(template.path),
        "aliases": template.aliases,
        "source": template.source,
        "status": template.status,
    }


def command_init(args: argparse.Namespace) -> int:
    prompt = args.prompt
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    path = create_template(args.name, prompt or "", Path(args.out), force=args.force)
    print(path)
    return 0


def command_list(args: argparse.Namespace) -> int:
    templates = [template_to_dict(template) for template in iter_template_files(Path(args.dir))]
    print(json.dumps(templates, ensure_ascii=False, indent=2))
    return 0


def command_match(args: argparse.Namespace) -> int:
    matches = find_matches(args.query, Path(args.dir))
    payload = [template_to_dict(template) for template in matches]
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif matches:
        print(matches[0].path)
    return 0 if matches else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create a local prep-template file")
    init.add_argument("--name", required=True)
    prompt_group = init.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file")
    init.add_argument("--out", default=".masterzhuyan/prep_templates")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=command_init)

    list_cmd = sub.add_parser("list", help="list local templates")
    list_cmd.add_argument("--dir", default=".masterzhuyan/prep_templates")
    list_cmd.set_defaults(func=command_list)

    match = sub.add_parser("match", help="find explicitly activated templates in a user query")
    match.add_argument("--query", required=True)
    match.add_argument("--dir", default=".masterzhuyan/prep_templates")
    match.add_argument("--json", action="store_true")
    match.set_defaults(func=command_match)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # noqa: BLE001
        print(f"prep_template error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
