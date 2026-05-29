## MasterZhuyan Agent Fabric

Use this reference for MasterZhuyan AgenticResearch runs: active acquisition, broad source coverage, model building, multi-perspective teaching composition, trace curation, continuation mapping, and recorded fallback passes.

The Agent Fabric turns MasterZhuyan from a monolithic prompt into an artifact-producing research system. Each agent receives one mission and writes one bounded artifact. The integrator reads artifacts, updates canonical notes, and composes the longform deliverable. DeepResearch runs use it as the dispatch contract; optionality applies to extra non-chapter passes, not to the default per-chapter Teaching Composer path after `chapter_plan` is stable.

### 0. DeepResearch Agent Planning

Promotion into canonical notes is the boundary. Exploratory sidecars may be broad and creative; accepted evidence, knowledge-model entries, and final chapters must have source state, inference labels, or explicit unavailable markers.

Plan agents like a concrete DeepResearch system: independent acquisition, evidence, modeling, critique, and synthesis are normal execution units when each has a bounded artifact, source grounding, useful dissent or teaching value, and an integrator promotion path. If the native sub-agent runtime is unavailable or a worker fails, record that concrete failure and create a fallback artifact for the same target; the fallback follows the same artifact -> integrator decision -> canonical target path.

### 1. Workbench Layout

Create this layout under the longform root:

```text
notes/
  process_trace.md
  research_tree.md
  source_map.md
  evidence_ledger.md
  knowledge_model.md
  chapter_plan.md
  integrator_decisions.md
  citation_audit.md
  continuation_map.md
  agent_outputs/
    source_scout/
    evidence_curator/
    mechanism_modeler/
    concept_graph_builder/
    misconception_repairer/
    comparison_builder/
    teaching_composer/
    trace_curator/
```

Create agent output subdirectories as needed for actual outputs or fallback records.

### 2. Agent Dispatch Card

Use this card for every agent pass:

```text
agent_id:
agent_type:
mission:
input_artifacts:
allowed_sources:
active_acquisition:
output_artifact:
canonical_targets:
trace_update:
handoff_to:
completion_signal:
failure_label:
```

Field meanings:

- `agent_id`: stable run-local id, for example `source_scout_official_001`.
- `agent_type`: one of the agent contracts below.
- `mission`: one concrete artifact-producing task.
- `input_artifacts`: paths the agent should read.
- `allowed_sources`: local files, web, MCP, OCR, user materials, or all available sources.
- `active_acquisition`: source types the agent may add.
- `output_artifact`: exact path under `notes/agent_outputs/`.
- `canonical_targets`: canonical notes the integrator may update from this artifact.
- `trace_update`: required process trace entry.
- `handoff_to`: next agent type or `integrator`.
- `completion_signal`: what the artifact must contain when finished.
- `failure_label`: `none`, `not_found`, `access_blocked`, `tool_failed`, `source_partial`, `contradicted`, `insufficient_precision`, or `out_of_scope`.

Each agent pass follows the compact loop from `references/deep-research-execution.md`: decide the node, act with the assigned tool or artifact task, observe source/evidence/result/failure, update canonical targets through the integrator, then stop only when the node's stop condition is met, retired, or recorded as blocked.

### 3. Agent Contracts

#### Contract Builder

Use this as the initialization agent or integrator-owned artifact that starts the run.

```text
agent_type: contract_builder
mission: turn the user request into route, scope, knowledge questions, success criteria, and agent plan
input_artifacts: user request, supplied sources, existing project notes
active_acquisition: none by default
output_artifact: notes/research_brief.md or notes/agent_outputs/contract_builder/<agent_id>.md
canonical_targets: notes/research_brief.md, notes/process_trace.md
completion_signal: learner goal, source situation, primary confusion, success criteria, and first useful agents
```

Output format:

```markdown
## Contract Builder Output

learner_goal:
primary_confusion:
success_criteria:
source_situation:
knowledge_questions:
agent_plan:
```

#### Source Scout

```text
agent_type: source_scout
mission: discover and collect sources that can support the learning model
input_artifacts: notes/research_brief.md, supplied files, existing notes/source_map.md
active_acquisition: web, local files, uploaded files, MCP, OCR, user-provided archives
output_artifact: notes/agent_outputs/source_scout/<agent_id>.md
canonical_targets: notes/source_map.md, notes/research_tree.md, notes/process_trace.md
completion_signal: source entries grouped by topic, source value, locator, and supported knowledge question
```

Output format:

```markdown
## Source Scout Output: <agent_id>

### Sources Added

source_id:
title:
source_type:
locator:
access_method:
retrieved_at:
read_state:
supports_questions:
usable_topics:
must_preserve:
evidence_card_ids:
limitations:
failure_label:

### Source Clusters

cluster:
sources:
teaching_value:

### Acquisition Notes

- query_or_method:
  result:
  next_source_hint:
```

