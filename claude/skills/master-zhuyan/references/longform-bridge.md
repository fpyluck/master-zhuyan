# MasterZhuyan longform bridge

Use this only after `SKILL.md` `Output policy` has selected file-backed longform and `$longform-composer` is unavailable. This bridge defines the fallback file protocol.

## 1. Handoff to longform-composer

When $longform-composer is available, pass this payload conceptually:

topic:
audience:
depth:
chapter emphasis: memory, understanding, comparison, easy-error, or mixed
active prep template: none, or template name plus the 3-6 useful biases it contributes
language: chinese unless otherwise requested
chapter plan:
tail section: 后续知识拓展, if the lesson plan needs one
source map:
required MasterZhuyan sections:
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

Required files:

manifest.yaml:
Authoritative chapter order, active prep template if any, chapter emphasis or mode, audience, depth, source notes, and status.

index.md:
Reading guide and chapter list.

chapters/*.md:
One coherent chapter per file. Each chapter must be independently useful and should include objective, core content, examples or applications, easy errors, and chapter summary when appropriate.

final/final_merged.md:
Merged deliverable in manifest order.

notes/:
Optional planning, source, worker-draft, review, validation, and limitation sidecars. These files are never canonical merge input unless their content is promoted into manifest-listed `chapters/*.md`.

For multi-agent runs, use `notes/worker-drafts/<section_id>/<agent>_draft.md`, `notes/source-drafts/<source_id>/<agent>_coverage.md`, `notes/lens-drafts/<lens_id>/<agent>_draft.md`, or `notes/checks/<check_id>/<agent>_findings.md` for sidecar artifacts, and `notes/review.md` for conflicts, missing artifacts, fallbacks, and post-merge review. Do not add new manifest status values or register sidecar artifacts as chapters. If longform-composer accepts extra manifest keys, coordination metadata may be recorded as shallow optional scalars such as `coordination_mode: sidecar-artifacts` and `sidecar_artifacts_root: notes`; omit these fields when the manifest schema is strict.

## 3. Recommended fallback commands

When this skill's script is available, use:

python scripts/mz_longform.py init --root long_output/<project-slug> --title "<title>" --mode "<mode>" --chapters "<chapter 1>|<chapter 2>|<后续知识拓展 if useful>"

After writing chapters:

python scripts/mz_longform.py validate --root long_output/<project-slug>
python scripts/mz_longform.py merge --root long_output/<project-slug>

## 4. Chapter writing standard

Each chapter should answer the learning questions that its `chapter_plan` assigns. These are optional ingredients, not required headings:

1. What is this chapter for?
2. What are the core concepts?
3. What is the logic chain?
4. What must be remembered?
5. What is easily confused?
6. How is it applied?
7. What is the boundary or limitation?

For learning chapters, keep the MasterZhuyan logic and use markdown headings.

Use `后续知识拓展` only as a final chapter or tail section when it adds transfer, adjacent concepts, open questions, or next-study value. Do not add decorative chapter endings such as “下一章怎么接” unless they carry real teaching content.

## 5. Chat delivery after longform

Chat delivery: see `SKILL.md` Output policy point 2.
