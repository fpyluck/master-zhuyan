# Deep-research artifact contracts

These contracts define the internal working-notes formats used by `references/deep-research-execution.md`. They are not user-facing output; they support evidence-grounded chapter drafting.

## 1. Research Planner

File path: `notes/research_plan.md`

Fields:

```text
topic: <topic title>
domain: <domain>
knowledge_questions:
  - <specific question this research must answer>
source_requirements:
  - <source type needed>: <why it is needed>
uncertainty_budget: low|medium|high
depth_required: shallow|standard|deep
completion_criteria: <when evidence is sufficient to teach from>
```

Use `uncertainty_budget: low` for clinical, legal, engineering-safety, or financial topics where wrong precision has real consequences. Use `high` only when conceptual richness matters more than precision (humanities, exploratory work).

## 2. Evidence Ledger

File path: `notes/evidence_ledger.md`

One entry per claim that will appear in teaching:

```text
claim_id: EL-<NNN>
claim: <exact claim as it will be used in teaching>
source_ref: <file name, section, page, or url>
evidence_type: definition|mechanism|classification|threshold|formula|step|example|exception|risk|contraindication
confidence: high|med|low|inferred
status: accepted|uncertain|contradicted|missing
contradiction_note: <if status=contradicted, describe both positions and their sources>
```

Confidence levels:
- `high`: source is unambiguous on this point
- `med`: interpretation was needed; the claim is a reasonable reading
- `low`: source is thin, indirect, or old
- `inferred`: no source supports this; derived by reasoning from other claims

Aggregate uncertainty flag: if more than 30% of precision-anchor entries (`evidence_type: threshold|formula|criteria|step`) are `uncertain` or `contradicted`, add a section note before chapter drafting: "该主题存在重要不确定性，以下内容来自现有证据，建议参阅原始文献。"

## 3. Knowledge Model

File path: `notes/knowledge_model.md`

### Concepts

One entry per named concept:

```text
concept: <name>
definition: <definition drawn from source>
evidence_ids: [EL-NNN, ...]
confidence: high|med|low
role: core|supporting|boundary
```

`role: core` means the concept is load-bearing for understanding the topic.
`role: boundary` means the concept defines the scope limits of the topic.

### Relationships

One entry per meaningful link between concepts:

```text
from: <concept>
to: <concept>
relation: causes|enables|inhibits|classifies|contrasts|requires|produces
evidence_ids: [EL-NNN, ...]
confidence: high|med|low
```

Only record relationships that affect understanding or application. Do not create relationship entries for obvious or purely organizational links.

### Misconceptions

One entry per known confusion pattern:

```text
misconception: <the wrong belief>
why_wrong: <mechanism or evidence that makes it wrong>
repair_anchor: <correct understanding in one sentence>
evidence_ids: [EL-NNN, ...]
```

Every misconception entry must have a `repair_anchor`. A flag without a repair is not actionable for teaching.

### Precision anchors

One entry per threshold, dose, formula, criterion, or sequence step that must not be blurred in teaching:

```text
anchor: <exact value, rule, or sequence>
context: <when and where this applies>
source_ref: <file name, section, page>
evidence_id: EL-<NNN>
```

Precision anchors that lack a source_ref must be marked with `confidence: inferred` in their Evidence Ledger entry and labeled as inference in the chapter.

### Gaps

One entry per knowledge question from the Research Planner that could not be answered:

```text
question: <from research_plan knowledge_questions>
status: missing|thin|conflicted
action: omit|flag-in-chapter|verify-before-teach
```

`omit`: exclude silently because the point is not load-bearing.
`flag-in-chapter`: include a note in the chapter that this is unresolved.
`verify-before-teach`: do not teach this claim; tell the user the gap exists and what kind of source is needed.
