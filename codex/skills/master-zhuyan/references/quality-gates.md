# MasterZhuyan quality gates

Run these checks silently before finalizing a longform deliverable or delivery/limitation chat note.

For source-heavy, current, high-risk, multi-file, conflicting, evidence-critical, or explicitly research-like tasks, also use `references/deep-research-quality-gates.md`. That file is the stronger verifier for source boundaries, claim traceability, inference labels, knowledge-model coverage, memory support, easy-error repair, and risk-domain handling.

## 1. Longform delivery gate

Default learning output is complete only when it has:

1. manifest or output plan;
2. index or reading order;
3. chapter files;
4. final/final_merged.md;
5. validation note or validation pass;
6. concise chat delivery with paths, reading order, validation status, and known limitations.

If the user explicitly requested no files, brief chat, or stopped file-backed output, or files are unavailable, say why the longform deliverable cannot be produced in this turn and provide only a limitation or handoff note. Do not replace the learning deliverable with chat content.

## 2. Chapter value gate

Each chapter should make at least one of these better:

1. understanding of the mechanism or logic;
2. memory and retrieval;
3. comparison or discrimination;
4. easy-error repair;
5. source-grounded coverage;
6. application or judgment.

Remove or merge chapters that do not improve understanding, memory, judgment, or reuse.

## 3. Coverage gate

When supported by the source or required by the task, preserve:

1. definitions;
2. mechanisms;
3. classifications and branch criteria;
4. thresholds, formulas, variables, and units;
5. process steps;
6. examples;
7. exceptions;
8. risks and limitations;
9. similar-concept distinctions;
10. easy errors;
11. application or judgment logic.

Do not add unsupported details just to fill a chapter.

## 4. Source and uncertainty gate

Separate:

1. source-grounded facts;
2. teacher framing or synthesis;
3. inferred points;
4. missing or uncertain details;
5. visible contradictions in the supplied material.

Do not invent doses, numbers, thresholds, legal consequences, guideline years, recommendation grades, prices, current facts, software behavior, citations, patient-specific decisions, or case-specific professional recommendations.

If precision is important but absent, say it is not provided or requires verification.

If the supplied source visibly contradicts itself or contains a self-evident error, flag the issue before teaching. In high-risk domains, do not replace the source with unsourced general knowledge.

For research-style runs, every load-bearing precision anchor in the final chapters should be supported by an accepted evidence entry or explicitly labeled as missing, uncertain, or inferred. A high-risk precision anchor without traceable support blocks final merge.

## 5. Teaching value gate

The deliverable should make clear:

1. what the knowledge is;
2. why it works or why it is true;
3. how to judge or apply it;
4. what it is not;
5. what is easily confused;
6. what is easiest to forget.

If the draft is mostly labels and lists, add causal links, examples, or contrasts.

## 6. Responsiveness gate

Before final merge, verify that the chapter plan and final draft answer the research brief's `primary_confusion` and satisfy its `success_criteria`. If either is missing, return to the research planner, evidence ledger, or chapter plan instead of adding prose.

## 7. Multi-agent gate

For multi-agent or delegated runs, check before merge:

1. Did each worker draft map to exactly one assigned `section_id`, `source_id`, `lens_id`, `check_id`, or artifact?
2. Did every worker use the stable or provided source map, selected spine, chapter plan, or bounded sidecar context available for its assignment?
3. Were conflicts, missing drafts, fallbacks, and source gaps recorded in `notes/review.md`?
4. Were worker drafts promoted into manifest-listed `chapters/*.md` before merge, instead of being merged directly?
5. For `source`, did the integrator use coverage findings without reopening parallel source intake?
6. For `lens`, did the integrator synthesize useful angles instead of copying perspective drafts as standalone chapters?
7. For `check`, did each finding use `gap`, `severity`, `source_needed`, and `suggested_action`?

After merge, run the final quality gate on `final/final_merged.md`, not only on individual worker drafts.

For explicit multi-agent deep-research runs, also verify the relevant handoff order from `references/deep-research-agent-patterns.md`: `research_plan -> evidence_ledger -> knowledge_model -> chapter_plan`. Do not merge chapter drafts that skipped the evidence or model layer needed for their claims.

## 8. Prep-template gate

When a named prep template is active, check silently:

1. Did the template sharpen the teaching bias?
2. Did current user material still outrank the template?
3. Did the template avoid becoming a visible rigid checklist?
4. If the template requested plain text, did that become quieter prose inside longform rather than accidental chat teaching?

## 9. Final quality gate

Before delivery, ask silently:

1. Is the first chapter or index useful?
2. Is the chapter structure helping rather than showing off?
3. Is there at least one strong mechanism, contrast, example, or recall anchor where needed?
4. Did any chapter repeat the same idea without adding value?
5. Would a strong teacher keep this deliverable in this shape?

Revise toward clarity and usefulness, not merely toward more files.
