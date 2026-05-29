# Deep-research execution protocol

Use this protocol as the durable AgenticResearch route for MasterZhuyan. It coordinates active acquisition, evidence curation, knowledge modeling, teaching composition, ProcessTracing, and longform integration through file-backed artifacts.

Use this protocol for MasterZhuyan runs. Artifact size follows the research graph, but every run keeps the source, evidence, model, decision, citation, and continuation state that final claims need.

## 1. Default route and depth

MasterZhuyan uses this AgenticResearch route by default. The following signals expand depth, add more agent passes, strengthen evidence work, or make the workbench more explicit:

1. The user asks for deep research, systematic synthesis, no token saving, agent delegation, evidence-grounded learning, or file-backed study assets.
2. The user supplies dense note sets, a single source that deserves deep modeling, or multiple distinct source files.
3. The material contains visible contradictions, multiple competing frameworks, or domain-sensitive precision claims.
4. The topic requires separating current/guideline-dependent facts from stable conceptual knowledge.
5. The supplied material lacks a load-bearing definition, mechanism, prerequisite, comparator, example, contradiction resolution, or source basis needed for a strong teaching model.
6. A chapter plan built without evidence verification would carry real risk if a precision anchor is wrong.

For a single-source deep dive, use the same DeepResearch protocol. Smaller scopes may produce fewer artifacts, but direct integrator-only production is a recorded fallback after native agent/tool/worker failure, not a route selected because the topic looks simple.

## 2. DeepResearch phase sequence

Each canonical phase leaves the state the next canonical phase needs. Agents/sub-agents may run in parallel inside or across phases when their output paths are distinct and their results remain sidecars until the integrator promotes them.

### Phase 1: Contract and workbench

Maintain the canonical DeepResearch workbench and AgenticResearch sidecar area:

```text
notes/process_trace.md
notes/research_brief.md
notes/research_tree.md
notes/source_map.md
notes/evidence_ledger.md
notes/knowledge_model.md
notes/chapter_plan.md
notes/integrator_decisions.md
notes/citation_audit.md
notes/continuation_map.md
notes/agent_outputs/
```

`notes/research_brief.md` contains:

```text
topic_title:
user_goal:
primary_confusion:
success_criteria:
learner_bottleneck:
source_map_ref:
scope:
research_questions:
selected_spine:
chapter_emphasis:
must_preserve_details:
precision_anchors:
agent_fabric_plan:
initial_continuation_branches:
revision_reasons:
```

`notes/research_tree.md` contains the dynamic research tree:

```text
node_id:
question:
why_it_matters:
source_need:
owner:
status: open | searching | reading | evidence_ready | modeled | retired | blocked
evidence_ids:
next_action:
stop_condition:
```

Write `contract_built` into `notes/process_trace.md`.

Keep notes concise when the research graph is small, but keep canonical source, evidence, model, decision, and continuation state available before final promotion. When native sub-agent/tool/worker execution is unavailable or fails, record the concrete failure label (for example `agent_runtime_unavailable`, `agent_worker_failed`, or `tool_failed`) in `notes/process_trace.md` and `notes/integrator_decisions.md`, then produce a fallback/proposed artifact under `notes/agent_outputs/` for the same DeepResearch target.

### Phase 2: Active source acquisition

Dispatch Source Scout agents from `references/agent-fabric.md` for acquisition nodes. The integrator performs acquisition directly only as a recorded fallback for a native agent/tool/worker failure and writes the same target artifact plus an integrator decision record.

Use active acquisition for:

```text
missing definition
missing mechanism
missing prerequisite
missing comparator
missing example
contradiction
current/source-sensitive claim
multimodal source gap
```

Each Source Scout writes:

```text
notes/agent_outputs/source_scout/<agent_id>.md
```

The integrator merges source entries into:

```text
notes/source_map.md
```

Write `source_acquisition` into `notes/process_trace.md`.

Use this tool chain discipline:

```text
search -> candidate source
read/fetch/browser/OCR/MCP -> source card
source card -> evidence card
evidence card -> knowledge model claim
knowledge model claim -> chapter sentence or marked limitation
```

Search retrieves candidates; reading creates source cards; source cards produce evidence. Unread, snippet-only, or partially read candidates stay in `notes/source_map.md` with `read_state`, attempted method, access time when available, failure reason, and next retrieval option. The Evidence Ledger receives claims only from read source cards, or from a snippet explicitly labeled as the studied source.

Source card fields:

```text
source_id:
title:
source_type:
access_method:
retrieved_at:
locator:
read_state: full | partial | snippet_only | unavailable
supports_questions:
must_preserve:
evidence_card_ids:
limitations:
failure_label:
```

### Phase 3: Evidence curation

Dispatch Evidence Curator agents over source clusters. If a native agent/tool/worker failure forces sequential fallback, the integrator writes the Evidence Ledger directly and records that fallback. Evidence work follows `references/deep-research-output-contracts.md` section 4 `Extraction flow`: claim -> support state -> reference frame when needed -> integrator action for unavailable precision or frame.

```text
notes/agent_outputs/evidence_curator/<agent_id>.md
```

Curator outputs are candidate ledger entries. The integrator merges accepted, contradicted, inferred, and missing entries into:

```text
notes/evidence_ledger.md
```

Write `evidence_curation` into `notes/process_trace.md`.

