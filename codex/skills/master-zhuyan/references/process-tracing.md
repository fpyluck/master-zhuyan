## MasterZhuyan ProcessTracing

Use this reference for MasterZhuyan DeepResearch runs. ProcessTracing turns research work into visible, reusable learning assets. It records what agents did, what artifacts changed, what evidence is strong, where contradictions live, and what branches can continue. Keep traces compact when the research graph is small, but do not replace durable DeepResearch with conversational teaching.

### 1. Trace Files

Create or update these files under the longform root when they make decision, evidence, agent work, or continuation state reusable:

```text
notes/process_trace.md
notes/integrator_decisions.md
notes/continuation_map.md
```

Use these files with:

```text
notes/source_map.md
notes/research_tree.md
notes/evidence_ledger.md
notes/knowledge_model.md
notes/chapter_plan.md
notes/citation_audit.md
notes/agent_outputs/
```

### 2. process_trace.md Template

```markdown
## Process Trace

### Run Header

topic:
user_goal:
route: deep-research
agent_fabric_state: active | runtime_unavailable_fallback | worker_failed_fallback
longform_root:
started_at:
current_state:

### Phase Timeline

#### phase: contract_built

timestamp:
input_materials:
assumed_scope:
target_asset:
agent_plan:
fallback_record:

#### phase: source_acquisition

timestamp:
agents:
sources_added:
source_clusters:
gaps_found:
next_artifacts:

#### phase: evidence_curation

timestamp:
agents:
evidence_entries_added:
contradictions_added:
inferred_items:
missing_items:
next_artifacts:

#### phase: knowledge_modeling

timestamp:
agents:
mechanisms_built:
concept_graphs_built:
misconceptions_added:
comparisons_added:
memory_anchors_added:
next_artifacts:

#### phase: chapter_composition

timestamp:
agents:
chapter_drafts:
evidence_used:
teaching_assets_added:
next_artifacts:

#### phase: integration

timestamp:
promoted_artifacts:
revised_artifacts:
canonical_chapters:
final_output:
continuation_map:

### Agent Run Index

| agent_id | agent_type | section_id | mission | output_artifact | canonical_target | status |
|---|---|---|---|---|---|---|

### Strong Evidence Zones

| topic | evidence_ids | sources | chapter_targets |
|---|---|---|---|

### Expansion Signals

| branch | reason_to_expand | suggested_agent | suggested_artifact |
|---|---|---|---|
```

For ordinary chapter drafting, each stable `chapter_plan` row creates one `teaching_composer` index row. Its `section_id` is the row's `chapter_id`, `output_artifact` is `notes/agent_outputs/teaching_composer/<section_id>/<agent_id>.md`, and `canonical_target` is the row's `output_path`.

When native sub-agent/tool/worker execution is unavailable or fails, the Agent Run Index records the planned or failed agent/output, a concrete failure label such as `agent_runtime_unavailable`, `agent_worker_failed`, or `tool_failed`, the fallback artifact, and the DeepResearch target it serves.

### 3. integrator_decisions.md Template

```markdown
## Integrator Decisions

### Canonical Artifacts

source_map:
research_tree:
evidence_ledger:
knowledge_model:
chapter_plan:
citation_audit:
chapters:
final:

### Promotions

#### promotion: <id>

source_artifact:
promoted_to:
source_section_id:
content_used:
edits_made:
reason:

### Revisions

#### revision: <id>

artifact:
change:
reason:
target_file:

### Merges

#### merge: <id>

inputs:
merged_into:
dedupe_action:
result:

### Continuation Seeds

branch:
current_artifacts:
suggested_next_agent:
suggested_next_output:
```

### 4. continuation_map.md Template

```markdown
## Continuation Map

### Ready-To-Use Branches

branch:
what_is_already_built:
where_to_read:
next_use:

### Expandable Research Branches

branch:
why_expand:
best_next_agent:
source_targets:
expected_new_artifact:

### Teaching Asset Extensions

asset:
based_on_chapters:
agent_to_dispatch:
output_path:

### User Navigation Paths

path_name:
start_here:
then_read:
use_when:

### Agent Handoff Cards

agent_type:
mission:
input_artifacts:
output_artifact:
```

### 5. Trace Entries for Agent Outputs

Promotable agent output ends with:

```markdown
### Trace Update

agent_id:
artifacts_read:
artifacts_written:
canonical_targets:
strong_findings:
open_branches:
handoff_suggestion:
```

Without the trace update, the integrator treats the output as exploratory material; canonical use waits for the trace update and promotion decision in `notes/integrator_decisions.md`.

### 6. Index Integration

Add a ProcessTracing section to `index.md`:

```markdown
### ProcessTracing

- [Process Trace](notes/process_trace.md)
- [Source Map](notes/source_map.md)
- [Research Tree](notes/research_tree.md)
- [Evidence Ledger](notes/evidence_ledger.md)
- [Knowledge Model](notes/knowledge_model.md)
- [Citation Audit](notes/citation_audit.md)
- [Integrator Decisions](notes/integrator_decisions.md)
- [Continuation Map](notes/continuation_map.md)
```

### 7. Final Delivery Note

The final delivery response includes:

```text
Created:
- final/final_merged.md
- index.md
- notes/process_trace.md
- notes/continuation_map.md

Reading order:
1. index.md
2. final/final_merged.md
3. notes/continuation_map.md
4. notes/process_trace.md
```
