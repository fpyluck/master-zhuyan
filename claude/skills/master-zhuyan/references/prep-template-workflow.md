# Named prep template workflow

A prep template is a user-named planning overlay. It extracts reusable attention biases from a saved prompt and feeds them into MasterZhuyan's normal research-to-longform route.

## 1. Core idea

Default output routing is defined in `SKILL.md` `Output policy`; this workflow only governs template creation, activation, and planning bias.

Template lookup is current-turn and explicit: creation/update requests write the template; style phrases such as `X式讲解`, `X模板`, or `用X风格` load the matching local template. Ordinary topic words stay source/topic intent.

A named prep template contributes only the useful biases extracted from the saved prompt: what to prioritize, what the learner is assumed to need, how to pace explanation, what the chapter should emphasize, and how cautious the writing should stay. Templates shape attention, not routing; the current request, current sources, Knowledge Model locking, and chapter planning remain the same route.

## 2. Creation trigger

Create a prep template when the user says things like:

1. 保存这个讲解风格，命名为 X；
2. 创建 X 式讲解；
3. 以后按 X 这个教案备课；
4. 把下面这段 prompt 做成本地教案模板；
5. 注册一个 X 风格的学习模板；
6. 把这个模板叫 `X`、`Y` 或任意用户指定名称。

Template identity resolves in this order: explicit user name -> same name after sanitizing only filesystem-unsafe characters; clear template request without a name -> short descriptive name derived from the prompt and reported back; ambiguous identity that changes activation or storage -> ask one naming question.

## 3. Storage

When filesystem output is available, store local user templates under:

`.masterzhuyan/prep_templates/<template-name>.md`

Use Markdown with compact frontmatter by default. Markdown is preferred because it is readable, easy to edit, and can preserve the user's original prompt verbatim. JSON is acceptable only when the user explicitly requests JSON or the local project already uses JSON conventions.

Use `scripts/prep_template.py` when helpful for safe creation, listing, and matching. The model may also write the file directly when the template needs richer human judgment.

## 4. Engineering-file shape

A useful `.md` prep template has two surfaces:

Required:
- template identity: `template_name` and activation `aliases`;
- the user's original prompt, preserved verbatim so it can be revised later;
- a short anti-overconstraint reminder that the prompt is soft attention, not a rigid branch.

Optional attention biases, included only when the prompt actually carries them, are the prompt signals that should flow into source strategy, planning, chapter emphasis, and prose/safety posture.

Keep the file compact enough that it sharpens attention rather than consuming context.

## 5. Activation

Before planning a longform deliverable, check only the current request text for explicit template activation phrases such as:

1. `X式讲解`;
2. `X式输出`;
3. `按X教案`;
4. `用X风格`;
5. `X模板`;
6. `按X讲` or `用X讲解`.

Activation requires one of the template's `aliases` entries to appear in the current request. The bare template name as a topic word stays source/topic intent, not template activation.

If matched, load the local template and apply only the useful parts of it to the current task. If no match exists, use the default MasterZhuyan style.

If multiple templates are mentioned, use the most explicit one. Merge only when the user clearly asks to combine them.

## 6. Precedence

Use this precedence order:

1. current user request;
2. user-supplied source material in the current turn;
3. explicitly activated prep template;
4. MasterZhuyan default teaching philosophy;
5. stable general knowledge.

Template safety or verification preferences enter planning as attention bias. Source-sensitive specifics still use the normal precision-anchor path: Evidence Ledger support state, unavailable/missing labels, or integrator action.

## 7. Longform integration

When a template is active, record it in the longform project when practical:

1. add `prep_template: <name>` to `manifest.yaml` or mention it in `notes/process_trace.md`;
2. optionally copy the active template into `notes/prep_template.md` when it helps reproducibility;
3. keep the final delivery note concise and path-focused.

Chat reports the active template path or status; template content stays in the local file or `notes/prep_template.md` unless the user asks to view it.

## 8. Anti-overconstraint rule

During application, extract what the user wants the teacher to notice, prioritize, avoid, and emphasize, then pass only those useful biases into source strategy, planning, and prose decisions. The template enriches the route; current task sources, learner goal, Evidence Ledger, and locked Knowledge Model control final structure.