### Phase 4: Knowledge modeling

Dispatch modeling agents for breadth, dissent, comparison, misconception repair, and mechanism repair:

```text
mechanism_modeler
concept_graph_builder
misconception_repairer
comparison_builder
```

Outputs go to:

```text
notes/agent_outputs/<agent_type>/<agent_id>.md
```

The integrator merges model entries into:

```text
notes/knowledge_model.md
```

Write `knowledge_modeling` into `notes/process_trace.md`.

### Phase 5: Chapter planning and teaching composition

Create:

```text
notes/chapter_plan.md
```

`notes/chapter_plan.md` is the lesson plan produced from the locked Knowledge Model. It must include the learner bottleneck, selected core spine, reference frame when load-bearing, precision anchors, and one row for each intended knowledge chapter with `purpose`, `required_anchors`, `output_path`, and `completion_criteria`. Reading maps, evidence/source maps, safety boundaries, artifact inventories, and process summaries stay in `index.md`, `notes/*`, or the final delivery note unless promoted as substantive reference-frame or knowledge-overview content.

Dispatch follows the Teaching Composer contract in `references/agent-fabric.md`: one agent per chapter row, with row-local `purpose`, `required_anchors`, `output_path`, `completion_criteria`, and relevant evidence/model context while the integrator owns cross-chapter coherence. If a native agent/tool/worker failure forces sequential fallback, the integrator drafts the assigned chapter target from the locked Knowledge Model and records the fallback:

```text
notes/agent_outputs/teaching_composer/<section_id>/<agent_id>.md
```

After `notes/chapter_plan.md` is stable, materialize these work packages when this script is the active longform carrier:

```text
python scripts/mz_longform.py materialize-chapter-agents --root <longform-root>
```

The integrator promotes chapter-ready content into:

```text
chapters/*.md
```

Write `chapter_composition` into `notes/process_trace.md`.

### Phase 6: Integration, tracing, and panorama delivery

Dispatch Trace Curator for agent contribution maps, citation state, continuation maps, and delivery metadata. If native runtime failure prevents that pass, record the failure label and have the integrator write the same trace artifacts through a fallback/proposed sidecar and decision record.

Update:

```text
notes/integrator_decisions.md
notes/citation_audit.md
notes/continuation_map.md
index.md
```

Merge longform:

```text
final/final_merged.md
```

Write `integration` into `notes/process_trace.md`.

Before merge, write `notes/citation_audit.md`:

```text
claim_or_section:
evidence_ids:
source_ids:
locator_check:
support_state: supported | partial | inferred | contradicted | missing
integrator_action: accept | revise | soften_claim | omit_claim | mark_unavailable | dispatch_agent | record_continuation
```

Any load-bearing claim, high-risk precision anchor, or contradiction controlling the user's main question with `missing` or `contradicted` citation support enters `integrator_action` as a merge blocker. Merge proceeds only after the claim has accepted evidence or an integrator decision records `soften_claim`, `omit_claim`, `mark_unavailable`, `dispatch_agent`, or `record_continuation` for the final teaching target.

Before final merge, every chapter row's evidence-bearing `required_anchors` must be resolved by a Teaching Composer sidecar and a chapter-level citation audit row. Resolution means the anchor's evidence ID is used in the sidecar and tied to the chapter `output_path`, `chapter_id`, or `final/final_merged.md` in `notes/citation_audit.md`, or the audit/integrator decision records the action that keeps it out of the final teaching body.

## 3. Continuation handling

When a source, tool, or agent output is unavailable, record the missing item in `notes/process_trace.md` or `notes/integrator_decisions.md`, add an entry to `notes/continuation_map.md` when the gap is useful to resume, and continue integrating the artifacts already produced.

When a Knowledge Model contains important gaps, dispatch Source Scout or Mechanism Modeler for the gap and record the result. If the gap remains, place it in `notes/continuation_map.md` with a concrete next agent handoff card.

If one source, tool, or agent path is unavailable, record the unavailable path and continue through available artifacts when useful. A full file-backed completion claim requires the actual container artifacts; if file output is unavailable, provide a limitation note with the intended file-backed route, missing capability, and smallest useful next step.

Continuation carries resumable work after the final claim is safe: a missing load-bearing definition, unsupported high-risk precision anchor, or unresolved contradiction that controls the user's main question first changes the final claim through accepted evidence or `soften_claim`, `omit_claim`, or `mark_unavailable`; only non-core or already-resolved gaps move unchanged to continuation.

## 4. Agent loop and failure handling

When an agent or integrator performs a research node, run the same compact loop:

```text
decide: pick the next node and tool/action from notes/research_tree.md
act: search, read, extract, model, critique, draft, or audit
observe: record source/evidence/result/failure
update: revise research_tree, source_map, evidence_ledger, knowledge_model, or chapter_plan
stop: node stop_condition met, node retired, or blocker recorded with next_action
```

Failure labels:

```text
agent_runtime_unavailable
agent_worker_failed
not_found
access_blocked
tool_failed
source_partial
contradicted
insufficient_precision
out_of_scope
```

Step, source, or runtime bounds keep the run inspectable, not exhaustive. When a bound stops a load-bearing node, the unresolved support state flows to `notes/integrator_decisions.md`; it can enter `notes/continuation_map.md` only after the affected final claim is evidenced, softened, omitted, or marked unavailable.
