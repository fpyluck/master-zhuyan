# MasterZhuyan — 全域学习助手技能
# MasterZhuyan — All-Domain Learning Assistant Skill

> 像强导师一样：先理解来源，建立可教模型，再交付高密度学习制品。

---

## What's New — 2026-05-30

- **Agent-first 架构**：`learning_artifacts.py` 和 `topic_research.py` 已移至 `scripts/legacy/`，不再作为主路由入口。
- 新增 `scripts/validate_deep_research_artifacts.py` — 验证深度研究制品的结构完整性。
- 新增 `references/agent-fabric.md` — agent 合约规范，定义 agent 工作的边界和交接协议。
- 新增 `references/process-tracing.md` — 多 agent 状态追踪和续接映射规范。
- 新增 `references/codex-execution.md` — 仓库、文件系统、代码导向的来源摄取规范。
- 新增 schemas：`citation_audit.schema.json`、`continuation_map.schema.json`、`research_tree.schema.json`。
- 新增测试：`tests/test_deep_research_artifacts.py`、`tests/test_legacy_learning_artifacts.py`、`tests/test_legacy_topic_research.py`、`tests/test_schema_contracts.py`，共 97 个测试。
- **质量动作边界**：Citation Audit 动作与 Quality Trace 动作正式分离，各自有独立的 schema 和验证路径。
- **减法发布通道**：移除了 chat-mode 门控，教学质量提升，指令负载降低。

---

## 是什么

MasterZhuyan 是一个 Claude Code / Codex 技能，提供全域学习支持：

**覆盖领域**：医学、自然科学、工程、法律、商业、人文、考试备考、语言学习、实用技能

**核心路由**：每个学习请求进入统一路由 — AgenticResearch + 文件支撑的长文制品。意图、主题规模、来源数量或表面简单性可以调整制品规模，但不创建备用研究模式或仅回答模式。

---

## 触发词

| 触发词 | 场景 |
|---|---|
| `【记忆】` `帮我记` `怎么记` | 记忆辅助、助记设计 |
| `【理解】` `讲懂` `解释` `为什么` | 概念理解、机制解释 |
| `系统整理` `知识点` `对比` | 知识体系化 |
| `复习` `易错点` `举一反三` | 考试备考 |
| `创建教案模板` `保存讲解风格` `某某式讲解` | 教案和风格管理 |
| 医学/科学/法律/商业/人文/考试/语言学习请求 | 领域学习 |

---

## 规范路由

AgenticResearch + file-backed longform

1. 设定学习者合约（目标、受众、深度、格式）
2. 维护动态研究树（research tree）
3. 派发制品生产 agent/sub-agent 作为常规执行织物
4. 将来源读入证据/引用追踪
5. 锁定知识模型
6. 综合持久化教学制品

执行脊柱：references/deep-research-execution.md
Agent 合约：references/agent-fabric.md

---

## 工作台结构

notes/
  chapter_plan.md
  source_map.md
  citation_audit.md
  research_tree.md
  process_trace.md
  continuation_map.md
  agent_outputs/
chapters/
  01_*.md
  02_*.md
final/
  final_merged.md

---

## 关键文件

### References
- references/deep-research-execution.md
- references/agent-fabric.md
- references/process-tracing.md
- references/codex-execution.md
- references/deep-research-output-contracts.md
- references/deep-research-quality-gates.md

### Schemas
- schemas/knowledge_model.schema.json
- schemas/evidence_card.schema.json
- schemas/source_map.schema.json
- schemas/citation_audit.schema.json
- schemas/research_tree.schema.json
- schemas/continuation_map.schema.json
- schemas/research_brief.schema.json
- schemas/quality_report.schema.json

### Scripts
- scripts/validate_deep_research_artifacts.py
- scripts/mz_longform.py
- scripts/prep_template.py
- scripts/smoke_test.py
- scripts/legacy/learning_artifacts.py
- scripts/legacy/topic_research.py

### Tests (97 total)
- tests/test_deep_research_artifacts.py
- tests/test_schema_contracts.py
- tests/test_mz_longform.py
- tests/test_prep_template.py
- tests/test_legacy_learning_artifacts.py
- tests/test_legacy_topic_research.py

---

## 安装

### Claude Code

claude skill install fpyluck/master-zhuyan

### Codex (OpenAI)

codex skill install fpyluck/master-zhuyan

安装后，在 Claude Code 或 Codex 中输入触发词即可激活。Codex 端通过 agents/openai.yaml 加载。

---

## 快速测试

python scripts/smoke_test.py
