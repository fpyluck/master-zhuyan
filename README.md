# MasterZhuyan — 全领域学习技能

> Claude Code × Codex 双端学习助教 — 机制优先、知识密度高、记忆友好。

---

## 一句话定位

`MasterZhuyan` 接管所有学习请求：供入笔记、截图、文档、概念、习题或标准学习触发词，默认走 **deep-research + longform** 合并路由：研究建模层完成溯源和概念结构，longform 层输出 manifest、章节、校验、最终合并。

触发词：`【记忆】`、`【理解】`、`帮我记`、`怎么记`、`讲懂`、`解释`、`系统整理`、`复习`等，覆盖医学、理工、法律、商业、人文、考试、语言学习及实操技能。

| 端 | 路径 |
|---|---|
| Claude Code | `claude/skills/master-zhuyan/` |
| Codex | `codex/skills/master-zhuyan/` |

---

## What's New — 2026-05-27

首次发布。Claude × Codex 双端双边结构。

---

## 安装

**Bash / macOS / Linux (Claude Code)**

```bash
mkdir -p ~/.claude/skills/master-zhuyan
curl -sL https://raw.githubusercontent.com/fpyluck/master-zhuyan/main/claude/skills/master-zhuyan/SKILL.md \
  > ~/.claude/skills/master-zhuyan/SKILL.md
```

**Codex (Windows PowerShell)**

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills\master-zhuyan" | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/fpyluck/master-zhuyan/main/codex/skills/master-zhuyan/SKILL.md" `
  -OutFile "$env:USERPROFILE\.codex\skills\master-zhuyan\SKILL.md"
```
