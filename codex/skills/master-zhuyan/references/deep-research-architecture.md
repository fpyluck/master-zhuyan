# MasterZhuyan Deep Research Architecture

本文描述 MasterZhuyan 重构后的 DeepResearch 教学交付架构。目标不是把教学过程机械化，而是让“证据链、专家知识建模、学习科学、长文交付”之间有可追踪的契约。

## 1. 总体目标

MasterZhuyan 的核心产物不是普通摘要，而是一份能帮助学习者理解、记住、辨析、避错和复用的教学交付。运行时应同时满足四个要求：

1. Deep Research 的证据链：每个关键说法尽量能回到 source、locator、evidence_card。
2. 专家教师的知识建模：先找到定义、机制、分类、边界、相似概念和应用判断，再写章节。
3. 学习科学的记忆与易错修复：把记忆钩子、提取线索、常见错误、修正链路纳入模型，而不是最后附会。
4. 长文交付系统：默认生成 manifest、index、chapters、final_merged、validation note，并在聊天中只给简洁交付说明。

## 2. 运行流水线

推荐流水线如下：

```text
User Request
  -> Research Contract + Dynamic Research Tree
  -> Tool/Source Acquisition
  -> Source Map + Source Cards
  -> Evidence Ledger + Evidence Cards
  -> Cross-check + Contradiction/Gap Repair
  -> Knowledge Model
  -> Lesson Plan / Chapter Plan
  -> Teaching Composer sidecars per chapter row
  -> Integrator-promoted Evidence-bound Chapters
  -> Citation Audit + Integrator Decisions
  -> final/final_merged.md + Delivery Note
```

### 2.1 Source Intake

Source Intake 负责读取用户材料、图片、文件、仓库内容或检索结果。它只做事实入口，不急着教学综合。

输出对象是 `source_map`。source_map 应回答：

- 有哪些来源；
- 每个来源支持哪些主题；
- 哪些定义、公式、阈值、例外、警告、原句必须保留；
- 哪些信息缺失；
- 哪些来源之间有矛盾。

如果没有可用来源，也要生成极简 `notes/source_map.md`，记录尝试过的读取/检索/OCR/MCP 路径、失败原因和不可确定的 claims；后续对象只接收带标签的稳定概念框架、unavailable claim 或 limitation，缺失细节进入 `notes/evidence_ledger.md`、`notes/integrator_decisions.md` 或 `notes/continuation_map.md`。

### 2.2 Research Brief

Research Brief 是 Planner 的紧凑契约。它把用户目标转成可执行研究问题和教学主干。

它应回答：

- 学习者到底想记忆、理解、比较、应用、复习，还是解决混淆；
- 最可能的学习瓶颈是什么；
- 本轮教学的范围是什么；
- 哪些问题必须被证据回答；
- 采用哪条 core spine，例如“定义 -> 要素 -> 边界 -> 例子 -> 混淆”或“基线 -> 扰动 -> 机制 -> 结果 -> 判断 -> 边界”；
- 什么时候需要回到 Planner。

Research Brief 不负责写最终章节。它负责防止后续写作跑偏。

### 2.3 Evidence Cards

Evidence Card 是最小证据单元。它把一个 teachable claim 连接到 source_id、locator、证据类型、可信度和教学用途。

Evidence Card 不要求覆盖每一句话，只要求覆盖关键承重信息：

- 定义；
- 机制；
- 分类标准；
- 公式、阈值、变量、单位；
- 步骤；
- 例外和禁区；
- 反例或矛盾点；
- 高风险或来源敏感的判断。

Evidence Card 应尽量短。它服务于可追溯性和质量检查，不是摘抄库。

### 2.4 Knowledge Model

Knowledge Model 是专家教师层。它把证据组织成学习者能理解的知识结构。

它应包含：

- core_spine：最小教学主干；
- concepts：核心概念及其角色；
- relations：概念之间的因果、组成、限制、对比、前后关系；
- mechanisms：从条件到过程再到结果的解释链；
- comparisons：相似概念的决定性区分标准；
- reference_frame：解释偏离、阈值、例外、风险、等级、比较或趋势所需的基线、默认规则、对照、单位尺度、版本契约、额定状态、历史起点或通常含义；
- precision_anchors：不能模糊的数字、条件、术语、公式、限定；
- memory_anchors：可提取、可复述的记忆抓手；
- easy_errors：错误模式、为什么错、如何修；
- transfer_boundaries：能迁移到哪里，不能外推到哪里。

