# Codex-like execution protocol

Use this protocol in repository, filesystem, or code-oriented environments.

## 1. Inspect Before Building The Asset

Filenames are entry candidates only; file facts enter `notes/source_map.md` or chapter drafting only after explicit inspection:

1. list files
2. identify likely relevant files
3. read entrypoint files first
4. use search for terms and headings
5. build a source map for multiple files

Recommended operations:

find <root> -maxdepth 3 -type f
rg -n "keyword" <root>
sed -n '1,220p' <file>

## 2. Source Map Format

For MasterZhuyan DeepResearch, write this as durable `notes/source_map.md`. Use it internally only for non-MasterZhuyan filesystem questions.

file:
role:
relevant sections:
facts supported:
gaps or uncertainty:
output sections supported:

The final chat response stays path-focused; the map lives in the file asset.

## 3. Longform in Codex

For MasterZhuyan learning requests, create files by default instead of compressing into chat. Treat deep research and longform as one route: lock enough research/modeling structure to teach accurately, then deliver it through the longform container.

Preferred path:
long_output/<project-slug>/

Use $longform-composer when available. If not, use scripts/mz_longform.py.

After writing, validate and merge. Return paths, not the full text.

### DeepResearch workbench in Codex

For MasterZhuyan DeepResearch runs, create this canonical workbench under the longform root before drafting canonical chapters. Use `notes/agent_outputs/` as the normal AgenticResearch sidecar area for agent/sub-agent outputs and recorded fallbacks:

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

Use `references/agent-fabric.md` for dispatch cards. Use `references/process-tracing.md` for trace templates.

Agent outputs are sidecars. Canonical content enters final merge only after the integrator promotes it into `chapters/*.md` or canonical notes.

## 4. Deep-research packages

Use this section to keep the DeepResearch workbench coherent. Stable concepts can use a compact research graph and compact artifacts, but they still remain inside the DeepResearch longform route.

Durable package options:

1. `scripts/legacy/topic_research.py --allow-legacy-helper`: 5.26 fallback helper for tree and dispatch mechanics after an observable AgenticResearch/tool/worker failure, or for migration. Route its useful output as fallback/proposed artifacts for `notes/research_brief.md`, `notes/research_tree.md`, `notes/source_map.md`, `notes/evidence_ledger.md`, `notes/knowledge_model.md`, or `notes/agent_outputs/<agent_type>/<agent_id>.md`; canonical updates wait for an entry in `notes/integrator_decisions.md`.
2. `scripts/legacy/learning_artifacts.py --allow-legacy-helper`: 5.26 fallback helper for core models, reasoning chains, misconceptions, retrieval hooks, and provenance after the agentic modeling path fails or leaves a weak model. Route useful content as proposed updates to `notes/knowledge_model.md`, `notes/chapter_plan.md`, validation notes, or bounded agent fallback artifacts; citation and continuation state must be updated before final merge.
3. `schemas/*.schema.json`: use when a custom artifact needs a stable contract: `source_map`, `research_brief`, `evidence_card`, `knowledge_model`, `lesson_plan`, or the legacy-named quality trace report.

Keep canonical artifacts coherent in this order:

```text
research_brief + research_tree + source_map -> evidence_ledger -> knowledge_model -> chapter_plan -> citation_audit -> chapters -> quality_trace
```

The chapter plan is the source of chapter intent; manifest and index are delivery projections derived from it. It must carry the learner bottleneck, selected spine, reference frame when load-bearing, precision anchors, and per-chapter `purpose`, `required_anchors`, and `completion_criteria`. Reading maps, source/evidence maps, safety boundaries, artifact inventories, and process notes stay in `index.md`, `notes/*`, or the final delivery note unless promoted as substantive reference-frame or knowledge-overview content.

Exploratory sidecars, section sketches, and agent notes may be produced earlier when they have a clear scope; the integrator promotes only supported material into canonical notes or chapters.

If a precision anchor in a chapter lacks accepted evidence, fix the evidence, apply `soften_claim`, `omit_claim`, or `mark_unavailable` before merge.

## 5. Artifact-backed modularity

Role labels, passes, and sub-agents earn their place by leaving a named artifact or fallback record that the integrator can accept, revise, reject, or use as fallback evidence. Route each distinct pass to the narrowest artifact it owns:

