# MasterZhuyan longform chapter modules

These modules describe chapter content inside the default longform deliverable. They are not output routes. Memory, understanding, comparison, review, and error-repair requests all produce the same file-backed container. Chat is reserved for delivery notes, limitations, and coordination.

## Global chapter rules

1. Use Markdown inside generated `.md` files.
2. Keep every chapter independently useful: purpose, core content, examples or applications, easy errors, and boundaries where relevant.
3. Preserve source-grounded facts, numbers, thresholds, formulas, criteria, examples, warnings, and uncertainty labels.
4. If source material visibly contradicts itself, flag the contradiction before synthesis and separate source facts from corrected or uncertain framing.
5. Do not invent missing details. When a needed point is absent, write: 原始材料未提供，不能确定。
6. Longform does not mean padding. Remove sections that do not improve understanding, memory, judgment, or reuse.
7. If a named prep template is active, let it tune the prose and emphasis, but do not paste the template or force its full outline into every chapter.
8. Use `后续知识拓展` only as a tail chapter or final section generated from the overall lesson plan and merged synthesis. Do not repeat it inside every chapter.
9. Do not add decorative chapter endings such as “下一章怎么接” unless they teach a prerequisite handoff, contrast, transfer point, or next-study reason.

## Memory chapter module

Use this module for 【记忆】, 帮我记, 怎么记, 复习, 考点, 高频, 背诵, 口诀, or exam recall signals.

Possible ingredients. Do not require these headings or all items; `chapter_plan` decides the actual sections:

1. 核心定位
   - 它是什么
   - 所属领域
   - 最重要的记忆价值

2. 记忆主干
   - 3-8 个核心点
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

Possible ingredients. Do not require these headings or all items; `chapter_plan` decides the actual sections:

1. 先给结论
   - 3-5 条真正能支撑理解的结论

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

Possible ingredients. Do not require these headings or all items; `chapter_plan` decides the actual sections:

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

Possible ingredients. Do not require these headings or all items; `chapter_plan` decides the actual sections:

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

## Delivery or limitation note module

Use only after file-backed longform is created, blocked, or intentionally stopped by the user.

Shape:
1. created paths, reading order, validation status, and known limitations; or
2. brief reason the file-backed deliverable could not be produced, plus the smallest useful next step.

Do not use this module to replace the longform learning deliverable with a full chat explanation.

## 后续知识拓展 tail module

Use at the end when the topic benefits from adjacent concepts, transfer paths, prerequisite repairs, next-study sequencing, open questions, or practice directions.

Possible tail ingredients. Do not require these headings or all items; the merged synthesis decides the actual section:

1. 还能往哪里学
   - 2-5 个 genuinely useful adjacent topics or next steps

2. 为什么接这些
   - each item should connect to the merged lesson's mechanisms, contrasts, examples, or application boundary

3. 学的时候先抓什么
   - the first question, prerequisite, or trap to watch for

Do not use this as a decorative closing or a generic bibliography.
