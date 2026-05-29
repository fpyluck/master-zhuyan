# MasterZhuyan quality tracing

`quality-gates.md` is a legacy filename. Treat this reference as a quality tracing and enhancement map contract, not as a pass/fail gate. Use it when a longform deliverable, research package, or limitation note needs extra teaching/source review beyond container validation. Hard stops are reserved for unsupported load-bearing claims, high-risk precision anchors, unresolved contradictions that control the answer, and outputs that miss the learner's primary confusion.

For source-heavy, current, high-risk, multi-file, conflicting, evidence-critical, or explicitly research-like tasks, also use `references/deep-research-quality-gates.md`. Translate that verifier's findings into the trace records below: visible support state, integrator action, and continuation candidates.

## 0. Enhancement map record

Write quality findings into the run's durable artifacts:

1. `notes/integrator_decisions.md` for resolved decisions, promotions, revisions, softened claims, omitted claims, and merge notes.
2. `notes/continuation_map.md` for open questions, missing evidence, follow-up branches, and dispatchable next-agent cards.
3. `notes/process_trace.md` for phase-level quality state and why the integrator chose the next action.
4. `notes/agent_outputs/trace_curator/<agent_id>.md` when a delegated Trace Curator performs the review.

Each record traces: finding -> support_state -> evidence_refs/teaching_effect -> integrator_action -> next_agent/output_path/user_visible_note. `create_missing_artifact` is only for quality-trace container or required-file repair; Citation Audit uses its claim-support enum and does not use that action. Use it whenever a quality finding matters:

```text
check_id:
artifact:
finding:
support_state: strong | partial | inferred | missing | contradicted | not_applicable
evidence_refs:
teaching_effect:
integrator_action: accept | revise | create_missing_artifact | dispatch_agent | soften_claim | omit_claim | mark_unavailable | record_continuation
next_agent:
output_path:
user_visible_note:
```

End the review with a concise quality summary:

```text
overall_state:
strong_zones:
partial_zones:
open_continuations:
next_agent_candidates:
user_visible_limitations:
```

## 1. Longform container trace

Record the container state for:

1. manifest or output plan;
2. index or reading order;
3. chapter files;
4. `final/final_merged.md`;
5. validation note or validation pass;
6. concise final delivery response with paths, reading order, validation status, and known limitations.

If a required artifact is missing, record `support_state: missing` with `integrator_action: create_missing_artifact` when the integrator can repair the container now; otherwise add a continuation entry with the exact missing path and next action. Continuation entries carry non-core expansion work or gaps already softened, omitted, or marked unavailable; a core evidence gap needed for the final answer stays in `notes/integrator_decisions.md` as an `integrator_action` until it is acquired, softened, omitted, or marked unavailable. If files are unavailable, record the boundary and provide a limitation note with the intended file-backed route, missing capability, and smallest useful next step.

## 2. Chapter value trace

For each chapter, record which learning value it improves:

1. mechanism or logic;
2. memory and retrieval;
3. comparison or discrimination;
4. easy-error repair;
5. source-grounded coverage;
6. application or judgment.

Metadata-heavy chapter candidates (reading map, source/evidence map, safety boundary, artifact inventory, or process explanation) route to `index.md`, `notes/*`, or the final delivery note. A chapter carries chapter value when it teaches one of the learning values above or a substantive reference frame/knowledge overview; otherwise merge, rewrite, or remove it, record the decision in `notes/integrator_decisions.md`, and revise `chapter_plan` from the Knowledge Model's first load-bearing reference frame or anchor.

## 3. Coverage trace

When supported by the source or required by the task, trace coverage for:

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

Missing required coverage flows to the quality record as `support_state: missing|partial` with `integrator_action: revise|dispatch_agent|record_continuation`. Chapter text receives only details backed by the Evidence Ledger, labeled as inference, or marked unavailable/missing.

## 4. Source and uncertainty trace

Separate these states in the Evidence Ledger, Knowledge Model, chapter notes, or final limitations:

1. source-grounded facts;
2. teacher framing or synthesis;
3. inferred points;
4. missing or uncertain details;
5. visible contradictions in the supplied material.

