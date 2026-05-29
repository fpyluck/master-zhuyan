# MasterZhuyan 深度研究式学习质量追踪

本文件用于最终输出前的静默质量追踪：记录来源、证据、教学价值、风险边界和后续增强方向，避免“看起来很长、实际不稳”的学习材料被当成完整结论。硬阻断只保留给会破坏主问题答案的缺口：无证据的核心结论、高风险精确锚点、控制判断的矛盾、以及没有回应用户主要困惑的最终稿。

它是追踪工具，不是章节模板；只记录会改变证据、教学或交付判断的发现，不要求正文按下列编号展开。

适用场景：

1. 用户要求系统整理、深度讲解、研究式学习、长文、MD 文件、课程化输出。
2. 输入包含截图、上传文件、长材料、多来源材料、当前信息或高风险领域。
3. 主题需要机制推理、比较辨析、记忆支持、错因修复或专业边界。

## 使用原则

1. 先检查来源和证据，再检查教学表达。
2. 先保护事实边界，再追求讲得漂亮。
3. 每个结论都应能归入：来源事实、证据支持、教师综合、明确推断、未知/待核验。
4. 深度研究式学习不是堆章节；章节必须增加理解、记忆、判断或复用价值。
5. 高风险关键建议需要来源支撑；缺少来源时记录为 `missing`/`uncertain` 并进入 `integrator_action`：`dispatch_agent`、`soften_claim`、`omit_claim` 或 `mark_unavailable`；来源核验后方可进入正文。

## 1. 来源追踪

状态流：识别 -> 分类 -> 路由。

1. 识别与分类：所有材料区分“本轮提供”和“模型综合”；多源时维护内部 source map（schema 见 `references/deep-research-output-contracts.md`）。时效性内容（指南、法规、价格、版本、政策、标准、新闻等）需要当前来源或显式标注需验证。图片/截图只用可见信息，不可识别处标注：图片中该部分不清晰，无法准确识别。
2. 缺口路由：先尝试可用获取入口；失败时将 acquisition attempts 和缺失来源写入 `notes/source_map.md` 与 `notes/evidence_ledger.md`。主结论必需的缺口走 `integrator_action`；非核心或已降级/出范围的缺口走 `notes/continuation_map.md`。
3. 矛盾路由：记录 `contradicted`/`support_state`；教学综合只使用已限定、已修订、已降级或标为不确定的版本。
4. 不可完成时：生成 file-backed limitation asset，说明 intended route、缺失能力、已保留状态和最小下一步；稳定概念框架只能作为带标签的学习框架或限制说明进入交付。

## 2. 证据追踪

状态流：证据 -> 强度 -> 路由。

1. 证据门槛：核心教学要素（定义、分类、机制、阈值、公式、步骤、例外、风险、禁忌、适用条件）和关键事实（数字、剂量、日期、指南年份、法律后果、价格、版本号、推荐等级、诊断/处置建议）需要来源或明确稳定知识依据；引用和转述保留条件、例外和限定语。
2. 强度对齐：结论强度匹配证据粒度；材料只支持“可能/相关/某条件下”时正文同强度，依据保留在 `support_state` 或 Evidence Ledger。反例、边界、例外放在能影响判断的位置。
3. 弱证据路由：无证据支撑的强结论进入 `integrator_action`：`soften_claim`、`omit_claim`、`dispatch_agent` 或 `mark_unavailable`；缺口入正文写为“原始材料未提供，不能确定”或“需要进一步核验”。高风险细节入正文前需要具体来源；核心 claim 缺源先进 `integrator_action`；来源核验后降级的学习框架才可入正文；非核心扩展进 continuation candidate。

## 3. 推断标注追踪

状态流：陈述类型 -> 证据状态 -> 出口。

1. 来源事实进入 Evidence Ledger 或 Citation Audit；已接受证据不能用 `confidence: inferred` 承担最终事实。
2. 有机制、研究设计或来源明示支撑的推断，记录对应证据与支撑强度；只有共现、间接线索或上下文支持时，进入 `inferred`/待核验状态，并在正文标注推断边界和不确定度。
3. 类比、结构化重组和教学解释只承载理解功能；事实支撑回到 Evidence Ledger 或明确标注的推断条目。
4. 既无来源也无可追溯推断依据的内容，出口是问题、待核验点或学习提示，不沉淀为断言。

读者应能区分来源事实、教师重组、类比和推断；每条推断都能指回触发依据。

## 4. 知识模型追踪

状态流：锁定骨干 -> 证据挂接 -> 章节投影。

1. 每个主题先锁一条知识主干，再按主题选择骨架：概念（定义 -> 要素 -> 边界）、机制（基线 -> 扰动 -> 结果）、分类（目的 -> 标准 -> 分支）、流程（目标 -> 步骤 -> 失败模式）、公式（条件 -> 变量 -> 应用）、规则（目的 -> 要件 -> 例外 -> 后果）。
2. 只有事实列表时，补出最小因果链、分类依据或判断链再进入 Knowledge Model；复杂主题保留层级，简单主题保持紧凑，重复章节合并到能承载学习价值的章节。
3. Knowledge Model 的骨干和条目通过 `evidence_ids` 或 `core_spine_evidence_ids` 字段回链 Evidence Ledger；free-text EL id 不完成证据挂接。
4. `support_state: supported` 的模型条目必须带 `evidence_ids`；弱证据进入模型时需要 uncertainty 或 `integrator_action`。
5. 章节顺序服务骨干：先定位，再机制，再比较、记忆、易错或应用。

## 5. 教学深度追踪

