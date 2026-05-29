# Deep-research artifact contracts

These contracts define internal working-note formats used by `references/deep-research-execution.md`. They are not user-facing teaching output; they keep research, evidence, modeling, tracing, and integration artifacts mergeable.

## 1. Research Brief

File path: `notes/research_brief.md`

Fields:

```text
topic_title:
user_goal:
primary_confusion:
success_criteria:
learner_bottleneck:
source_map_ref:
scope:
research_questions:
  - id:
    question:
    why_it_matters:
    expected_agent:
source_strategy:
  - source_type:
    use_for:
    acquisition_agent:
agent_fabric_plan:
  - agent_id:
    agent_type:
    mission:
    output_artifact:
selected_spine:
chapter_emphasis:
must_preserve_details:
precision_anchors:
initial_continuation_branches:
  - branch:
    why_it_may_expand:
revision_reasons:
```

The brief records the learner's goal, primary confusion, success criteria, reasonable scope, and research questions so execution can start. `schemas/research_brief.schema.json` is the canonical field vocabulary; older labels such as `topic`, `learner_goal`, or `knowledge_questions` may be read as compatibility aliases, but new artifacts use the schema names. Broad scope alone flows to panoramic structure. Only scope problems that are also high-risk or break the user's stated goal become `revision_reasons`; remaining gaps are continuation targets.

## 2. Research Tree

File path: `notes/research_tree.md`

Fields:

```text
node_id:
question:
why_it_matters:
source_need:
owner:
status: open|searching|reading|evidence_ready|modeled|retired|blocked
evidence_ids:
next_action:
stop_condition:
```

The research tree is dynamic: nodes may split, merge, retire, or become blocked as evidence changes. Node count is descriptive: quality is shown by question, source_need, status, evidence_ids, next_action, stop_condition, and state transitions as evidence changes.

## 3. Source Map

File path: `notes/source_map.md`

Fields:

```text
source_id:
title:
source_type:
locator:
access_method:
retrieved_at:
read_state:
supports_questions:
limitations:
failure_label:
usable_topics:
must_preserve:
gaps:
evidence_card_ids:
```

Use `access_method` to distinguish supplied material, local reads, retrieval, OCR, browser, MCP, or failed attempts. Put the retraceable path, URL, page range, or screenshot label in `locator`. `must_preserve` details flow into Evidence Ledger claims before teaching synthesis; `evidence_card_ids` is the reverse index from this source to those claim/card ids. Knowledge Model and Citation Audit consume those claims through `evidence_ids`. Limitations and gaps travel with the source into the Evidence Ledger and continuation map.

## 4. Evidence Ledger

File path: `notes/evidence_ledger.md`

One entry per claim that can affect teaching:

```text
claim_id: EL-<NNN>
claim:
source_ref:
locator:
evidence_type: definition|mechanism|classification|threshold|formula|step|example|exception|risk|contrast|case
confidence: high|med|low|inferred
status: accepted|uncertain|contradicted|missing
teaching_use:
chapter_targets:
contradiction_note:
```

Confidence levels:

- `high`: source is unambiguous on this point.
- `med`: interpretation was needed; the claim is a reasonable reading.
- `low`: source is thin, indirect, old, or context-limited.
- `inferred`: no source directly supports this; the claim is derived by reasoning from other claims and must be labeled as inference in teaching output.

Extraction flow:

1. Extract the claim and its source locator.
2. If the claim controls a precision anchor, record support state visibly in `status`, `confidence`, or `contradiction_note`.
3. If the claim describes a deviation, abnormal state, exception, threshold, risk, severity grade, comparator, or trend, carry the reference frame that makes it interpretable in the same entry or a peer entry: normal/baseline range, default rule, null model, comparator group, unit and scale, API/version contract, nominal operating state, historical starting point, ordinary-language meaning, or domain-specific reference condition.
4. If the source lacks the needed precision or reference frame, mark the gap as unavailable in the ledger and route it to `integrator_action`: `dispatch_agent`, `soften_claim`, `omit_claim`, `mark_unavailable`, or `record_continuation`. Non-core extension gaps may continue; load-bearing, high-risk, or `primary_confusion` gaps must be resolved or marked unavailable before final merge.

## 5. Knowledge Model

File path: `notes/knowledge_model.md`

### Core Spine

```text
spine:
why_this_spine:
evidence_ids:
open_questions:
```

### Concepts

```text
concept:
definition:
role: core|supporting|boundary
evidence_ids:
confidence: high|med|low|inferred
```

### Mechanisms