Treat doses, numbers, thresholds, legal consequences, guideline years, recommendation grades, prices, current facts, software behavior, citations, and professional or patient-specific recommendations as precision anchors. They enter final output only through accepted evidence, explicit missing/unavailable state, or labeled inference where allowed.

If precision is important but absent, write that the source does not provide it or that verification is required. If the supplied source visibly contradicts itself or contains a self-evident error, flag the issue before teaching and keep source facts separate from corrected or uncertain framing.

For research-style runs, every load-bearing precision anchor in the final chapters should be supported by an accepted evidence entry or explicitly labeled as missing, uncertain, or inferred. A high-risk precision anchor without traceable support becomes an integrator action: `dispatch_agent`, `soften_claim`, `omit_claim`, or `mark_unavailable`; add a concrete continuation card only after the final claim is safe.

For high-risk topics, the default safety boundary is one concise sentence in `index.md` or the final delivery note. Longer safety discussion becomes chapter content only when the learner asked to study safety workflows, contraindications, risk boundaries, or professional decision limits as knowledge content.

## 5. Teaching value trace

The deliverable should make clear:

1. what the knowledge is;
2. why it works or why it is true;
3. how to judge or apply it;
4. what it is not;
5. what is easily confused;
6. what is easiest to forget.

If the draft is mostly labels and lists, enhance it with causal links, examples, contrasts, retrieval anchors, or boundary cases. Record the change as an integrator revision instead of adding decorative sections.

## 6. Responsiveness trace

Compare the chapter plan and final draft with the research brief's `primary_confusion` and `success_criteria`.

Record one of these states:

1. `strong`: the output directly answers the confusion and satisfies the success criteria.
2. `partial`: the output is useful but leaves named criteria weak or unsupported.
3. `missing`: the output is structurally complete but does not answer the learner's real need.

For `partial` or `missing`, revise the research brief, evidence ledger, chapter plan, or draft. If the weakness needs more information, dispatch the next agent or record the continuation target.

## 7. Multi-agent trace

For multi-agent or delegated runs, record before and after merge:

1. each worker output path under `notes/agent_outputs/<agent_type>/<agent_id>.md`, plus any named canonical target the integrator may later update;
2. assigned boundary such as `section_id`, `source_id`, `lens_id`, `check_id`, `node_id`, or artifact path;
3. input artifacts each worker actually used;
4. artifacts each worker wrote or modified;
5. promotions, edits, rejected material, conflicts, fallbacks, and source gaps in `notes/integrator_decisions.md`;
6. unresolved branches and next handoff cards in `notes/continuation_map.md`;
7. final review of `final/final_merged.md`, not only individual worker drafts.

For explicit multi-agent deep-research runs, preserve the evidence/model sequence from `references/deep-research-agent-patterns.md` and the dispatch contract from `references/agent-fabric.md`. If a worker skipped evidence or model support needed for its claims, record the anchor state and either revise through the integrator, dispatch a support agent, or move the unsupported branch into the continuation map.

## 8. Prep-template trace

When a named prep template is active, record silently whether:

1. explicit activation and template path or status were captured;
2. useful template biases reached planning or prose decisions;
3. current user material, learner goal, Evidence Ledger, and Knowledge Model still controlled final structure;
4. style-phrase biases landed as prose adjustments such as word choice, pacing, or framing rather than restructuring chapters into question-answer blocks, thematic-summary sections, standalone explainer inserts, or visible rigid checklists.

If the template weakens source fit, mechanism clarity, or responsiveness, record an integrator revision and restore the current task's source and learner goal as the higher priority.

## 9. Final enhancement pass

Before delivery, ask silently:

1. Is the first chapter or index useful?
2. Is the chapter structure helping rather than showing off?
3. Is there at least one strong mechanism, contrast, example, or recall anchor where needed?
4. Did any chapter repeat the same idea without adding value?
5. Would a strong teacher keep this deliverable in this shape?

Revise toward clarity and usefulness. Record open branches as continuation candidates instead of pretending the learning asset is exhaustively complete.
