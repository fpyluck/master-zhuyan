# Multi-agent split patterns

Use this for bounded multi-agent or delegated work in MasterZhuyan AgenticResearch. This file helps the planner choose split strategies that convert scope, source coverage, critique, or synthesis into bounded artifacts with integrator review paths.

## 1. Strategy rule

Multi-agent work is a normal capability. Choose the split type by the artifact needed: reduce omission, cover sources, strengthen examples or checks, broaden planning, draft sections, or speed large work without losing integrator ownership. After `chapter_plan` is stable, `section` is the ordinary chapter-drafting path; non-chapter work may use `source`, `lens`, or `check`.

For DeepResearch MasterZhuyan runs, prefer `references/agent-fabric.md` as the dispatch layer. The split types in this file remain valid as artifact shapes:

```text
section -> teaching_composer
source  -> source_scout or evidence_curator
lens    -> comparison_builder, misconception_repairer, or concept_graph_builder
check   -> trace_curator or integrator review
```

Write agent outputs under `notes/agent_outputs/<agent_type>/...` and record canonical promotion in `notes/integrator_decisions.md`.

Supported split types:

1. `section`: produce a bounded chapter or section draft.
2. `source`: audit coverage across the locked source map or a bounded source cluster.
3. `lens`: inspect the same locked material from a bounded perspective to catch missing angles.
4. `check`: audit gaps, risks, precision, contradictions, or quality tracing findings.

Planner sidecars, lens agents, critic passes, or debate-like reviews are fine when each produces a named artifact with an output path and completion criteria. A split counts as agentic when its artifact has scope, output path, completion criteria, and an integrator accept/revise/reject path.

## 2. Section Split

Each `chapter_plan` row becomes one bounded Teaching Composer artifact.

Brief fields:

section_id:
title:
allowed_sources:
required_anchors:
forbidden_scope:
output_path:
completion_criteria:

For ordinary chapter drafting, set `section_id` to the chapter row's `chapter_id`.

Output goes to `notes/agent_outputs/teaching_composer/<section_id>/<agent_id>.md` until the integrator promotes it into canonical `chapters/*.md`.

## 3. Source split

Use when source coverage would improve: many files, dense notes, important exceptions, formulas, examples, or evidence that could be lost during chapter drafting. It uses a locked or sufficiently stable `notes/source_map.md`.

Brief fields:

source_id:
source_scope:
allowed_sources:
output_path:
completion_criteria:

Output goes to `notes/agent_outputs/source_scout/<agent_id>.md` or `notes/agent_outputs/evidence_curator/<agent_id>.md`. The artifact should map source items to chapters or findings as covered, missing, uncertain, or contradiction-flagged.

## 4. Lens split

Use when examples, contrasts, applications, or viewpoints would improve the teaching design. Good triggers include user requests for 多角度, 发散, 举一反三, or topics with competing frameworks, ambiguous cross-domain meanings, or important mechanism/exam/application/easy-error angles.

Brief fields:

lens_id:
lens_question:
allowed_sources:
required_anchors:
forbidden_scope:
output_path:
completion_criteria:

Output goes to the assigned Agent Fabric path, usually `notes/agent_outputs/comparison_builder/<agent_id>.md`, `notes/agent_outputs/misconception_repairer/<agent_id>.md`, or `notes/agent_outputs/concept_graph_builder/<agent_id>.md`. Lens drafts stay sidecars that propose missing angles, examples, contrasts, or chapter-plan adjustments; source claims enter canonical output only after integrator promotion through Evidence Ledger or chapter-plan revision.

## 5. Check split

Use when a bounded review can catch omission, false precision, unsupported inference, weak examples, poor contrast, or source/teaching drift.

Brief fields:

check_id:
check_scope:
allowed_sources:
output_path:
completion_criteria:

Each finding must use this structure:

```text
gap: <claim, omission, contradiction, or risk>
severity: high|med|low
source_needed: yes|no
suggested_action: <revise, verify, mark uncertainty, add example, add contrast, merge, cut>
```

Output goes to `notes/agent_outputs/trace_curator/<agent_id>.md` or an integrator review artifact under `notes/integrator_decisions.md`. The integrator resolves or rejects findings in `notes/integrator_decisions.md` or `notes/continuation_map.md`.

## 6. Examples, not schema

Keep these as planner examples unless repeated real use proves they need their own contract:

1. example or boundary-case generation: usually a `lens` or integrator task; mark teaching examples as synthesis or inference.
2. retrieval practice, flashcards, tables, or summary sheets: produce after merge as `output/*.md` unless the user asked for them as chapters.
3. audience or style variants: use prep templates or separate final products, not multi-agent roles.

## 7. Integration rule

The integrator owns synthesis. It may use section drafts, source coverage, lens drafts, and check findings to revise `chapters/*.md`, `index.md`, and `final/final_merged.md`, but final source wording, contradiction handling, chapter scope, teaching spine, and quality judgment remain centralized. Record accepted, revised, or discarded agent outputs in `notes/integrator_decisions.md`.
