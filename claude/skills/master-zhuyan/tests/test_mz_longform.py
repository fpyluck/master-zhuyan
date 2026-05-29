from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.mz_longform import load_manifest


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
            "--chapter-emphasis",
            "understanding",
            "--chapters",
            "总论|机制|应用",
        ],
        check=True,
    )
    assert (root / "manifest.yaml").exists()
    assert (root / "index.md").exists()
    assert (root / "notes" / "process_trace.md").exists()
    manifest_text = (root / "manifest.yaml").read_text(encoding="utf-8")
    assert "chapter_emphasis: understanding" in manifest_text
    assert "chapter_emphasis:" in manifest_text
    chapter_files = sorted((root / "chapters").glob("*.md"))
    assert len(chapter_files) == 3
    chapter_text = chapter_files[0].read_text(encoding="utf-8")
    assert "# 总论" in chapter_text
    assert "purpose: 待由 notes/chapter_plan.md 的 purpose / required_anchors / completion_criteria 写入。" in chapter_text
    assert "本章正文待根据 locked Knowledge Model 和 required_anchors 写入。" in chapter_text
    assert "## 核心内容" not in chapter_text
    assert "## 例子、对比或应用" not in chapter_text
    assert "## 易错点与边界" not in chapter_text
    assert "## 本章小结" not in chapter_text

    (root / "notes" / "chapter_plan.md").write_text(
        "\n".join(
            [
                "# Chapter Plan",
                "",
                "chapter_id: 01_overview",
                "title: 总论",
                "purpose: explain the topic overview",
                "input_refs: notes/knowledge_model.md, notes/evidence_ledger.md",
                "required_anchors: EL-demo, core model",
                "output_path: chapters/01-总论.md",
                "completion_criteria: learner can explain the overview",
                "",
                "chapter_id: 02_mechanism",
                "title: 机制",
                "purpose: explain the mechanism",
                "input_refs: notes/knowledge_model.md, notes/evidence_ledger.md",
                "required_anchors: EL-demo, mechanism chain",
                "output_path: chapters/02-机制.md",
                "completion_criteria: learner can explain the mechanism",
                "",
            ]
        ),
        encoding="utf-8",
    )
    materialize = subprocess.run(
        [sys.executable, str(script), "materialize-chapter-agents", "--root", str(root)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "materialized: notes/agent_outputs/teaching_composer/01_overview/" in materialize.stdout
    assert "materialized: notes/agent_outputs/teaching_composer/02_mechanism/" in materialize.stdout
    package = root / "notes" / "agent_outputs" / "teaching_composer" / "01_overview" / "teaching_composer_01_overview.md"
    assert package.exists()
    package_text = package.read_text(encoding="utf-8")
    assert "agent_type: teaching_composer" in package_text
    assert "purpose: explain the topic overview" in package_text
    assert "evidence_ids_used: pending" in package_text
    assert "required_anchors_covered: pending" in package_text
    assert "required_anchors_omitted: none" in package_text
    assert "integrator_action: pending_integrator_review" in package_text
    assert "input_artifacts: notes/knowledge_model.md, notes/evidence_ledger.md, notes/chapter_plan.md" in package_text
    assert "artifacts_read: notes/knowledge_model.md, notes/evidence_ledger.md, notes/chapter_plan.md" in package_text
    assert "canonical_targets: chapters/01-总论.md" in package_text
    trace_text = (root / "notes" / "process_trace.md").read_text(encoding="utf-8")
    assert "default_flow: chapter_plan_row -> teaching_composer_sidecar -> integrator_promotion" in trace_text
    assert "manifest_projection: 2 chapter_plan rows -> manifest.yaml + index.md" in trace_text

    many_rows = ["# Chapter Plan", ""]
    for index in range(1, 13):
        many_rows.extend(
            [
                f"chapter_id: ch{index:02d}",
                f"title: Chapter {index}",
                f"purpose: teach chapter {index}",
                "input_refs: notes/knowledge_model.md, notes/evidence_ledger.md",
                f"required_anchors: EL-demo, anchor {index}",
                f"output_path: chapters/{index:02d}-chapter-{index}.md",
                f"completion_criteria: learner can explain chapter {index}",
                "",
            ]
        )
    (root / "notes" / "chapter_plan.md").write_text("\n".join(many_rows), encoding="utf-8")
    many_materialize = subprocess.run(
        [sys.executable, str(script), "materialize-chapter-agents", "--root", str(root), "--overwrite"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert many_materialize.stdout.count("materialized: notes/agent_outputs/teaching_composer/") == 12
    assert many_materialize.stdout.count("chapter shell ready: chapters/") == 12
    assert (
        root
        / "notes"
        / "agent_outputs"
        / "teaching_composer"
        / "ch12"
        / "teaching_composer_ch12.md"
    ).exists()
    synced_manifest = load_manifest(root)
    assert [chapter["id"] for chapter in synced_manifest["chapters"]] == [f"ch{index:02d}" for index in range(1, 13)]
    assert [chapter["file"] for chapter in synced_manifest["chapters"]] == [
        f"chapters/{index:02d}-chapter-{index}.md" for index in range(1, 13)
    ]
    index_text = (root / "index.md").read_text(encoding="utf-8")
    assert "[Chapter 12](chapters/12-chapter-12.md)" in index_text
    assert "## 交付说明" in index_text
    assert len(list((root / "chapters").glob("*.md"))) == 15
    for index in range(1, 13):
        assert (root / "chapters" / f"{index:02d}-chapter-{index}.md").exists()

    validate = subprocess.run(
        [sys.executable, str(script), "validate", "--root", str(root)],
        text=True,
        capture_output=True,
    )
    assert validate.returncode == 1
    assert "validation failed" in validate.stdout
    assert "chapter still contains scaffold text" in validate.stdout

    for chapter in synced_manifest["chapters"]:
        chapter_file = root / chapter["file"]
        title = chapter_file.read_text(encoding="utf-8").splitlines()[0]
        chapter_file.write_text(
            "\n".join(
                [
                    title,
                    "",
                    "This chapter contains evidence-bound learning content.",
                    "",
                    "Evidence reference: EL-demo.",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    validate = subprocess.run(
        [sys.executable, str(script), "validate", "--root", str(root)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "validation passed" in validate.stdout
    assert "semantic DeepResearch checks require:" in validate.stdout

    subprocess.run([sys.executable, str(script), "merge", "--root", str(root)], check=True)
    final_file = root / "final" / "final_merged.md"
    assert final_file.exists()
    text = final_file.read_text(encoding="utf-8")
    assert "# 演示项目" in text
    assert "Chapter 12" in text
    assert "总论" not in text


def test_mz_longform_materialize_preserves_index_delivery_notes(tmp_path: Path) -> None:
    script = Path(__file__).resolve().parents[1] / "scripts" / "mz_longform.py"
    root = tmp_path / "long_output" / "notes"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "init",
            "--root",
            str(root),
            "--title",
            "说明保留项目",
            "--chapters",
            "起点",
        ],
        check=True,
    )
    index_path = root / "index.md"
    index_path.write_text(index_path.read_text(encoding="utf-8") + "\n## 交付说明\n\nkeep me\n", encoding="utf-8")
    (root / "notes" / "chapter_plan.md").write_text(
        "\n".join(
            [
                "# Chapter Plan",
                "",
                "chapter_id: ch01",
                "title: 起点",
                "purpose: keep the chapter current",
                "input_refs: notes/knowledge_model.md, notes/evidence_ledger.md",
                "required_anchors: EL-demo",
                "output_path: chapters/01-start.md",
                "completion_criteria: learner can explain the chapter",
                "",
            ]
        ),
        encoding="utf-8",
    )

    subprocess.run([sys.executable, str(script), "materialize-chapter-agents", "--root", str(root)], check=True)

    updated_index = index_path.read_text(encoding="utf-8")
    assert "keep me" in updated_index
    assert "[起点](chapters/01-start.md)" in updated_index


def test_mz_longform_materialize_refuses_to_drop_non_planned_chapter(tmp_path: Path) -> None:
    script = Path(__file__).resolve().parents[1] / "scripts" / "mz_longform.py"
    root = tmp_path / "long_output" / "drop"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "init",
            "--root",
            str(root),
            "--title",
            "保留章节项目",
            "--chapters",
            "旧章",
        ],
        check=True,
    )
    (root / "manifest.yaml").write_text(
        "title: 保留章节项目\n"
        "chapter_emphasis: understanding\n"
        "status: drafting\n"
        "chapters:\n"
        "  - id: old\n"
        "    title: Old chapter\n"
        "    file: chapters/old.md\n"
        "    status: reviewed\n",
        encoding="utf-8",
    )
    (root / "notes" / "chapter_plan.md").write_text(
        "\n".join(
            [
                "# Chapter Plan",
                "",
                "chapter_id: ch01",
                "title: 新章",
                "purpose: explain the new plan",
                "input_refs: notes/knowledge_model.md, notes/evidence_ledger.md",
                "required_anchors: EL-demo",
                "output_path: chapters/01-new.md",
                "completion_criteria: learner can explain the new plan",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(script), "materialize-chapter-agents", "--root", str(root)],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "cannot drop non-planned manifest chapter entries" in result.stdout


def test_mz_longform_validate_and_merge_reject_manifest_drift(tmp_path: Path) -> None:
    script = Path(__file__).resolve().parents[1] / "scripts" / "mz_longform.py"
    root = tmp_path / "long_output" / "drift"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "init",
            "--root",
            str(root),
            "--title",
            "漂移项目",
            "--chapters",
            "旧章",
        ],
        check=True,
    )
    (root / "notes" / "chapter_plan.md").write_text(
        "\n".join(
            [
                "# Chapter Plan",
                "",
                "chapter_id: ch01",
                "title: 新章",
                "purpose: teach the current planned chapter",
                "input_refs: notes/knowledge_model.md, notes/evidence_ledger.md",
                "required_anchors: EL-demo",
                "output_path: chapters/01-new.md",
                "completion_criteria: learner can explain the current plan",
                "",
            ]
        ),
        encoding="utf-8",
    )

    validate = subprocess.run(
        [sys.executable, str(script), "validate", "--root", str(root)],
        text=True,
        capture_output=True,
    )
    assert validate.returncode == 1
    assert "manifest chapters do not match notes/chapter_plan.md" in validate.stdout

    merge = subprocess.run(
        [sys.executable, str(script), "merge", "--root", str(root)],
        text=True,
        capture_output=True,
    )
    assert merge.returncode == 1
    assert "merge failed: manifest chapters do not match notes/chapter_plan.md" in merge.stdout
