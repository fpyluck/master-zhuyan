from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"
CITATION_ACTIONS = {
    "accept",
    "revise",
    "soften_claim",
    "omit_claim",
    "mark_unavailable",
    "dispatch_agent",
    "record_continuation",
}


def iter_object_schemas(schema: dict[str, Any], path: str) -> list[tuple[str, dict[str, Any]]]:
    found: list[tuple[str, dict[str, Any]]] = []
    if schema.get("type") == "object":
        found.append((path, schema))
    for key in ("properties", "$defs"):
        values = schema.get(key, {})
        if isinstance(values, dict):
            for name, value in values.items():
                if isinstance(value, dict):
                    found.extend(iter_object_schemas(value, f"{path}/{key}/{name}"))
    items = schema.get("items")
    if isinstance(items, dict):
        found.extend(iter_object_schemas(items, f"{path}/items"))
    return found


def test_schema_required_fields_are_defined() -> None:
    failures: list[str] = []
    for schema_path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        for path, object_schema in iter_object_schemas(schema, schema_path.name):
            required = object_schema.get("required", [])
            properties = object_schema.get("properties", {})
            if not isinstance(required, list) or not isinstance(properties, dict):
                continue
            missing = [field for field in required if field not in properties]
            if missing:
                failures.append(f"{path}: {', '.join(missing)}")
    assert failures == []


def test_source_map_schema_keeps_question_support_flow() -> None:
    schema = json.loads((SCHEMA_DIR / "source_map.schema.json").read_text(encoding="utf-8"))
    source = schema["$defs"]["source"]
    supports = source["properties"]["supports_questions"]

    assert "supports_questions" in source["required"]
    assert supports["type"] == "array"
    assert supports["items"]["type"] == "string"


def test_research_brief_schema_carries_final_quality_contract() -> None:
    schema = json.loads((SCHEMA_DIR / "research_brief.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    properties = schema["properties"]

    assert {"primary_confusion", "success_criteria"} <= required
    assert properties["success_criteria"]["type"] == "array"


def test_source_map_keeps_source_to_card_index_separate_from_model_evidence_ids() -> None:
    schema = json.loads((SCHEMA_DIR / "source_map.schema.json").read_text(encoding="utf-8"))
    source_properties = schema["$defs"]["source"]["properties"]
    contracts = (ROOT / "references" / "deep-research-output-contracts.md").read_text(encoding="utf-8")
    source_map_section = contracts.split("## 4. Evidence Ledger", 1)[0].split("## 3. Source Map", 1)[1]

    assert "evidence_card_ids" in source_properties
    assert "evidence_ids" not in source_properties
    assert "evidence_card_ids:" in source_map_section
    assert "evidence_ids:" not in source_map_section


def test_source_map_architecture_names_card_index_not_model_evidence_field() -> None:
    architecture = (ROOT / "references" / "deep-research-architecture.md").read_text(encoding="utf-8")
    object_block = architecture.split("research_brief", 1)[0].split("source_map", 1)[1]

    assert "records evidence_card_ids[]" in object_block
    assert "records evidence_ids[]" not in object_block


def test_evidence_card_schema_matches_ledger_value_contract() -> None:
    schema = json.loads((SCHEMA_DIR / "evidence_card.schema.json").read_text(encoding="utf-8"))
    properties = schema["properties"]

    assert "claim_id" in schema["required"]
    assert "claim_id" in properties
    assert "card_id" not in schema["required"]
    assert "card_id" not in properties

    confidence = set(properties["confidence"]["enum"])
    evidence_type = set(properties["evidence_type"]["enum"])

    assert {"high", "medium", "med", "low", "inferred", "unknown"} <= confidence
    assert {"step", "risk", "contrast"} <= evidence_type


def test_citation_audit_schema_matches_output_action_contract() -> None:
    schema = json.loads((SCHEMA_DIR / "citation_audit.schema.json").read_text(encoding="utf-8"))
    item = schema["$defs"]["item"]
    properties = item["properties"]

    assert {"evidence_ids", "source_ids", "locator_check"} <= set(item["required"])

    actions = set(properties["integrator_action"]["enum"])
    assert actions == CITATION_ACTIONS
    assert "weaken" not in actions
    assert "omit" not in actions


def test_quality_trace_action_boundary_extends_citation_actions_only_for_artifact_repair() -> None:
    schema = json.loads((SCHEMA_DIR / "quality_report.schema.json").read_text(encoding="utf-8"))

    actions = schema["$defs"]["action_enum"]["enum"]
    assert len(actions) == len(set(actions))
    assert set(actions) == CITATION_ACTIONS | {"create_missing_artifact"}
    assert "not_applicable" not in actions


def test_quality_gate_docs_name_quality_only_action_boundary() -> None:
    quality_gates = (ROOT / "references" / "quality-gates.md").read_text(encoding="utf-8")
    output_contracts = (ROOT / "references" / "deep-research-output-contracts.md").read_text(encoding="utf-8")

    assert "create_missing_artifact" in quality_gates
    assert "only for quality-trace container or required-file repair" in quality_gates
    assert (
        "integrator_action: accept | revise | create_missing_artifact | dispatch_agent | "
        "soften_claim | omit_claim | mark_unavailable | record_continuation"
    ) in quality_gates
    assert "verify, soften, omit, scope out, dispatch evidence work" not in output_contracts


def test_knowledge_model_schema_uses_evidence_ids_not_card_aliases() -> None:
    schema = json.loads((SCHEMA_DIR / "knowledge_model.schema.json").read_text(encoding="utf-8"))
    defs = schema["$defs"]

    for def_name in ("concept", "relation", "mechanism", "comparison", "anchor", "easy_error"):
        properties = defs[def_name]["properties"]
        assert "evidence_ids" in properties
        assert "evidence_card_ids" not in properties

    assert "core_spine_evidence_ids" in schema["required"]
    assert "core_spine_evidence_ids" in schema["properties"]
