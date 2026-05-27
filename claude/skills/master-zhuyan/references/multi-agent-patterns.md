# Multi-agent split patterns

Use this when multi-agent or delegated work can improve evidence coverage, planning breadth, examples, checks, or speed. This file helps the planner choose a split strategy without turning viewpoints into role theater.

## 1. Strategy rule

Multi-agent work is a normal capability when bounded artifacts reduce omission, improve evidence coverage, strengthen examples or checks, broaden planning, or speed large work without losing integrator ownership. Choose the split type by the artifact needed; `section` is common, not mandatory.

Supported split types:

1. `section`: produce a bounded chapter or section draft.
2. `source`: audit coverage across the locked source map or a bounded source cluster.
3. `lens`: inspect the same locked material from a bounded perspective to catch missing angles.
4. `check`: audit gaps, risks, precision, contradictions, or quality gates.

Planner sidecars, lens agents, critic passes, or debate-like reviews are fine when each produces a named artifact with an output path and completion criteria. Avoid splits that merely duplicate reading, spend context, blur ownership, or create more reconciliation work than learning value.

## 2. Section split

Use when chapter or section drafting can be done faster or with better coverage as bounded artifacts.

Brief fields:

section_id:
title:
allowed_sources:
required_anchors:
forbidden_scope:
output_path:
completion_criteria:

Output goes to `notes/worker-drafts/<section_id>/<agent>_draft.md` until the integrator promotes it into manifest-listed `chapters/*.md`.

## 3. Source split

Use when source coverage would improve: many files, dense notes, important exceptions, formulas, examples, or evidence that could be lost during chapter drafting. It uses a locked or sufficiently stable `notes/source_map.md`.

Brief fields:

source_id:
source_scope:
allowed_sources:
output_path:
completion_criteria:

Output goes to `notes/source-drafts/<source_id>/<agent>_coverage.md`. The artifact should map source items to chapters or findings as covered, missing, uncertain, or contradiction-flagged.

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

Output goes to `notes/lens-drafts/<lens_id>/<agent>_draft.md`. Lens drafts are sidecars only: they may suggest missing angles, examples, contrasts, or chapter-plan adjustments, but they are not canonical chapters and must not introduce unsupported source facts.

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

Output goes to `notes/checks/<check_id>/<agent>_findings.md`. The integrator resolves or rejects findings in `notes/review.md`.

## 6. Examples, not schema

Keep these as planner examples unless repeated real use proves they need their own contract:

1. example or boundary-case generation: usually a `lens` or integrator task; mark teaching examples as synthesis or inference.
2. retrieval practice, flashcards, tables, or summary sheets: produce after merge as `output/*.md` unless the user asked for them as chapters.
3. audience or style variants: use prep templates or separate final products, not multi-agent roles.

## 7. Integration rule

The integrator owns synthesis. It may use section drafts, source coverage, lens drafts, and check findings to revise `chapters/*.md`, `index.md`, and `final/final_merged.md`, but final source wording, contradiction handling, chapter scope, teaching spine, and quality judgment remain centralized.
