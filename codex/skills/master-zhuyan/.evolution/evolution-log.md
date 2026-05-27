# evolution log

## 2026-05-25 - upgrade-skill

- evidence used: user reported that modularized MasterZhuyan still underperformed in Codex-like use and did not reliably trigger longform-composer.
- hypothesis: performance was blocked by soft routing, overlong trigger description, ambiguous artifact responsibilities, insufficient file-inspection protocol, and lack of a local longform fallback.
- files changed: SKILL.md, agents/openai.yaml, references/router.md, references/masterzhuyan-planning.md, references/masterzhuyan-output-contracts.md, references/domain-kernels.md, references/dense-topic-scaffold.md, references/teaching-advantage-overlay.md, references/quality-gates.md, references/longform-bridge.md, references/codex-execution.md, references/regression-prompts.md, scripts/mz_longform.py, tests/test_mz_longform.py.
- validation result: pending at edit time; package and tests must pass before delivery.
- regressions checked: memory mode, understanding mode, comparison mode, longform escalation, chat-only long answer, current/source-sensitive caution.
- next improvement idea: add a small behavior test harness that checks generated outputs against regression-prompts.md with model-in-the-loop evaluation.

## 2026-05-25 performance-first revision

- mode: upgrade-skill
- evidence used: user feedback that the previous revision made behavior harder/stricter but the desired goal was better model performance.
- hypothesis: answer quality should improve more from adaptive tutor judgment, explanation exemplars, misconception repair, contrastive teaching, and taste gates than from stronger routing alone.
- files changed: SKILL.md, agents/openai.yaml, references/adaptive-router.md, references/teaching-performance-playbook.md, references/exemplar-patterns.md, references/masterzhuyan-planning.md, references/quality-gates.md, references/teaching-advantage-overlay.md, references/regression-prompts.md; removed obsolete hard router reference file.
- validation result: smoke_test passed; pytest passed; package validation passed.
- regressions checked: formal memory/understanding contracts preserved; longform-composer handoff preserved; bundled longform fallback preserved; anti-overrigidity behavioral prompts added.
- next improvement idea: run side-by-side answers on a fixed benchmark set and compress the best-performing patterns into exemplar-patterns.md.

## 2026-05-25 longform-first simplification

- mode: simplify-routing
- evidence used: user explicitly requested one default route: file-backed longform for all learning requests, with chat-only only after explicit user request or unavailable files.
- hypothesis: performance should improve by removing route hesitation; memory, understanding, comparison, review, and easy-error work become chapter emphases inside one durable deliverable instead of competing answer modes.
- files changed: SKILL.md, references/adaptive-router.md, references/masterzhuyan-output-contracts.md, references/quality-gates.md, references/longform-bridge.md, references/codex-execution.md, references/exemplar-patterns.md, references/masterzhuyan-planning.md, references/dense-topic-scaffold.md, references/teaching-performance-playbook.md, references/regression-prompts.md.
- validation result: smoke_test passed; unittest discovery passed (26 tests); py_compile passed; skill consistency check had 0 failures and one registry warning because MasterZhuyan is not a collaborative skill.
- regressions checked: default longform from bare material, memory signal as chapter emphasis, understanding signal as chapter emphasis, comparison signal as chapter emphasis, explicit chat-only exception, stop-file-output exception, current/source-sensitive caution, source contradiction handling.
- next improvement idea: add a behavior harness that confirms ordinary learning prompts produce a manifest, chapters, validation note, and final/final_merged.md unless explicitly chat-only.

## 2026-05-25 named prep-template overlay

- mode: upgrade-skill
- evidence used: user reported that over-branching reduced model performance, that fixed longform output now works well, and requested a local, user-named lesson-prep prompt file that can be activated later.
- hypothesis: MasterZhuyan can gain controllable teaching direction without reintroducing router bloat by treating named lesson-prep prompts as soft attention overlays before longform chapter planning.
- snapshot: .evolution/snapshots/20260525T133310_274249Z
- files changed: SKILL.md, agents/openai.yaml, references/adaptive-router.md, references/codex-execution.md, references/longform-bridge.md, references/masterzhuyan-output-contracts.md, references/masterzhuyan-planning.md, references/quality-gates.md, references/regression-prompts.md, references/prep-template-workflow.md, scripts/prep_template.py, scripts/smoke_test.py, tests/test_prep_template.py.
- validation result: smoke_test passed; pytest passed with 30 tests; py_compile passed; local_validate passed; package validation passed before archive creation.
- regressions checked: longform-first default preserved, memory/understanding remain chapter emphases, chat-only remains explicit exception, no forced mode-choice question for named styles, local template creation, explicit activation behavior.
- next improvement idea: add an optional model-evaluated benchmark comparing default MasterZhuyan vs named prep-template outputs on the same medical textbook prompt to measure whether the overlay improves focus without adding rigidity.

## 2026-05-25 generic named-template cleanup