#### Evidence Curator

```text
agent_type: evidence_curator
mission: convert sources into claim-level evidence entries
input_artifacts: notes/source_map.md, assigned sources
active_acquisition: source follow-ups needed to verify a claim
output_artifact: notes/agent_outputs/evidence_curator/<agent_id>.md
canonical_targets: notes/evidence_ledger.md, notes/citation_audit.md
completion_signal: accepted, contradicted, inferred, and missing evidence entries ready for integrator merge
```

Output format:

```markdown
## Evidence Curator Output: <agent_id>

claim_id: EL-<NNN>
claim:
source_ref:
locator:
evidence_type:
confidence:
status:
teaching_use:
contradiction_note:
```

Populate candidate entries with `references/deep-research-output-contracts.md` section 4 `Extraction flow`: claim, support state, reference frame when needed, and unavailable precision/frame gaps for integrator action.

#### Mechanism Modeler

```text
agent_type: mechanism_modeler
mission: build causal, procedural, structural, or decision mechanisms from accepted evidence
input_artifacts: notes/evidence_ledger.md
active_acquisition: mechanism sources when evidence lacks intermediate links
output_artifact: notes/agent_outputs/mechanism_modeler/<agent_id>.md
canonical_targets: notes/knowledge_model.md
completion_signal: mechanism chains with conditions, process, result, boundary, and evidence ids
```

Output format:

```markdown
## Mechanism Modeler Output: <agent_id>

mechanism:
starting_condition:
trigger_or_constraint:
intermediate_steps:
result:
failure_or_boundary:
evidence_ids:
teaching_anchor:
```

#### Concept Graph Builder

```text
agent_type: concept_graph_builder
mission: turn evidence and mechanisms into a concept graph and prerequisite map
input_artifacts: notes/evidence_ledger.md, notes/agent_outputs/mechanism_modeler/*.md
active_acquisition: prerequisite definitions and adjacent concepts
output_artifact: notes/agent_outputs/concept_graph_builder/<agent_id>.md
canonical_targets: notes/knowledge_model.md
completion_signal: concepts, relations, prerequisites, and transfer boundaries
```

Output format:

```markdown
## Concept Graph Output: <agent_id>

### Concepts

concept:
definition:
role:
evidence_ids:

### Relations

from:
to:
relation:
why_it_matters:
evidence_ids:

### Prerequisites

concept:
requires:
teach_before:
```

#### Misconception Repairer

```text
agent_type: misconception_repairer
mission: identify likely wrong patterns and write repair anchors
input_artifacts: notes/evidence_ledger.md, notes/knowledge_model.md
active_acquisition: examples, counterexamples, and exam/application traps
output_artifact: notes/agent_outputs/misconception_repairer/<agent_id>.md
canonical_targets: notes/knowledge_model.md, notes/chapter_plan.md
completion_signal: wrong belief, why it fails, repair anchor, trigger clue, and teaching placement
```

Output format:

```markdown
## Misconception Repair Output: <agent_id>

misconception:
surface_appeal:
why_wrong:
repair_anchor:
trigger_clue:
chapter_target:
evidence_ids:
```

#### Comparison Builder

```text
agent_type: comparison_builder
mission: build decisive contrasts, classification criteria, and comparison tables
input_artifacts: notes/evidence_ledger.md, notes/knowledge_model.md
active_acquisition: missing comparator definitions or examples
output_artifact: notes/agent_outputs/comparison_builder/<agent_id>.md
canonical_targets: notes/knowledge_model.md, chapters/comparison-related files
completion_signal: contrast criteria, examples, boundary cases, and table-ready rows
```

Output format:

```markdown
## Comparison Output: <agent_id>

comparison_set:
same_surface:
decisive_difference:
observable_clue:
wrong_if_confused:
examples:
evidence_ids:
```

#### Teaching Composer

```text
agent_type: teaching_composer
mission: compose one assigned evidence-bound knowledge chapter sidecar from the locked Knowledge Model and its lesson-plan row
input_artifacts: notes/knowledge_model.md, notes/chapter_plan.md, notes/evidence_ledger.md
active_acquisition: none; missing examples or source needs flow to integrator continuation or a source/lens follow-up artifact
output_artifact: notes/agent_outputs/teaching_composer/<section_id>/<agent_id>.md
canonical_targets: chapters/<chapter>.md
completion_signal: chapter-ready prose that satisfies the lesson-plan purpose, required anchors, completion criteria, evidence references, memory anchors, examples, and continuation hooks; any promoted claim names at least one accepted Evidence Ledger id or is marked as synthesis, inference, omission, or continuation
```

Output format:

