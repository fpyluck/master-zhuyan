# MasterZhuyan longform bridge

Use this only after `SKILL.md` `Output policy` has selected file-backed longform and `$longform-composer` is unavailable. This bridge defines the fallback file protocol; `notes/chapter_plan.md` remains the source of chapter intent.

## 1. Handoff to longform-composer

When $longform-composer is available, pass this compact contract:

topic:
audience:
depth:
chapter emphasis: memory, understanding, comparison, easy-error, or mixed
active prep template: none, or template name plus the useful biases it contributes
language: chinese unless otherwise requested
source map:
knowledge model:
chapter plan:
  learner bottleneck:
  selected spine:
  precision anchors:
  per chapter: purpose, required_anchors, completion_criteria
tail section: 后续知识拓展, if the lesson plan needs one
delivery or limitation note, if any:
final requirement: create manifest, index, chapters, validate, and final/final_merged.md

MasterZhuyan remains responsible for teaching synthesis. Longform-composer manages file organization, validation, and merge.

## 2. Fallback file protocol

If longform-composer is unavailable but filesystem output is available, create:

long_output/<project-slug>/
  manifest.yaml
  index.md
  chapters/
  final/
  notes/

File roles:

manifest.yaml:
Delivery projection of current `notes/chapter_plan.md` rows, active prep template if any, chapter emphasis, audience, depth, source notes, and status.

index.md:
Reading guide, chapter list, source/validation pointers, and one-sentence boundary note when needed.

chapters/*.md:
Canonical teaching chapters. Each chapter satisfies its row-level `purpose`, `required_anchors`, and `completion_criteria`.

final/final_merged.md:
Merged deliverable in manifest order.

notes/:
Non-canonical planning, source, agent output, integrator decision, process trace, continuation, validation, and limitation sidecars. These files are never canonical merge input unless their content is promoted into canonical `chapters/*.md`.

State flow:

1. `notes/chapter_plan.md` stable -> `materialize-chapter-agents` -> `notes/agent_outputs/teaching_composer/<section_id>/<agent_id>.md` -> integrator promotion -> canonical `chapters/*.md`.
2. Other delegated or multi-agent work -> `notes/agent_outputs/<agent_type>/<agent_id>.md` or explicit Agent Fabric path -> `notes/integrator_decisions.md`, `notes/continuation_map.md`, or `notes/process_trace.md`.
3. `materialize-chapter-agents` projects current chapter-plan rows into `manifest.yaml` and `index.md`; `merge_project` reads `manifest["chapters"]` as the delivery order and refuses manifest/chapter-plan drift.

Coordination metadata stays in notes unless the manifest field is already defined for this bridge.

## 3. Recommended fallback commands

When this skill's script is available, initialize the container:

python scripts/mz_longform.py init --root long_output/<project-slug> --title "<title>" --chapter-emphasis "<memory|understanding|comparison|easy-error|mixed>" --chapters "<Knowledge-Model-derived chapter titles>"

After `notes/chapter_plan.md` is stable, materialize the per-chapter Teaching Composer work packages:

python scripts/mz_longform.py materialize-chapter-agents --root long_output/<project-slug>

After writing chapters:

python scripts/mz_longform.py validate --root long_output/<project-slug>
python scripts/mz_longform.py merge --root long_output/<project-slug>

## 4. Chapter writing standard

Each Teaching Composer sidecar answers the row contract assigned by `chapter_plan`: `purpose`, `required_anchors`, `completion_criteria`, and `output_path`. Headings are local choices; cover concepts, logic chain, memory, confusion repair, application, and boundaries only when they serve that row.

Reading maps, source/evidence maps, safety boundaries, artifact inventories, and process explanations belong in `index.md`, `notes/*`, or the final delivery note. A chapter file is the right place only when the content teaches a substantive reference frame or knowledge overview.

Place `后续知识拓展` at one final location: a final chapter or final section when it adds transfer, adjacent concepts, open questions, or next-study value. Chapter-local bridges stay inside a chapter only when they complete that chapter's purpose through prerequisite handoff, contrast, transfer, or next-study reason.

## 5. Chat delivery after longform

Chat delivery: see `SKILL.md` Output policy point 2.
