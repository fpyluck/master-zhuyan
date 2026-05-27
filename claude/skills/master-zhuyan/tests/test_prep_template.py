from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prep_template.py"
SPEC = importlib.util.spec_from_file_location("test_mz_prep_template", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
prep_template = importlib.util.module_from_spec(SPEC)
sys.modules["test_mz_prep_template"] = prep_template
SPEC.loader.exec_module(prep_template)


def test_init_creates_arbitrary_named_template_and_preserves_prompt(tmp_path: Path) -> None:
    out_dir = tmp_path / "templates"
    path = prep_template.create_template(
        "猫",
        "角色定位：外科学教材精读助手。默认不主动检索外部资料。",
        out_dir,
    )
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "template_name: 猫" in text
    assert "猫式讲解" in text
    assert "猫风格" in text
    assert "外科学教材精读助手" in text


def test_match_activates_only_explicit_style_phrase(tmp_path: Path) -> None:
    out_dir = tmp_path / "templates"
    prep_template.create_template("猫", "本地猫模板。", out_dir)
    payload = [prep_template.template_to_dict(item) for item in prep_template.find_matches("请用猫式讲解胆石症", out_dir)]
    assert payload[0]["name"] == "猫"
    assert payload[0]["source"] == "local"


def test_bare_ordinary_word_does_not_activate_template(tmp_path: Path) -> None:
    out_dir = tmp_path / "templates"
    prep_template.create_template("猫", "本地猫模板。", out_dir)
    assert prep_template.find_matches("请讲一下猫抓病的临床表现", out_dir) == []


def test_multiple_arbitrary_names_are_supported(tmp_path: Path) -> None:
    out_dir = tmp_path / "templates"
    prep_template.create_template("外星人", "强调反常识类比。", out_dir)
    prep_template.create_template("狗", "强调步骤化训练。", out_dir)
    payload = [prep_template.template_to_dict(item) for item in prep_template.iter_template_files(out_dir)]
    assert {item["name"] for item in payload} == {"外星人", "狗"}

    matched = prep_template.find_matches("请按外星人教案讲解这段内容", out_dir)
    assert matched[0].name == "外星人"