状态流：用户意图 -> `teaching_use` -> 必备字段。

1. “为什么/机制/原理”进入 `core_explanation`：起点、关键前提、机制变化、结果、边界齐全；专业主题在这里说明为什么这样判断。
2. “怎么区分/对比”进入 `comparison`：决定性标准、相似原因、不同本质、一句话区分；误用后果和“看到什么就归哪类”的判别线索进入 `easy_error_repair`。
3. “怎么用/怎么判断”进入 `comparison` 或 `example`：输出可执行判断线索。
4. 抽象概念进入 `example` 和 `boundary`：至少一个准确例子或边界案例；新风险回到证据或边界说明后再使用。
5. `core_explanation` 缺机制链时补“从条件到结果”的推演；`comparison` 缺判别时补“看到什么就归哪类”；没有教学用途的段落不进任何 `teaching_use` 桶。

## 6. 记忆支持追踪

状态流：记忆意图 -> `memory_anchor` -> 复习出口。

1. 记忆、复习、考试、背诵或高频点请求进入 `memory_anchor`：核心锚点、检索线索、30 秒回顾齐全；重要细节按“为什么值得记”排序。
2. 记忆钩子先回链 `core_explanation` 或 `boundary`，再选择押韵、类比、口号或逻辑线。
3. 易混项进入 `easy_error_repair`：最短区分句或触发词。
4. 长文尾部生成 `quality_check` 形态的压缩层：核心表、判断链、速记段或回顾清单。
5. 只有讲解没有回忆入口时，补 `memory_anchor` 主干和 30 秒回顾。

## 7. 易错修复追踪

状态流：错点 -> `easy_error_repair` -> 边界/质量出口。

1. `easy_error_repair` 至少承载一个会改变判断的错点，按链路展开：错误说法/操作 -> 为什么容易混 -> 正确认识 -> 触发线索 -> 修正动作。
2. 触发线索落到可识别的具体特征；抽象的“注意区别”转成能改变判断的线索。
3. 高风险域（考试、临床、法律、金融、工程安全、网络安全等）追加 `boundary` 锚点，说明不能外推的范围。
4. 来源矛盾、图像不清、材料缺口走 `quality_check`，进入 `notes/evidence_ledger.md`、`notes/citation_audit.md` 或最终风险说明，不混入易错说理。

## 8. 长文容器追踪

状态流：容器文件 -> 章节计划 -> 最终交付。

1. 容器按 canonical files 落位：`manifest.yaml`、`index.md`、`final/final_merged.md`、`notes/process_trace.md`、`notes/research_brief.md`、`notes/research_tree.md`、`notes/source_map.md`、`notes/evidence_ledger.md`、`notes/knowledge_model.md`、`notes/chapter_plan.md`、`notes/integrator_decisions.md`、`notes/citation_audit.md`、`notes/continuation_map.md`，以及 `chapters/`。
2. `manifest.yaml` 投影章节，`index.md` 给阅读顺序和章节链接，`final/final_merged.md` 是可脱离聊天阅读的合并体。
3. `notes/chapter_plan.md` 每行携带 `purpose`、`required_anchors`、`completion_criteria`、`output_path`，并与 manifest chapters、index 链接和实际 chapter 文件对齐；学习价值重复的章节合并到同一行。
4. 来源、证据、推断、缺口、容器完整性和风险边界分别落到对应 notes 与 validation 记录；缺少容器文件时补文件，文件能力不可用时写明 intended file-backed route、缺失能力和最小下一步。
5. 最终聊天回复只报告路径、阅读顺序、验证状态和已知限制；正文归文件包。

## 9. 风险领域追踪

高风险领域：医学、法律、金融投资、工程安全、化学/生物安全、网络安全、心理健康、用药、急救、监管合规、儿童或弱势人群相关建议。

命中风险域的 claim 走状态流：识别风险 -> 评估 `support_state` -> 选择 `integrator_action` -> 落到交付位置。

判定要点：

1. 时效信息（指南、法规、标准、价格、版本、漏洞、政策等）缺当前来源时，`support_state` 为 `missing` 或 `partial`，`integrator_action` 选 `soften_claim`、`mark_unavailable` 或 `dispatch_agent`。
2. 个案条件不足时，`support_state` 为 `partial`，`integrator_action` 选 `revise`；正文改为“还需要哪些信息才能判断”。
3. 伤害相关的步骤、剂量、阈值、处置方案、规避规则等缺来源支持时，具体建议走 `omit_claim`；可保留部分改为学习框架、判断要素或待核验问题，并走 `revise` 或 `soften_claim`。
4. 专业场景提醒压成一句元信息，落到 `index.md`、delivery note 或限制说明；仅当用户明确要求学习安全流程或风险边界本身时扩为章节。

## 10. 最终质量追踪摘要

最终交付前确认：

1. 主结论的 `source_ids` 与 `locator_check` 可定位。
2. 每条主结论的 `support_state` 已记录；非 `supported` 的结论已经过 `integrator_action` 处理。
3. 知识主干覆盖用户显式学习意图：记忆、理解、比较、应用或易错修复。
4. 长文容器完整，或文件化交付受阻的限制说明清楚。
5. 最终回复只交代交付物、验证状态和限制。

高风险缺口走状态流：记录 `support_state` 和 `integrator_action` -> 对最终 claim 先用 `revise`、`soften_claim`、`dispatch_agent`、`omit_claim` 或 `mark_unavailable` 处理 -> 非核心扩展或已处理缺口写入 `notes/continuation_map.md`。`continuation_map` 不承接支撑主结论所必需的证据缺口，那部分仍由 `integrator_action` 处理。