```text
mechanism:
starting_condition:
process:
result:
boundary:
evidence_ids:
teaching_anchor:
```

### Comparisons

```text
comparison_set:
same_surface:
decisive_difference:
observable_clue:
wrong_if_confused:
evidence_ids:
```

### Misconceptions

```text
misconception:
why_it_appears:
why_wrong:
repair_anchor:
evidence_ids:
```

Every misconception entry must have a `repair_anchor`. A flag without a repair is not actionable for teaching.

### Memory Anchors

```text
anchor:
recall_trigger:
supports:
chapter_target:
evidence_ids:
```

### Transfer Boundaries

```text
can_transfer_to:
requires:
boundary:
evidence_ids:
```

### Gaps

```text
question:
status: missing|thin|conflicted
current_artifacts:
next_agent:
continuation_target:
```

Gaps enter `integrator_action` before final merge: `dispatch_agent`, `revise`, `mark_unavailable`, `omit_claim`, `soften_claim`, or `record_continuation`. Continuation without changing the final claim is reserved for non-core extension gaps; load-bearing gaps change the final claim through acquisition, revision, softening, omission, or unavailable marking.

## 6. Lesson Plan / Chapter Plan

File path: `notes/chapter_plan.md`

The lesson plan is produced from the locked Knowledge Model. It chooses knowledge chapters from the learner bottleneck, selected core spine, reference frame, and precision anchors. Delivery metadata flows to `index.md`, `notes/*`, or the final delivery note; only substantive reference-frame or knowledge-overview content is promoted into chapter rows.

Header fields:

```text
learner_bottleneck:
selected_spine:
reference_frame:
precision_anchors:
knowledge_model_ref:
evidence_ledger_ref:
```

One row per knowledge chapter:

```text
chapter_id:
title:
purpose:
emphasis:
input_refs:
required_anchors:
output_path:
completion_criteria:
```

Each row is also the default Teaching Composer boundary: `chapter_id` becomes `section_id`, the sidecar path is `notes/agent_outputs/teaching_composer/<section_id>/<agent_id>.md`, and `output_path` stays the canonical chapter target that the integrator may promote into after review.

Rules:

1. A chapter teaches something the learner must understand, remember, judge, repair, or reuse; `chapter_id` and `title` name that knowledge. Navigation, reading order, sources, safety scope, usage instructions, high-risk boundaries, and pure prelude/metadata flow to `index.md`, `notes/*`, or the final delivery note unless the user asks to study safety logic itself.
2. `purpose` states what the learner can do after the chapter. `required_anchors` lists the load-bearing reference frame, definitions, mechanisms, classifications, thresholds, causes, contraindications, exceptions, criteria, formulas, or easy-error repairs; evidence-bearing anchors include their `EL-*`/`EV-*` ids so sidecar, citation, and final-resolution checks can trace them. `completion_criteria` must be checkable against the Knowledge Model and Evidence Ledger.
3. Reverse coverage is part of the plan: every accepted load-bearing `must_preserve` detail, precision anchor, contradiction/gap resolution, primary-confusion answer, and teaching-critical example, exception, risk, or contrast from the Evidence Ledger or Knowledge Model resolves to a chapter row, an explicit limitation/unavailable note, or a continuation target with the integrator's reason. Do not add a decorative chapter just to host it; merge it into the row whose `purpose` it changes, or record why it stays outside the final teaching body.

## 7. Agent Output

File path: `notes/agent_outputs/<agent_type>/<agent_id>.md` or, for chapter drafts, `notes/agent_outputs/teaching_composer/<section_id>/<agent_id>.md`

Common wrapper:

```text
agent_id:
agent_type:
mission:
input_artifacts:
output_targets:
```

Each agent output includes an agent-specific work product from `references/agent-fabric.md`, then ends with:

```text
canonical_promotion_hints:
  promote_to:
  sections_or_entries:
  edits_needed:
trace_update:
  artifacts_read:
  artifacts_written:
  canonical_targets:
  strong_findings:
  open_branches:
  handoff_suggestion:
```

Teaching Composer sidecars also expose the chapter coverage state before promotion:

```text
evidence_ids_used:
required_anchors_covered:
required_anchors_omitted:
integrator_action:
```

`evidence_ids_used` and `required_anchors_covered` name the evidence ids that actually support the draft, not only prose labels for the anchors. If an anchor is not covered, `required_anchors_omitted` names it with the integrator action that keeps it out of the final teaching target.

