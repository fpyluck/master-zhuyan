# Deep-research agent coordination patterns

Use this file for bounded multi-agent work in a durable deep-research run from `references/deep-research-execution.md`. For standard multi-agent patterns (section, source, lens, check), use `references/multi-agent-patterns.md`.

For DeepResearch MasterZhuyan runs, use `references/agent-fabric.md` as the primary dispatch contract and this file as the deep-research sequencing adapter. Evidence and model splits map to Agent Fabric as:

```text
evidence split -> evidence_curator
model split -> mechanism_modeler, concept_graph_builder, misconception_repairer, comparison_builder
verification split -> trace_curator plus integrator decision record
```

Deep-research adds two split types: `evidence` and `model`. Use them as bounded artifacts the integrator can merge. Keep canonical evidence and model artifacts coherent, but allow exploratory sidecars, source coverage notes, and model sketches to run as soon as their inputs are clear.

## 1. Sequencing constraint

Canonical evidence, model, and chapter artifacts stabilize in order:

```text
notes/research_brief.md + notes/process_trace.md
  -> evidence_curator agents (parallel within phase)
    -> notes/evidence_ledger.md
      -> model agents (parallel within phase)
        -> notes/knowledge_model.md
          -> teaching_composer / lens / trace_curator agents
```

Evidence workers need at least a research question and source scope.
Model workers need an evidence slice or clearly marked exploratory scope.
Chapter workers need enough knowledge model, source map, or chapter-plan context to stay bounded.

The integrator decides what can be promoted. Unsupported sidecars remain notes, not canonical claims.

## 2. Evidence split

Use for source clusters, assigned sources, or evidence slices that need claim-level extraction.

Brief fields:

```text
split_type: evidence
claim_id: EL-<NNN> or claim_id_prefix: EL-<agent_or_source>
source_scope: <files or source cluster this worker covers>
knowledge_questions: <subset of questions or nodes from notes/research_brief.md>
allowed_sources: <file paths or source refs>
forbidden_scope: <sources not assigned to this worker>
agent_type: evidence_curator
output_path: notes/agent_outputs/evidence_curator/<agent_id>.md
completion_criteria: <all assigned sources have ledger entries; gaps and contradictions flagged>
```

Output: candidate Evidence Ledger entries following `references/deep-research-output-contracts.md` section 4 `Extraction flow`. The worker extracts and tags source-grounded claims, carries reference frames when needed, marks unavailable precision or frame gaps, and leaves synthesis or chapter drafting to later artifacts.

The integrator merges evidence drafts into `notes/evidence_ledger.md`. When two workers report contradictory claims from different sources, the integrator creates a `status: contradicted` entry for both and writes a `contradiction_note`.

## 3. Model split

Use for Evidence Ledger slices or clearly scoped exploratory evidence slices that need a bounded pass over relationships, misconceptions, gaps, or precision anchors.

Brief fields:

```text
split_type: model
model_id: MO-<NNN>
agent_type: mechanism_modeler|concept_graph_builder|misconception_repairer|comparison_builder
model_scope: mechanisms|concepts|relationships|misconceptions|comparisons|precision_anchors|gaps
evidence_ids: [EL-NNN, ...] (assigned ledger entries)
output_path: notes/agent_outputs/<agent_type>/<agent_id>.md
completion_criteria: <all assigned ledger entries mapped to model entries; low-confidence and gap items flagged>
```

Output: the relevant section of `references/deep-research-output-contracts.md` section 3. Keep chapter structure suggestions as optional sidecar notes unless explicitly assigned.

The integrator merges model drafts into `notes/knowledge_model.md`. Conflicts in concept definitions are resolved using source confidence and evidence_ids: prefer the entry with more `high`-confidence ledger references.

## 4. Verification split (check extension)

Use the `check` split type from `references/multi-agent-patterns.md` for post-draft evidence verification. Extend the finding format for deep-research:

```text
gap: <claim in chapter not in Evidence Ledger, or inferred without flag>
severity: high|med|low
source_needed: yes|no
claim_id: <EL-NNN — existing ledger entry covering this gap that was not cited; omit if no match exists>
suggested_action: revise|mark-uncertainty|add-evidence-entry|cut
```

Write verification output to `notes/agent_outputs/trace_curator/<agent_id>.md` or directly into `notes/integrator_decisions.md` when the integrator performs the review. Severity `high` means a precision anchor (threshold, dose, criterion, formula) in the draft has no `accepted` Evidence Ledger entry; record the anchor state, mitigation, and any next acquisition handoff in `notes/continuation_map.md`.

## 5. Integrator responsibilities

1. Create a usable `notes/research_brief.md` and `notes/process_trace.md` before promoting worker output into canonical evidence or model artifacts.
2. Merge evidence drafts into `notes/evidence_ledger.md`; resolve contradictions.
3. Merge model drafts into `notes/knowledge_model.md`; resolve concept conflicts.
4. Verify chapters against the Evidence Ledger before merge and record quality tracing (Phase 6 of execution protocol).

If any phase artifact fails to be produced, the integrator may narrow the worker boundary, continue sequentially for that phase, or proceed with the portions whose evidence and model are stable. Record the concrete agent/tool/worker failure in `notes/process_trace.md`, the fallback decision in `notes/integrator_decisions.md`, and unresolved gaps in `notes/continuation_map.md`.

## 6. Anti-patterns

Boundary failures — do not use deep-research agent patterns for:

1. Chapter expansion before the evidence/model layer is ready. After evidence and Knowledge Model are locked, simple chapter expansion can use `section` split from `references/multi-agent-patterns.md`, but it remains constrained by DeepResearch evidence, citation, and model artifacts.
2. Named roles without a bounded artifact, traceable execution record, or integrator accept/revise/reject path.
3. Promoting exploratory model notes as canonical claims before their evidence slice is accepted.

Single-source requests are not an anti-pattern by themselves. Use DeepResearch for a single paper, screenshot, note, or concept, with compact but real artifacts.