1. scope, learner goal, and acquisition plan -> `notes/research_brief.md` or `notes/agent_outputs/contract_builder/<agent_id>.md`
2. source acquisition or coverage -> `notes/source_map.md` or `notes/agent_outputs/source_scout/<agent_id>.md`
3. research questions and stop conditions -> `notes/research_tree.md`
4. claims, support state, contradictions, and precision anchors -> `notes/evidence_ledger.md` or `notes/citation_audit.md`
5. teaching model and chapter contract -> `notes/knowledge_model.md` or `notes/chapter_plan.md`
6. dispatch, trace updates, promotions, discarded outputs, and fallbacks -> `notes/process_trace.md`, `notes/integrator_decisions.md`, or `notes/continuation_map.md`
7. teachable synthesis -> promoted `chapters/*.md` and `final/final_merged.md`

For named prep templates, the loaded template lives in `.masterzhuyan/prep_templates/<name>.md`; record the active template in the longform manifest or progress log when practical.

## 6. Multi-agent and multi-pass longform

Entry condition: see `SKILL.md` Multi-agent and multi-pass execution.

For planner schema fields, see `references/masterzhuyan-planning.md` section 4.

Use agents/sub-agents and passes as soon as the integrator can give them a clear bounded artifact. The boundary can be a stable source cluster, research node, lens question, check scope, section draft, or explicit output path; it does not require the whole chapter plan to be finished before useful exploratory or evidence work begins. Create and update the planning layer as the work becomes stable:

When using Agent Fabric, write one dispatch card per agent in `notes/process_trace.md` or `notes/agent_outputs/<agent_type>/<agent_id>.md`. Record every canonical promotion in `notes/integrator_decisions.md`.

1. `notes/source_map.md`: canonical source facts, gaps, contradictions, and uncertainty.
2. `notes/research_brief.md`: learner goal, assumed scope, primary confusion, source strategy, selected spine, success criteria, and continuation seeds.
3. `notes/evidence_ledger.md`: claim-to-source entries for load-bearing definitions, mechanisms, formulas, thresholds, examples, contradictions, gaps, and precision anchors.
4. `notes/knowledge_model.md`: concepts, relationships, mechanism chain, comparisons, memory anchors, easy errors, and transfer boundaries.
5. `notes/chapter_plan.md`: selected teaching spine and lesson-plan rows with `purpose`, `required_anchors`, `output_path`, and `completion_criteria` for each intended chapter. Worker-boundary details and non-chapter-pass exceptions live in `references/agent-fabric.md` and `references/multi-agent-patterns.md`.

A worker boundary is ready when the dispatch card can name scope, output path, completion signal, and canonical targets; until then, the integrator owns that part. If a later artifact such as `notes/source_map.md`, `notes/evidence_ledger.md`, `notes/knowledge_model.md`, or `notes/chapter_plan.md` cannot be stabilized, continue with the bounded portions that remain useful and record the fallback in `notes/process_trace.md`, the decision in `notes/integrator_decisions.md`, and the unresolved gap in `notes/continuation_map.md`.

Artifact-flow contract:

1. Worker scope is an assigned `section_id`, `source_id`, `lens_id`, `check_id`, or artifact path. The worker reads available source map, research brief, evidence ledger, knowledge model, and chapter plan as context, then writes the assigned output under `notes/agent_outputs/<agent_type>/<agent_id>.md` or an explicit Agent Fabric path such as `notes/agent_outputs/teaching_composer/<section_id>/<agent_id>.md`. Workers may name canonical targets; canonical note or chapter edits are written by the integrator after an accept/revise/reject decision.
2. Worker output may contain scoped findings, drafts, local teaching examples labeled as synthesis or inference, and proposed planning changes. It remains sidecar material until the integrator accepts, revises, rejects, or uses it as fallback evidence.
3. Canonical changes flow through the integrator. The integrator records conflicts, missing drafts, source gaps, promotions, discarded outputs, and revisions in `notes/integrator_decisions.md`, then promotes supported material into canonical notes or promoted `chapters/*.md`.
4. Final merge uses only promoted chapter files after pre-merge quality tracing; run the final quality trace on `final/final_merged.md`.
5. Worker failure, timeout, or omitted artifact flows to `notes/process_trace.md`; the integrator sequentially produces the assigned target when useful and records unresolved branches in `notes/continuation_map.md`.
6. A pass counts as agentic only when it leaves a named artifact with scope, output path, and completion criteria that the integrator can accept, revise, reject, or use as fallback evidence.

## 7. Failure handling

If a tool, file, or companion skill is unavailable, state the limitation and keep the intended file-backed DeepResearch route explicit. If the user requests stopped file output, or files are unavailable, provide a limitation note that preserves the intended route, current progress, missing capability, source/uncertainty state, and smallest useful next step as the recoverable state, not a self-contained teaching document.
