# Filesystem execution protocol

Use this protocol in repository, filesystem, or code-oriented environments.

## 1. Inspect before answering

Do not assume file contents from names alone. Use explicit inspection:

1. list files
2. identify likely relevant files
3. read entrypoint files first
4. use search for terms and headings
5. build a source map for multiple files

Recommended operations:

find <root> -maxdepth 3 -type f
rg -n "keyword" <root>
sed -n '1,220p' <file>

## 2. Source map format

Use internally:

file:
role:
relevant sections:
facts supported:
gaps or uncertainty:
output sections supported:

Show this map only if the user asks.

## 3. Longform in filesystem environments

For MasterZhuyan learning requests, create files by default instead of compressing into chat. Treat deep research and longform as one route: lock enough research/modeling structure to teach accurately, then deliver it through the longform container.

Preferred path:
long_output/<project-slug>/

Use $longform-composer when available. If not, use scripts/mz_longform.py.

After writing, validate and merge. Return paths, not the full text.

## 4. Deep-research packages

Use this section when the request is source-heavy, current, high-risk, multi-file, conflicting, evidence-critical, or explicitly asks for systematic/evidence-grounded learning. For ordinary stable concepts, keep research planning silent and proceed with normal longform; do not treat that as skipping the research/modeling layer.

Durable package options:

1. `scripts/topic_research.py`: use when traceability matters. It creates or validates `framing_brief.md`, `tree.md`, `dispatch.md`, `agent_outputs/*.md`, `source_ledger.jsonl`, `claim_ledger.md`, `synthesis.md`, and `learning_path.md`.
2. `scripts/learning_artifacts.py`: use for standalone knowledge cards or dense study reports that need `core_model`, `reasoning_chain`, `misconceptions`, `retrieval_hooks`, and `provenance`.
3. `schemas/*.schema.json`: use when a custom artifact needs a stable contract: `source_map`, `research_brief`, `evidence_card`, `knowledge_model`, `lesson_plan`, or `quality_report`.

Do not draft chapters before the research layer is locked. The dependency chain is:

```text
research_plan/source_map -> evidence_ledger -> knowledge_model -> chapter_plan -> chapters -> quality_report
```

If a precision anchor in a chapter lacks accepted evidence, fix the evidence, weaken or remove the claim, or mark it unavailable before merge.

## 5. Avoid fake modularity

Role names such as planner, researcher, teacher, worker, and reviewer are not real separate agents unless separate files, scripts, or passes are created. Make modularity real by producing explicit artifacts:

1. source map
2. research brief or research plan
3. evidence ledger or evidence cards
4. knowledge model
5. chapter plan
6. chapter files
7. validation log or quality report
8. final merge

For named prep templates, make the modularity real by creating or loading `.masterzhuyan/prep_templates/<name>.md` and recording the active template in the longform manifest or progress log when practical.

## 6. Multi-agent and multi-pass longform

Entry condition: see `SKILL.md` Multi-agent and multi-pass execution.

For planner schema fields, see `references/masterzhuyan-planning.md` section 4.

Use agents and passes as soon as the integrator can give them a clear bounded artifact. The boundary can be a stable source cluster, research node, lens question, check scope, section draft, or explicit output path; it does not require the whole chapter plan to be finished before useful exploratory or evidence work begins. Create and update the planning layer as the work becomes stable:

1. `notes/source_map.md`: canonical source facts, gaps, contradictions, and uncertainty.
2. `notes/research_plan.md` or `notes/research_brief.md`: learner goal, questions, source strategy, selected spine, completion criteria, and iteration triggers.
3. `notes/evidence_ledger.md`: claim-to-source entries for load-bearing definitions, mechanisms, formulas, thresholds, examples, contradictions, gaps, and precision anchors.
4. `notes/knowledge_model.md`: concepts, relationships, mechanism chain, comparisons, memory anchors, easy errors, and transfer boundaries.
5. `notes/chapter_plan.md`: selected teaching spine, chapter order, `section_id` list, and non-parallel notes.
6. `notes/section_map.md`: one row per worker brief with `split_type`, artifact id, title or question, allowed sources, required anchors, output path, and owner.

If a worker boundary cannot be stated clearly, keep that part with the integrator until it can. If a later artifact such as `notes/source_map.md`, `notes/evidence_ledger.md`, `notes/knowledge_model.md`, or `notes/chapter_plan.md` cannot be stabilized, continue with the bounded portions that remain useful and record the fallback or unresolved gap in `logs/progress.md` or `notes/review.md`.

Worker rules:

1. A worker may write only the assigned `section_id`, `source_id`, `lens_id`, `check_id`, or artifact.
2. A worker may read the available source map, research brief, and chapter plan. It may suggest changes in its own artifact, but canonical planning changes belong to the integrator.
3. A worker may add local teaching examples only as synthesis or inference, not as new source facts.
4. A worker must not resolve contradictions, change the selected spine, widen chapter scope, or edit canonical `chapters/*.md` unless explicitly assigned that file.
5. Worker drafts go under `notes/worker-drafts/`, `notes/source-drafts/`, `notes/lens-drafts/`, or `notes/checks/` according to `references/multi-agent-patterns.md`.

Integrator rules:

1. Promote worker drafts into the manifest-listed `chapters/*.md`; only these chapter files are canonical merge input.
2. Record conflicts, missing drafts, source gaps, and revisions in `notes/review.md`.
3. Run pre-merge checks on chapters, merge through the normal longform path, then run the final quality check on `final/final_merged.md`.
4. If a worker fails, times out, or omits its artifact, fall back to sequentially producing that `section_id` and record the fallback in `notes/review.md`.
5. Do not add workers or passes when their likely output is a duplicate summary, an ungrounded opinion, or a review with no named artifact to resolve.

## 7. Failure handling

If a tool, file, or companion skill is unavailable, state the limitation briefly and use the fallback path. Do not silently skip file-backed longform. If the user explicitly requests no files, brief chat, or stopped file output, or files are unavailable, provide only a delivery, limitation, or handoff note rather than a full chat teaching substitute.
