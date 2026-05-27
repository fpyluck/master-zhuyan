from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_mz_longform_init_validate_merge(tmp_path: Path) -> None:
    script = Path(__file__).resolve().parents[1] / "scripts" / "mz_longform.py"
    root = tmp_path / "long_output" / "demo"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "init",
            "--root",
            str(root),
            "--title",
            "演示项目",
            "--mode",
            "understanding",
            "--chapters",
            "总论|机制|应用",
        ],
        check=True,
    )
    assert (root / "manifest.yaml").exists()
    assert (root / "index.md").exists()
    chapter_files = sorted((root / "chapters").glob("*.md"))
    assert len(chapter_files) == 3
    chapter_text = chapter_files[0].read_text(encoding="utf-8")
    assert "# 总论" in chapter_text
    assert "chapter objective: 本章用于承载 MasterZhuyan 的系统学习内容。" in chapter_text
    assert "本章正文结构由 MasterZhuyan chapter_plan 决定" in chapter_text
    assert "## 核心内容" not in chapter_text
    assert "## 例子、对比或应用" not in chapter_text
    assert "## 易错点与边界" not in chapter_text
    assert "## 本章小结" not in chapter_text

    validate = subprocess.run(
        [sys.executable, str(script), "validate", "--root", str(root)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "validation passed" in validate.stdout
    assert "chapter still contains scaffold text" in validate.stdout

    subprocess.run([sys.executable, str(script), "merge", "--root", str(root)], check=True)
    final_file = root / "final" / "final_merged.md"
    assert final_file.exists()
    text = final_file.read_text(encoding="utf-8")
    assert "# 演示项目" in text
    assert "总论" in text
