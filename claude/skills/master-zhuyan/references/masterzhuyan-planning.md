# MasterZhuyan planning canvas

Use this canvas silently for complex answers. It should improve judgment, not create visible bureaucracy.

## 1. Research-learning canvas

Use this layer for every learning run. For simple stable concepts, keep it mental and proceed to the teaching canvas; for source-heavy, current/source-sensitive, high-risk, multi-file, explicitly research-like, or traceability-sensitive tasks, write durable artifacts.

Source map:
Record source -> role -> supported facts -> gaps -> contradictions -> output sections supported. Separate user-provided material, repository/uploaded files, current retrieval, primary sources, secondary sources, and stable conceptual knowledge.

Research brief:
Capture learner goal, primary confusion, entry point, source strategy, success criteria, and dynamic research nodes if a durable package is useful. Node boundaries are chosen by the planner or integrator from knowledge questions, source structure, dependency order, contradiction risk, domain precision, and teaching value. Do not force fixed chunks or fixed counts. Each node needs a falsifiable stop condition; vague goals such as "research thoroughly" are not enough. Candidate node maps or scoring may be written only when they clarify scope, not as a restriction on expansion.

Evidence ledger:
Track load-bearing claim -> source_id -> confidence -> teaching use. If a claim cannot be traced, either remove it, label it as inference, or mark it as unavailable.

Knowledge model:
Compress evidence into the smallest teachable model:
1. concept graph: terms and dependencies;
2. mechanism chain: cause, process, result, recognition, boundary;
3. prerequisite map: what the learner must know first;
4. misconception map: likely wrong pattern, why it is tempting, repair cue.

Pedagogy plan:
Map the knowledge model into chapter order, examples, memory hooks, comparison anchors, easy-error repair, validation notes, and any final `后续知识拓展` tail section. Do not let research artifacts replace teaching judgment.

Execution support:
Use `scripts/topic_research.py` for durable research packages that need `framing_brief.md`, `tree.md`, `dispatch.md`, `source_ledger.jsonl`, `claim_ledger.md`, `synthesis.md`, and `learning_path.md`. Use `scripts/learning_artifacts.py` for knowledge cards or dense study reports that need explicit core models, reasoning chains, misconceptions, retrieval hooks, and provenance.

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

Likely easy errors:
False equivalence, reversed causality, overgeneralization, missing exception, wrong application condition, memorizing a category without its branch criterion.

Transfer frontier:
Where this knowledge can be reused, and where it stops applying.

Active prep template:
If the user explicitly named a local prep template, load it as a soft attention overlay. Record only the useful bias: source priority, learner assumptions, explanation taste, chapter emphasis, safety posture, and anti-overconstraint note. If no template is named, use the default MasterZhuyan style and do not scan the template registry.

Chapter emphasis:
Memory, understanding, comparison, easy-error, source/uncertainty, application, or mixed. Do not turn emphasis into a separate output route.

Tail extension:
Plan `后续知识拓展` early if the topic benefits from transfer, adjacent concepts, next-study sequence, or open questions. Finalize it only after the merged synthesis is clear, and keep it as a tail chapter/section instead of repeating it inside every chapter.

## 3. Planning preferences

Prefer causal explanation over bare summary when the user asks why or how.

Prefer classification, contrast, and recall anchors when the user asks to remember.

Prefer examples and boundary cases when a concept is abstract.

Prefer domain-specific precision when the topic is legal, medical, engineering, statistical, financial, or safety-related.

Prefer source fidelity when the user supplied material; do not replace the user's material with a generic encyclopedia entry.

If the original material is thin, anchor the answer to what is provided and label missing details.

## 4. Planner handoff schema

Use this for bounded multi-agent/delegated runs. Keep it as a handoff contract, not visible teaching scaffolding. Do not populate `worker_briefs` unless workers or distinct passes will produce named artifacts.

For concrete file paths, see `references/filesystem-execution.md` section 6.

topic_title:
domain:
user_goal:
source_map_ref:
selected_spine:
must_preserve_details:
precision_anchors:
contrast_anchors:
easy_errors:
chapter_list:
tail_extension:
split_strategy:
worker_briefs:
non_parallel_notes:

node_candidates, when useful:
candidate_id:
nodes:
selection_basis:
why_selected_or_rejected:

For multi-agent work, set `split_strategy` from `references/multi-agent-patterns.md`. Use `section` for chapter/section drafting, `source` for locked-source coverage, `lens` for missing angles/examples/contrasts, and `check` for audit or teaching/source review.

Each `worker_briefs` entry should include `split_type`, `section_id` or `source_id` or `lens_id` or `check_id`, title or question, allowed sources, required anchors, forbidden scope, output path, and completion criteria.

Stabilize enough of `source_map_ref`, `research_brief`, `evidence_ledger_ref`, `selected_spine`, and `chapter_list` for the worker's artifact to stay bounded. Exploratory workers may suggest planning changes in their own sidecars; the integrator owns any canonical revision to the planning layer.

## 5. Chapter judgment

Do not preserve completeness by mechanically expanding every section. Preserve what carries learning value.

Do not create chapters that merely repeat other chapters. Merge or cut weak chapters while preserving load-bearing mechanisms, exceptions, contrasts, or examples.

Do not add decorative chapter endings such as “下一章怎么接” unless they carry real teaching content: a prerequisite handoff, contrast, transfer point, or next-study reason.

Follow `SKILL.md` `Output policy` for the merged deep-research plus longform route and delivery/limitation chat notes. Use this canvas only to decide what the output must teach.
