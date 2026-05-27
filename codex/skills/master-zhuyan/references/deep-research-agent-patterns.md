# Deep-research agent coordination patterns

Use this file when bounded multi-agent work can improve a durable deep-research run from `references/deep-research-execution.md`. For standard multi-agent patterns (section, source, lens, check), use `references/multi-agent-patterns.md`.

Deep-research adds two split types: `evidence` and `model`. These are sequenced and cannot run in parallel with each other. Use them when they produce bounded artifacts the integrator can merge; otherwise run the same passes sequentially.

## 1. Sequencing constraint

Dependent deep-research phases still need clean handoffs, but this is a sequencing aid, not a reason to avoid agents. The integrator may use exploratory workers early when they produce sidecar questions, source coverage notes, or planning options. Canonical evidence, model, and chapter artifacts should then lock in order:

```
research_plan (locked)
  → evidence workers (parallel within phase)
    → evidence_ledger (locked)
      → model workers (parallel within phase)
        → knowledge_model (locked)
          → section/lens/check workers (parallel within phase)
```

Evidence workers need at least a stable research question and source scope.
Model workers need a stable evidence slice.
Chapter workers need enough knowledge model or chapter-plan context to stay bounded.

Skipping the relevant handoff produces chapters that are not evidence-grounded; using early sidecar workers to clarify the handoff is allowed.

## 2. Evidence split

Use when the source set is large or heterogeneous enough that single-pass intake risks missing key evidence.

Brief fields:

```text
split_type: evidence
evidence_id: EV-<NNN>
source_scope: <files or source cluster this worker covers>
knowledge_questions: <subset of questions from research_plan>
allowed_sources: <file paths or source refs>
forbidden_scope: <sources not assigned to this worker>
output_path: notes/evidence-drafts/<evidence_id>/<agent>_ledger.md
completion_criteria: <all assigned sources have ledger entries; gaps and contradictions flagged>
```

Output: Evidence Ledger entry format from `references/deep-research-output-contracts.md` section 2. Extract and tag only. Do not synthesize, interpret beyond what the source says, or draft chapters.

The integrator merges evidence drafts into `notes/evidence_ledger.md`. When two workers report contradictory claims from different sources, the integrator creates a `status: contradicted` entry for both and writes a `contradiction_note`.

## 3. Model split

Use when the locked Evidence Ledger would benefit from a separate bounded pass over relationships, misconceptions, gaps, or precision anchors.

Brief fields:

```text
split_type: model
model_id: MO-<NNN>
model_scope: concepts|relationships|misconceptions|precision_anchors|gaps
evidence_ids: [EL-NNN, ...] (assigned ledger entries)
output_path: notes/model-drafts/<model_id>/<agent>_model.md
completion_criteria: <all assigned ledger entries mapped to model entries; low-confidence and gap items flagged>
```

Output: the relevant section of `references/deep-research-output-contracts.md` section 3. Do not draft chapters or propose chapter structure.

The integrator merges model drafts into `notes/knowledge_model.md`. Conflicts in concept definitions are resolved using source confidence and evidence_ids: prefer the entry with more `high`-confidence ledger references.

## 4. Verification split (check extension)

Use the `check` split type from `references/multi-agent-patterns.md` for post-draft evidence verification. Extend the finding format for deep-research:

```text
gap: <claim in chapter not in Evidence Ledger, or inferred without flag>
severity: high|med|low
source_needed: yes|no
evidence_id: <EL-NNN if a ledger entry exists but was missed>
suggested_action: revise|mark-uncertainty|add-evidence-entry|cut
```

Severity `high` means a precision anchor (threshold, dose, criterion, formula) in the draft has no `accepted` Evidence Ledger entry. These must be resolved before merge. They are not optional.

## 5. Integrator responsibilities

The integrator owns synthesis at every phase boundary:

1. Lock `notes/research_plan.md` before any worker begins evidence work.
2. Merge evidence drafts into `notes/evidence_ledger.md`; resolve contradictions.
3. Merge model drafts into `notes/knowledge_model.md`; resolve concept conflicts.
4. Use `notes/knowledge_model.md` as primary input for chapter planning (Phase 4 of execution protocol).
5. Verify chapters against the Evidence Ledger before merge (Phase 6 of execution protocol).
6. Record all conflicts, fallbacks, and resolution decisions in `notes/review.md`.

If any phase artifact fails to be produced, the integrator may narrow the worker boundary, continue sequentially for that phase, or proceed only with the portions whose evidence and model are stable. Record the fallback or unresolved gap in `notes/review.md`.

## 6. Anti-patterns

Do not use deep-research agent patterns for:

1. Single-source requests: use the standard adaptive loop.
2. Simple chapter expansion where no evidence grounding is needed: use `section` split from `references/multi-agent-patterns.md`.
3. Creating role names without artifacts: calling an agent a "researcher" without requiring it to produce Evidence Ledger entries is fake modularity (`references/codex-execution.md` section 5).
4. Running evidence and model phases in parallel: the Evidence Ledger must be complete before the Knowledge Model begins.

An agent that produces no locked artifact is not doing deep-research work.
