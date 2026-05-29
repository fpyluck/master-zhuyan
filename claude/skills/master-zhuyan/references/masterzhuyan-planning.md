# MasterZhuyan planning canvas

Use this canvas silently for DeepResearch learning assets. It should improve judgment, not create visible bureaucracy.

## 1. Research-learning canvas

Use this layer for every learning run. For small or stable concepts, shrink artifact scale while the durable package still owns the learner contract, source/evidence state, research-tree decisions, and chapter-plan commitments.

Source map:
Record source -> role -> supported facts -> gaps -> contradictions -> output sections supported. Separate user-provided material, repository/uploaded files, current retrieval, primary sources, secondary sources, and stable conceptual knowledge.

Research brief:
Capture learner goal, primary confusion, entry point, source strategy, success criteria, and research nodes for the durable package. Derive node boundaries from knowledge questions, source structure, dependency order, contradiction risk, domain precision, and teaching value. Each node carries question, source_need, status, next_action, and a falsifiable stop_condition; the node list grows from unresolved questions, not from a predetermined count or chunk structure, and state changes (split, merge, block, retire) are the plan's update mechanism. Candidate node maps or scoring may clarify scope; unresolved or load-bearing nodes flow to evidence work, integrator decisions, or continuation.

Evidence ledger:
Track load-bearing claim -> source_id -> confidence -> teaching use. If a claim cannot be traced, either remove it, label it as inference, or mark it as unavailable.
When a claim depends on a deviation, abnormal state, exception, threshold, risk, grade, comparator, or trend, preserve the reference frame that makes it interpretable. Examples include normal or baseline range, default rule, null model, comparator, unit and scale, API/version contract, nominal operating condition, historical starting point, or ordinary-language meaning.

Knowledge model:
Compress evidence into the smallest teachable model:
1. concept graph: terms and dependencies;
2. mechanism chain: cause, process, result, recognition, boundary;
3. prerequisite map: what the learner must know first;
4. misconception map: likely wrong pattern, why it is tempting, repair cue.

Pedagogy plan:
Let the locked Knowledge Model decide the chapters. Map learner bottleneck, selected core spine, reference frame, precision anchors, examples, memory hooks, comparison anchors, easy-error repair, validation notes, and any final `后续知识拓展` tail section into a lesson plan. Non-chapter items route to their durable surfaces.

Lesson plan:
Each lesson-plan row is derived from the Knowledge Model and carries `purpose`, `required_anchors`, and `completion_criteria`. Required anchors are reference frames, definitions, mechanisms, classifications, thresholds, causes, contraindications, exceptions, formulas, branch criteria, common errors, and source-sensitive limits. Reading maps, source/evidence maps, disclaimers, safety boundaries, artifact inventories, and process summaries belong in `index.md`, `notes/*`, or the final delivery note — never as chapter rows.

Execution support:
After an observable AgenticResearch/tool/worker failure, legacy helpers invoked with `--allow-legacy-helper` may reconstruct the failed research-tree, dispatch, model, reasoning, misconception, retrieval, or provenance portion.
Write useful results as fallback/proposed artifacts for `notes/research_brief.md`, `notes/research_tree.md`, `notes/source_map.md`, `notes/evidence_ledger.md`, `notes/knowledge_model.md`, `notes/chapter_plan.md`, validation notes, or bounded agent outputs.
Record the fallback label, promotion/revision/discard decision, and unresolved gaps in `notes/integrator_decisions.md` and `notes/continuation_map.md` before final merge; absent a concrete fallback label, the validator rejects zero `notes/agent_outputs/`.

## 2. Teaching canvas

Topic title:
Use the most specific title supported by the source.

Domain:
Medicine, mathematics, natural science, engineering, computer science, law, business, humanities, language learning, practical skill, exam review, or mixed.

Knowledge type:
Definition, mechanism, classification, formula, procedure, rule, case pattern, comparison, argument, skill, historical narrative, policy, or research synthesis.

User goal:
Remember, understand, compare, apply, review, create durable notes, or resolve confusion.

Learner bottleneck:
Choose the likely bottleneck: unknown term, unclear mechanism, confusing contrast, weak application, poor recall, missing boundary, or overloaded source material.

Core spine:
Choose the mechanism-first backbone that makes the topic easiest to grasp. Named templates may adjust emphasis or tone, but the plan still needs a coherent mechanism, structure, procedure, or contrast. Switch the spine only when the material gives a concrete trigger: `comparison` for two or more confusable alternatives, `classification` for branch criteria, `procedure` for ordered actions, `formula` for variables or derivation, `rule` for legal/policy/standard elements, and `narrative` for historical or humanities sequences:
1. definition -> elements -> boundary -> example -> confusion
2. cause -> mechanism -> result -> recognition -> handling
3. structure -> function -> consequence -> recognition -> use
4. target -> effect -> use -> risk -> caution
5. condition -> rule -> exception -> consequence -> example
6. problem -> constraint -> method -> process -> validation -> failure mode
7. background -> event/viewpoint -> cause -> process -> influence -> evaluation

Must-preserve details:
Definitions, terms, formulas, thresholds, steps, evidence, examples, exceptions, contraindications, risks, caveats, and original wording that carries meaning.

Contrast anchors:
Similar concepts, diseases, formulas, rules, tools, events, or methods that could be confused.