```markdown
## Teaching Composer Draft: <section_id>

### Purpose

### Draft

### Evidence Used

evidence_ids_used:
required_anchors_covered:
required_anchors_omitted:
integrator_action:

### Memory Anchors

### Examples / Boundary Cases

### Continuation Hints
```

Dispatch one Teaching Composer per knowledge chapter row after `notes/chapter_plan.md` is stable. Use `chapter_id` as `section_id` for ordinary chapter drafts. The chapter row is the worker boundary; the integrator promotes only supported sidecar material into `chapters/*.md` and records accepted, revised, or discarded drafts in `notes/integrator_decisions.md`. Required anchors that do not enter the chapter are named in `required_anchors_omitted` with the integrator action that handles them.

#### Trace Curator

```text
agent_type: trace_curator
mission: turn process events and agent outputs into user-readable ProcessTracing assets
input_artifacts: notes/process_trace.md, notes/agent_outputs/**/*.md, notes/integrator_decisions.md
active_acquisition: none
output_artifact: notes/agent_outputs/trace_curator/<agent_id>.md
canonical_targets: notes/process_trace.md, notes/citation_audit.md, notes/continuation_map.md, index.md
completion_signal: phase summary, source map summary, agent contribution summary, continuation map entries
```

Output format:

```markdown
## Trace Curator Output: <agent_id>

### Phase Timeline

### Agent Contribution Map

### Strong Evidence Zones

### Citation Support State

### Expandable Branches

### User Navigation Notes
```

#### Integrator

```text
agent_type: integrator
mission: merge canonical artifacts and produce the final longform asset
input_artifacts: all canonical notes and agent outputs
active_acquisition: targeted follow-up when canonical artifacts contain unresolved load-bearing gaps
output_artifact: notes/integrator_decisions.md, notes/citation_audit.md, canonical chapters, final/final_merged.md
canonical_targets: all final artifacts
completion_signal: final merged document plus process trace and continuation map
```

Output format:

```markdown
## Integrator Decisions

### Promotions

source_artifact:
promoted_to:
changes_made:

### Revisions

artifact:
revision:
reason:

### Canonical State

source_map:
evidence_ledger:
knowledge_model:
chapter_plan:
chapters:
final:
citation_audit:
```

### 4. Dispatch Patterns

These are examples, not fixed recipes. Prefer the smallest artifact-producing plan that preserves evidence, modeling, critique, speed, and teaching quality.

#### Targeted gap or recorded fallback run

```text
contract_builder or integrator initialization
-> targeted source_scout/evidence_curator/modeler/check agent
-> fallback artifact only if native agent/tool/worker fails
-> integrator promotion/rejection
-> citation audit
-> final chapter/file asset
```

Use this for one missing mechanism, source, comparison, critique, or for a concrete runtime/tool/worker failure. It is still AgenticResearch; the fallback record explains what failed and which fallback/proposed artifact under `notes/agent_outputs/` replaced the failed agent output for the same target.

#### DeepResearch source-heavy run

```text
contract_builder
-> source_scout x N
-> evidence_curator x N
-> mechanism_modeler
-> concept_graph_builder
-> teaching_composer x chapters
-> trace_curator
-> integrator
```

#### DeepResearch concept-heavy run

```text
contract_builder
-> source_scout for definitions and mechanisms
-> mechanism_modeler
-> concept_graph_builder
-> misconception_repairer
-> comparison_builder
-> teaching_composer
-> integrator
```

#### Review-heavy run

```text
contract_builder
-> source_scout
-> evidence_curator
-> comparison_builder
-> misconception_repairer
-> trace_curator
-> integrator
```

### 5. Integrator Merge Rule

The integrator reads agent outputs, updates canonical notes, records the promotion, revision, or rejection in `notes/integrator_decisions.md`, and writes the final chapter files. Agent output files remain sidecars. Canonical merge input remains `chapters/*.md`.

Every promoted agent output must leave a traceable path:

```text
agent output -> integrator decision -> source/evidence/knowledge/chapter artifact -> final output
```

Agent output reaches DeepResearch only through an integrator decision: accepted evidence, model improvement, critique, or teaching value is promoted to canonical targets; rejected or future-use material is recorded in `notes/integrator_decisions.md` or moved to `notes/continuation_map.md`.

### 6. Validation

Use `scripts/validate_deep_research_artifacts.py --root <longform-root> --json` after the relevant artifacts exist.

Validation checks the workbench, final files, evidence/model references, integrator decisions, agent traces, and any recorded runtime/tool/worker fallback. A package with no agent outputs passes this dimension only when `process_trace.md` or `integrator_decisions.md` records a concrete fallback label such as `agent_runtime_unavailable`, `agent_worker_failed`, or `tool_failed`. This is a semantic completeness check, not an artifact-volume check.