这一层决定“教什么”和“按什么逻辑教”。如果 Knowledge Model 很弱，长文会变成堆材料。

### 2.5 Lesson Plan

Lesson Plan 把 Knowledge Model 转成可交付章节。它不是固定模板，而是章节契约。

Knowledge Model 决定章节：learner bottleneck、core spine、precision anchors 和 lesson plan 生成知识章节；交付元信息、来源目录和安全免责声明流向 `index.md`、`notes/*` 或 delivery note，不得从其中倒推章节结构。

每个 chapter 至少说明：

- chapter_id；
- title；
- purpose；
- emphasis，例如 memory、understanding、comparison、easy_error；
- input_refs，例如 evidence_card、knowledge_model 部分或 source；
- required_anchors；
- output_path；
- completion_criteria。

Lesson Plan 还应列出 deliverables 和 review_tasks，确保最终长文容器完整。元信息保留在 `index.md`、`notes/*` 或最终 delivery note；`chapter_plan` 和章节文件只承载真正讲解 reference frame 或知识总览的内容。

高风险领域只需要在元信息层保留一句边界，例如：`本文仅作学习材料；急症、具体用药和个体治疗按当地医院/医生流程处理。` 只有当用户明确要求学习安全流程或风险边界本身时，才把它作为知识章节。

### 2.6 Compose、Merge、Quality Trace

Teaching Composer sidecars 根据 Lesson Plan 的每个章节 row 写入 `notes/agent_outputs/teaching_composer/<chapter_id>/...`。写作可调整表达；任何 `source_map`、`core_spine` 或 `chapter_plan` 的事实承诺变化先回到 Planner 或 `notes/integrator_decisions.md`，再由 Integrator 进入章节。

Merge Longform 将章节合并为 final_merged，并保证阅读顺序自然、章节之间不重复、不互相矛盾。

Quality Trace 在最终交付前记录质量状态和增强动作：

- delivery trace：文件容器是否完整，缺失 artifact 写入 continuation；
- chapter value trace：每章是否真的改善理解、记忆、判断或复用；
- coverage trace：定义、机制、分类、阈值、例外、风险是否被保留；
- source uncertainty trace：来源事实、教师综合、推断、缺失和矛盾是否分开；
- teaching value trace：是否讲清是什么、为什么、怎么判断、不是什么、易混什么、易忘什么；
- final enhancement trace：最终文档哪些区域强，哪些区域需要下一轮增强。

## 3. 对象关系

对象之间推荐使用稳定 id 或路径引用，不要求硬编码成一个大型嵌套对象。

```text
source_map
  contains sources[]
  records evidence_card_ids[] as source-to-Evidence-Ledger claim/card links
  records contradictions[]

research_brief
  references source_map_ref
  defines research_questions[]
  defines selected_spine
  records revision_reasons[]

evidence_card
  references source_id
  may reference related_question_ids[]
  supports knowledge_model elements

knowledge_model
  references research_brief_ref
  references source_map_ref
  uses evidence_ids inside concepts, relations, mechanisms, anchors, errors

lesson_plan
  references research_brief_ref
  references knowledge_model_ref
  turns model pieces into chapter_plan[]

quality_trace_report
  references lesson_plan_ref
  references final_output_ref
  records support_state, integrator_action, and continuation candidates
```

这种关系有三个好处：

1. 可追踪：最终章节里的关键判断能回到证据卡和来源。
2. 可迭代：发现缺口时能知道该回到 source_map、research_brief 还是 lesson_plan。
3. 可分工：多 Agent 场景下可以按 source_id、chapter_id、check_id 或 evidence_card_id 分配任务。

## 4. 什么时候修订规划或派 Agent 继续增强

只要后续阶段发现“继续写会制造假完整、假精确或低质量教学”，就修订对应 artifact 或派 Agent 继续增强。常见修订信号如下。

### 4.1 从 Source Intake 回 Planner