Precision anchors:
Numbers, thresholds, sequence, named criteria, formula variables, scope limits, and source-sensitive claims.

Reference frame:
The baseline needed to interpret the topic's deviations, exceptions, thresholds, risks, grades, comparisons, or trends. Keep only frames that control understanding or judgment.

Likely easy errors:
False equivalence, reversed causality, overgeneralization, missing exception, wrong application condition, memorizing a category without its branch criterion.

Transfer frontier:
Where this knowledge can be reused, and where it stops applying.

Active prep template:
When a prep template is active (created, updated, or invoked in the current or a recent turn of the same session), load it as planning bias and record only the useful contributions, such as source priority, learner assumptions, explanation taste, chapter emphasis, safety posture, and anti-overconstraint notes. If no template is currently active or no style phrase from it applies, keep the default MasterZhuyan style; ordinary topic words stay source/topic intent.

Chapter emphasis:
Memory, understanding, comparison, easy-error, source/uncertainty, application, or mixed. Emphasis flows into chapter `purpose`, `required_anchors`, and examples inside the single route.

Tail extension:
Plan `后续知识拓展` early if the topic benefits from transfer, adjacent concepts, next-study sequence, or open questions. Finalize it only after the merged synthesis is clear. Route chapter-local transfer cues into `required_anchors` only when they serve that chapter; route broader next-study items to the final tail.

Delivery metadata:
Keep reading order, source/evidence maps, validation status, limitations, process trace, and safety boundary in `index.md`, `notes/*`, or the final delivery note; they stay outside `chapter_plan` unless they teach a substantive reference frame or knowledge overview. For high-risk material the safety boundary is one concise sentence in `index.md` or the final delivery note unless the user asks for a safety lesson.

## 3. Planning preferences

Prefer causal explanation over bare summary when the user asks why or how.

Prefer classification, contrast, and recall anchors when the user asks to remember.

Prefer examples and boundary cases when a concept is abstract.

Prefer domain-specific precision when the topic is legal, medical, engineering, statistical, financial, or safety-related.

Prefer source fidelity when the user supplied material; do not replace the user's material with a generic encyclopedia entry.

If the original material is thin, anchor the answer to what is provided and label missing details.

## 4. Planner handoff schema

Use this as a handoff contract, not visible teaching scaffolding. Each chapter row in `notes/chapter_plan.md` / `lesson_plan` is already the Teaching Composer dispatch record: `chapter_id` becomes `section_id`, `input_refs` and `required_anchors` bound the sidecar, `output_path` is the canonical target, and `completion_criteria` defines done. Extra worker briefs are only for non-chapter source, lens, check, or exceptional follow-up passes.

For concrete file paths, see `references/codex-execution.md` section 6.

topic_title:
domain:
user_goal:
source_map_ref:
selected_spine:
reference_frame:
must_preserve_details:
precision_anchors:
contrast_anchors:
easy_errors:
chapter_list:
lesson_plan:
  - chapter_id:
    title:
    purpose:
    input_refs:
    required_anchors:
    output_path:
    completion_criteria:
tail_extension:
split_strategy:
extra_worker_briefs:
non_parallel_notes:
delivery_metadata:
  index_or_reading_order:
  source_or_evidence_map_refs:
  delivery_note: include one-sentence boundary when useful

node_candidates, when useful:
candidate_id:
nodes:
selection_basis:
why_selected_or_rejected:

Ordinary chapters do not need another brief. Use `source` for locked-source coverage, `lens` for missing angles/examples/contrasts, and `check` for audit or teaching/source review.

Each extra worker brief should include `split_type`, `source_id` or `lens_id` or `check_id`, title or question, allowed sources, required anchors, forbidden scope, output path, and completion criteria. If a non-chapter section truly needs a Teaching Composer pass, give it an explicit `section_id`; ordinary chapter sections consume the existing chapter row.

Stabilize enough of `source_map_ref`, `research_brief`, `evidence_ledger_ref`, `selected_spine`, and `chapter_list` for the worker's artifact to stay bounded. Exploratory workers may suggest planning changes in their own sidecars; the integrator owns any canonical revision to the planning layer.

## 5. Chapter judgment

Keep chapter candidates that carry learning value: mechanism, exception, contrast, example, reference frame, retrieval anchor, easy-error repair, application judgment, or transfer boundary.

Merge or cut candidates that repeat an existing chapter without adding one of those values. Preserve the load-bearing anchors by moving them into the chapter whose `purpose` needs them.

Route delivery metadata to its durable surface: reading guide and reading order to `index.md`, source/evidence maps to `notes/source_map.md` or `notes/citation_audit.md`, process state to `notes/process_trace.md`, open branches to `notes/continuation_map.md`, and user-facing limitations or boundaries to the final delivery note. Titles that describe navigation, sources, safety scope, process, usage, or delivery state are metadata signals. Build `chapter_plan` from the Knowledge Model's first load-bearing reference frame or anchor.

End each chapter on its own purpose; include a bridge such as “下一章怎么接” only when it teaches a prerequisite handoff, contrast, transfer point, or next-study reason.

Follow `SKILL.md` `Output policy` for the merged deep-research plus longform route and delivery/limitation chat notes. Use this canvas only to decide what the output must teach.