- mode: upgrade-skill
- evidence used: user clarified that the earlier named style was only an example; any arbitrary name such as 猫, 狗, 外星人, or another label should be a user-created optional style overlay.
- hypothesis: template support should remain a low-friction attention overlay by removing example-specific templates, avoiding default template scans, and activating only on explicit style phrases.
- snapshot: .evolution/snapshots/pre_generic_template_fix_20260525.zip
- files changed: SKILL.md, agents/openai.yaml, references/adaptive-router.md, references/masterzhuyan-planning.md, references/prep-template-workflow.md, references/regression-prompts.md, scripts/prep_template.py, scripts/smoke_test.py, tests/test_prep_template.py; removed the example-specific bundled prep template from the active package.
- validation result: smoke_test passed; pytest passed with 31 tests; py_compile passed.
- regressions checked: default longform remains unchanged, templates are not read on default runs, arbitrary names are supported, explicit style activation works, bare ordinary words do not activate templates.
- next improvement idea: add a tiny real-output benchmark comparing default style and one user-created style without adding any new routing branch.

## 2026-05-26 deep-research learning architecture

- mode: multi-agent upgrade-skill
- evidence used: user requested a new MasterZhuyan architecture based on ChatGPT/Gemini/Perplexity/Claude-style deep research, then explicitly asked Codex and Claude to use agent teams to implement it.
- hypothesis: MasterZhuyan should keep longform-first delivery but add conditional research artifacts for source-heavy, current, high-risk, multi-file, conflicting, or evidence-critical learning tasks: source intake, research brief, evidence ledger, knowledge model, lesson plan, quality verifier, and regression prompts.
- collaboration: Codex acted as integrator; Codex subagents produced architecture/schema/quality-regression drafts; Claude reviewed and created execution/output/agent-pattern references. Claude's preserved constraints: deep research is conditional, not a new output channel; `research_plan -> evidence_ledger -> knowledge_model -> chapter_plan` must stay sequenced; high-severity precision-anchor evidence failures block merge.
- files changed: SKILL.md, agents/openai.yaml, references/masterzhuyan-planning.md, references/codex-execution.md, references/quality-gates.md, references/regression-prompts.md, references/deep-research-architecture.md, references/deep-research-execution.md, references/deep-research-output-contracts.md, references/deep-research-agent-patterns.md, references/deep-research-quality-gates.md, schemas/source_map.schema.json, schemas/research_brief.schema.json, schemas/evidence_card.schema.json, schemas/knowledge_model.schema.json, schemas/lesson_plan.schema.json, schemas/quality_report.schema.json.
- validation result: schema JSON validation passed with jq; py_compile passed for scripts; smoke_test passed; unittest discovery passed with 26 tests; skill_consistency_check passed with 0 failures and one expected registry warning because MasterZhuyan is not a collaborative skill. `python3 -m pytest` could not run because pytest is not installed in this environment.
- regressions checked: longform-first remains default, chat-only remains explicit exception, named templates remain soft overlays, topic_research and learning_artifacts are formally connected, deep-research multi-agent work remains explicit and artifact-bounded.
- next improvement idea: add model-evaluated behavior tests that score generated longform outputs against `references/regression-prompts.md`, especially claim traceability, inference labels, and precision-anchor blocking.

## 2026-05-26 merged research-longform hardening

- mode: buddys + multi-agent upgrade-skill
- evidence used: user requested removal of "Chinese-first", elimination of chat-mode teaching, a merged deep-research + longform route, model-inferred research nodes with soft target around five, mechanism-first teaching that templates may adjust, default bounded multi-agent/multi-pass execution, and removal of mandatory owner taste review.
- collaboration: Codex integrated; Claude and Gemini reviewed the route and both returned REFINE, emphasizing mandatory synthesis responsiveness, concrete examples/hooks, bounded artifacts before multi-agent expansion, and explicit fallback boundaries. Two Codex subagents implemented disjoint script/test and documentation lanes.
- files changed: SKILL.md, agents/openai.yaml, references/adaptive-router.md, references/masterzhuyan-planning.md, references/deep-research-execution.md, references/deep-research-agent-patterns.md, references/multi-agent-patterns.md, references/codex-execution.md, references/regression-prompts.md, references/quality-gates.md, references/masterzhuyan-output-contracts.md, references/exemplar-patterns.md, references/deep-research-quality-gates.md, references/longform-bridge.md, references/dense-topic-scaffold.md, references/deep-research-architecture.md, scripts/topic_research.py, tests/test_topic_research.py.
- behavior changes: MasterZhuyan now treats research/modeling plus file-backed longform as one default learning route; chat is only for delivery, limitation, or coordination notes. Research node planning uses model-inferred nodes with a soft target around five and a compact scored-node-candidate artifact when scope is uncertain. Mechanism-first is the default spine, with operational switches for comparison, classification, procedure, formula, rule, and narrative topics. Multi-pass is default for substantive learning runs and multi-agent work is allowed when bounded artifacts and one integrator are present. Artifact validation now rejects empty examples and teaching hooks, and synthesis/coverage gates reject structurally traceable but non-responsive research.
- validation result: smoke_test passed; unittest discovery passed with 28 tests; py_compile passed; skill_consistency_check passed with 0 failures and one expected registry warning because MasterZhuyan is not a collaborative skill.
- next improvement idea: add a semantic/model-evaluated responsiveness scorer for `primary_confusion` and `success_criteria`, because the current script-level alignment check is deterministic lexical overlap by design.