回到 Planner，当：

- 来源不足以支撑用户要求的范围；
- 用户材料存在关键矛盾，且矛盾会影响 core_spine；
- 高风险领域缺少必要年份、标准、剂量、阈值、法条、版本或适用条件；
- 图片或文件关键部分无法识别；
- 用户目标过宽，现有材料只能覆盖一部分。

Planner 应更新 scope、research_questions、must_preserve_details 或 revision_reasons。必要时在最终交付中明确“原始材料未提供，不能确定”。

### 4.2 从 Evidence Cards 回 Planner

回到 Planner，当：

- 关键 research_question 没有证据卡回答；
- 多张证据卡互相矛盾且无法通过限定条件解决；
- 证据只支持事实罗列，不足以支持选定的因果或机制主干；
- 发现新概念改变了原来的章节重点。

Planner 应调整 selected_spine、chapter_emphasis 或研究问题，而不是让 Drafter 硬写。

### 4.3 从 Knowledge Model 回 Planner

回到 Planner，当：

- core_spine 不能解释主要材料；
- concepts 很多但 relations 很弱，说明模型只是词表；
- mechanisms 缺少条件、过程、结果或边界；
- comparisons 没有决定性区分标准；
- easy_errors 只是泛泛提醒，不能形成修正链；
- transfer_boundaries 无法判断。

Planner 应重选教学主干，或缩小范围。

### 4.4 从 Lesson Plan 回 Planner

回到 Planner，当：

- chapter_plan 出现重复章节；
- 某章没有学习价值，只是在展示结构；
- 某章只是导航、来源、过程、交付状态或安全边界元信息；
- 章节顺序不符合学习路径；
- required_anchors 无来源支撑；
- deliverables 不满足长文交付要求；
- 多 Agent 分工没有锁定 source_map、selected_spine 和 chapter_plan。

Planner 应回到 Knowledge Model，合并、删除、重排章节，或补充证据需求。被删除的元信息应移动到 `index.md`、`notes/*` 或 delivery note，而不是被扩写成章节。

### 4.5 从 Quality Trace 修订规划或继续增强

当 Quality Trace 记录 `support_state: missing|contradicted|partial`，并且问题不是简单局部修文可以解决时，修订 `notes/research_brief.md`、`notes/source_map.md`、`notes/evidence_ledger.md`、`notes/knowledge_model.md` 或 `notes/chapter_plan.md`，也可以派 Source Scout、Evidence Curator、Mechanism Modeler 或 Trace Curator 继续补强。

典型情况：

- 关键来源缺失；
- 高风险断言未验证；
- 章节没有产生学习价值；
- 最终文档重复严重；
- 教学主干与用户目标不匹配；
- 呈现为摘要而非专家教学；
- 证据、推断、缺失、矛盾混在一起。

如果只是措辞不清、某章例子不够、局部记忆钩子弱，可以由 Drafter、Teaching Composer 或 Integrator 修订，不必改动上游规划。

## 5. 契约使用原则

1. 字段克制：schema 是最低可验证契约，不是完整数据库设计。
2. 必填克制：只强制对象身份、主题和核心内容，避免让实现为了填字段而造内容。
3. 证据不等于堆引用：Evidence Card 只承载关键教学判断。
4. 教学模型先于章节：先把知识结构建好，再决定章节。
5. 长文不是 padding：章节必须改善理解、记忆、辨析、避错或复用。
6. 不确定要显式：缺失、推断、矛盾和需要验证的内容必须标出来。
7. Planner 可迭代：迭代不是失败，而是防止假完整的质量机制。

## 6. Schema 文件清单

- `schemas/source_map.schema.json`：来源、覆盖、缺口、矛盾。
- `schemas/research_brief.schema.json`：用户目标、研究问题、教学主干、迭代触发器。
- `schemas/evidence_card.schema.json`：单条证据与教学用途。
- `schemas/knowledge_model.schema.json`：概念、关系、机制、对比、记忆锚点、易错修复。
- `schemas/lesson_plan.schema.json`：章节计划、交付物、质量任务。
- `schemas/quality_report.schema.json`：legacy filename；用于 quality trace、support state、integrator action 和 continuation candidates。