Agent outputs start as sidecars. For chapter composition, `section_id` maps back to the `chapter_plan` row's `chapter_id`; the chapter row supplies purpose, anchors, target path, and completion criteria. The integrator records promotion, revision, or discard in `notes/integrator_decisions.md`; only promoted content updates canonical notes or chapters. A required anchor may be omitted only when the sidecar or integrator records `soften_claim`, `omit_claim`, `mark_unavailable`, `dispatch_agent`, or `record_continuation` for the affected final target.

## 8. Process Trace

File path: `notes/process_trace.md`

Minimum sections:

```text
run_header:
  topic:
  user_goal:
  route: deepresearch-longform
  agent_fabric_state: active | runtime_unavailable_fallback | worker_failed_fallback
  agent_plan_reason:
  longform_root:
  current_state:
phase_timeline:
  - phase:
    timestamp:
    agents:
    artifacts_written:
    gaps_found:
    next_artifacts:
agent_run_index:
  - agent_id:
    agent_type:
    mission:
    output_artifact:
    canonical_target:
    status:
strong_evidence_zones:
  - topic:
    evidence_ids:
    sources:
    chapter_targets:
expansion_signals:
  - branch:
    reason_to_expand:
    suggested_agent:
    suggested_artifact:
```

Process trace is visibility and continuation infrastructure, not a budget or stop mechanism.

## 9. Integrator Decisions

File path: `notes/integrator_decisions.md`

Fields:

```text
canonical_artifacts:
  source_map:
  evidence_ledger:
  knowledge_model:
  chapter_plan:
  chapters:
  final:
promotions:
  - promotion_id:
    source_artifact:
    promoted_to:
    source_section_id:
    content_used:
    edits_made:
    reason:
revisions:
  - revision_id:
    artifact:
    change:
    reason:
    target_file:
merges:
  - merge_id:
    inputs:
    merged_into:
    dedupe_action:
    result:
anchor_omissions:
  - chapter_id:
    anchor:
    evidence_id:
    reason: limitation|out_of_scope|deferred_to_continuation|merged_elsewhere
    integrator_action:
discarded_outputs:
  - artifact:
    reason:
continuation_seeds:
  - branch:
    current_artifacts:
    suggested_next_agent:
    suggested_next_output:
```

The integrator owns canonical promotion: worker or agent material becomes canonical only through a promotion entry in `notes/integrator_decisions.md`.

## 10. Citation Audit

File path: `notes/citation_audit.md`

Fields:

```text
claim_or_section:
evidence_ids:
source_ids:
locator_check:
support_state: supported|partial|inferred|contradicted|missing
integrator_action: accept|revise|soften_claim|omit_claim|mark_unavailable|dispatch_agent|record_continuation
```

Citation audit records whether final claims are actually supported by the Evidence Ledger and source locators. A missing or contradicted load-bearing claim enters `integrator_action`: `revise`, `soften_claim`, `omit_claim`, `dispatch_agent`, or `mark_unavailable` before final merge.

A citation row binds evidence to a target; it does not replace teaching. When evidence is accepted for a chapter or final target, the target text carries the claim's core meaning, or the citation/integrator record names the action that keeps it out of that target.

## 11. Final Merge

File path: `final/final_merged.md`

The final merge reads promoted `chapters/*.md`, `notes/chapter_plan.md`, `notes/integrator_decisions.md`, and `notes/citation_audit.md`. It is not a blind concatenation step. It preserves each chapter row's required anchors through chapter-level citation audit rows, removes duplicate delivery metadata, normalizes terminology and voice, centralizes safety or limitation notes, and places `后续知识拓展` in one final location when useful.

For each promoted knowledge chapter, `notes/citation_audit.md` has a row whose `claim_or_section` names the chapter `output_path`, `chapter_id`, or `final/final_merged.md`. The row lists the evidence IDs that support that chapter's required anchors, or records the integrator action that softened, omitted, marked unavailable, dispatched, or continued an unresolved anchor.

## 12. Continuation Map

File path: `notes/continuation_map.md`

Fields:

```text
ready_to_use_branches:
  - branch:
    what_is_already_built:
    where_to_read:
    next_use:
expandable_research_branches:
  - branch:
    why_expand:
    best_next_agent:
    source_targets:
    expected_new_artifact:
teaching_asset_extensions:
  - asset:
    based_on_chapters:
    agent_to_dispatch:
    output_path:
user_navigation_paths:
  - path_name:
    start_here:
    then_read:
    use_when:
agent_handoff_cards:
  - agent_type:
    mission:
    input_artifacts:
    output_artifact:
```

The continuation map returns choice to the learner and gives the next agent a concrete starting point.
