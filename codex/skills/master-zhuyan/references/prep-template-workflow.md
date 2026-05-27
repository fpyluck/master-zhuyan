# Named prep template workflow

A prep template is a user-named teaching-plan overlay. It is meant to adjust MasterZhuyan's attention before writing, not to trap the answer in a rigid mode tree.

## 1. Core idea

Default output routing is defined in `SKILL.md` `Output policy`; this workflow only governs template creation and activation.

Templates are optional and user-activated. MasterZhuyan should not scan, read, or apply saved templates during ordinary default runs. A template only becomes active when the current request explicitly names it, or when the user is creating/updating that template in the current turn.

A named prep template may adjust:

1. source priority;
2. learner role and presumed learning goal;
3. explanation taste;
4. chapter emphasis;
5. safety and verification posture;
6. formatting quietness inside generated markdown files;
7. what not to overdo.

It should not add a second router, force visible checklists, or mechanically fill every section in the user's original prompt.

## 2. Creation trigger

Create a prep template when the user says things like:

1. 保存这个讲解风格，命名为 X；
2. 创建 X 式讲解；
3. 以后按 X 这个教案备课；
4. 把下面这段 prompt 做成本地教案模板；
5. 注册一个 X 风格的学习模板；
6. 把这个模板叫“猫”“狗”“外星人”或任何其他名字。

If a name is provided, use it exactly after sanitizing only filesystem-unsafe characters. If no name is provided but the request clearly asks for a template, choose a short descriptive name from the prompt and report it. Do not block the task solely to ask for a name.

## 3. Storage

When filesystem output is available, store local user templates under:

`.masterzhuyan/prep_templates/<template-name>.md`

Use Markdown with compact frontmatter by default. Markdown is preferred because it is readable, easy to edit, and can preserve the user's original prompt verbatim. JSON is acceptable only when the user explicitly requests JSON or the local project already uses JSON conventions.

Use `scripts/prep_template.py` when helpful for safe creation, listing, and matching. The model may also write the file directly when the template needs richer human judgment.

## 4. Engineering-file shape

A useful `.md` prep template contains:

1. template name and activation aliases;
2. activation examples;
3. core intent in 2-5 lines;
4. source priority, if relevant;
5. preparation attention points;
6. chapter-emphasis tendencies;
7. output taste;
8. safety and uncertainty policy, if relevant;
9. anti-overconstraint note;
10. source prompt excerpt or full source prompt.

Keep the file concise enough that it improves attention rather than consuming context. Preserve the original prompt so the user can revise it later.

## 5. Activation

Before planning a longform deliverable, check only the current request text for explicit template activation phrases such as:

1. `X式讲解`;
2. `X式输出`;
3. `按X教案`;
4. `用X风格`;
5. `X模板`;
6. `按X讲` or `用X讲解`.

Do not activate a template from a bare name alone. This prevents accidental activation when a template name is an ordinary word such as `猫` or `狗`.

If matched, load the local template and apply only the useful parts of it to the current task. If no match exists, use the default MasterZhuyan style.

If multiple templates are mentioned, use the most explicit one. Merge only when the user clearly asks to combine them.

## 6. Precedence

Use this precedence order:

1. current user request;
2. user-supplied source material in the current turn;
3. explicitly activated prep template;
4. MasterZhuyan default teaching philosophy;
5. stable general knowledge.

For high-risk topics, safety and source uncertainty rules remain mandatory. A prep template may make caution stronger, but may not authorize fabricated numbers, doses, citations, guideline years, or case-specific professional decisions.

## 7. Longform integration

When a template is active, record it in the longform project when practical:

1. add `prep_template: <name>` to `manifest.yaml` or mention it in `logs/progress.md`;
2. optionally copy the active template into `sources/prep_template.md` when it helps reproducibility;
3. keep final chat delivery concise and path-focused.

Do not paste the template into chat unless the user asks to see it.

## 8. Anti-overconstraint rule

The saved prompt is a reusable attention lens, not a constitution. During application, extract what the user wants the teacher to notice, prioritize, avoid, and emphasize. Let the named template enrich the selected output route rather than replacing it.
