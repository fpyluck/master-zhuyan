# MasterZhuyan longform chapter modules

These modules describe chapter content inside the default longform deliverable. They are not output routes. Memory, understanding, comparison, review, and error-repair requests all use the same research-to-teaching spine; file-backed longform is the durable surface. Chat is only for delivery notes, limitation reports, and continuation coordination around that asset.

## Global chapter rules

1. Use Markdown inside generated `.md` files.
2. Keep every chapter independently useful: purpose, core content, examples or applications, easy errors, and boundaries where relevant.
3. Preserve source-grounded facts, numbers, thresholds, formulas, criteria, examples, warnings, uncertainty labels, and any reference frame needed to interpret deviations, grades, risks, trends, or exceptions.
4. If source material visibly contradicts itself, flag the contradiction before synthesis and separate source facts from corrected or uncertain framing.
5. Absent needed details take one of three paths: omit if peripheral; mark unavailable (`原始材料未提供，不能确定。`) if expected; or carry as labeled inference only when the Evidence Ledger already marks the claim as `inferred`. Anything not covered by one of these three paths does not enter the chapter.
6. Keep only sections that improve understanding, memory, judgment, or reuse.
7. If a named prep template is active, let its useful biases tune prose and emphasis; keep template content in the local template file or `notes/prep_template.md`, and let `chapter_plan` choose only the ingredients that serve the current chapter purpose.
8. `后续知识拓展` is planned once and rendered at the tail as a final chapter or final section when the merged synthesis shows transfer, adjacent concepts, open questions, or next-study value.
9. End each chapter on its own purpose; include a bridge such as “下一章怎么接” only when it teaches a prerequisite handoff, contrast, transfer point, or next-study reason.

## Module contract

The modules below are ingredient pools, not fixed outlines. `chapter_plan` chooses only the sections that serve the chapter purpose, renames or merges them freely, and may omit any ingredient that would add padding. Repeated source facts should flow into the first chapter where they become necessary for understanding, memory, comparison, error repair, or judgment.

## Memory chapter module

Use this module for 【记忆】, 帮我记, 怎么记, 复习, 考点, 高频, 背诵, 口诀, or exam recall signals.

Ingredients:

1. 核心定位
   - 它是什么
   - 所属领域
   - 最重要的记忆价值

2. 记忆主干
   - 按章节目的选择若干核心点
   - 每个核心点给关键词、核心含义、适用场景、重要性

3. 必须记住的细节
   - 定义、机制、分类依据、公式或标准、例外、风险、常见错误
   - 只写对学习有承载作用的细节，不机械填满清单

4. 记忆钩子
   - 如果适合，给准确口诀
   - 如果不适合，给逻辑线

5. 30秒回顾
   - 核心是什么
   - 必须记住什么
   - 最容易错什么
   - 一句话总结

## Understanding chapter module

Use this module for 【理解】, 为什么, 原理, 机制, 讲懂, 解释, 推导, 判断逻辑, or application-logic signals.

Ingredients:

1. 先给结论
   - 先给几条真正能支撑理解的结论

2. 这个知识点在解决什么问题
   - 没有它会困惑在哪里
   - 它在领域中的位置

3. 底层逻辑推演
   - 起点
   - 关键前提
   - 核心机制或规则
   - 产生的结果
   - 如何判断或应用
   - 限制、例外或风险

4. 白话解释
   - 用一个准确类比解释
   - 明确类比边界

5. 迁移应用
   - 在题目、实践、相邻知识中的用法
   - 哪里不能迁移

## Comparison chapter module

Use this module for 对比、区别、鉴别、怎么区分、A 与 B, or confusing-neighbor signals.

Ingredients:

1. 一句话先分开
   - 用最短句给决定性区别

2. 本质区别
   - 表面相似点
   - 隐藏差异

3. 判断标准
   - 看什么线索
   - 哪个条件出现就归哪一类

4. 机制或原理区别
   - 为什么它们会表现相似
   - 为什么实际不是一回事

5. 适用场景和误用后果
   - 各自适用哪里
   - 混用会错在哪里

## Easy-error chapter module

Use this module for 易错点、陷阱、容易混淆、错题、风险、边界, and high-stakes caution signals. Include it by default when the topic is exam-facing, professional, safety-sensitive, or source-heavy.

Ingredients:

1. 易错点
   - 错误说法或错误操作
   - 为什么容易错
   - 正确理解

2. 触发线索
   - 看到什么词、条件、数字、图像、场景时要警惕

3. 修正方法
   - 用什么判断链纠错
   - 如何避免下次再错

4. 边界和禁区
   - 不能外推到哪里
   - 哪些信息缺失时不能下结论

## Delivery or boundary note module

Triggers when file-backed longform is created, unavailable, or intentionally stopped.

State → output shape:
- **created**: created paths, reading order, validation status, known limitations
- **unavailable / stopped**: preserved work, missing capability, smallest continuation step

The delivery note carries package status. For high-risk topics, one concise safety boundary sentence belongs here unless the user asked for a safety-focused lesson.

## 后续知识拓展 tail module

Use at the end when the topic benefits from adjacent concepts, transfer paths, prerequisite repairs, next-study sequencing, open questions, or practice directions.

Tail ingredients:

1. 还能往哪里学
   - a few genuinely useful adjacent topics or next steps, sized by transfer value rather than a fixed count

2. 为什么接这些
   - each item should connect to the merged lesson's mechanisms, contrasts, examples, or application boundary; items without that link stay out of the tail

3. 学的时候先抓什么
   - the first question, prerequisite, or trap to watch for

Each tail item names the next object of study, why it follows from this lesson, and what to watch first.
