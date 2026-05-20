# =============================================================================
# Symphony WORKFLOW.md Demo
# 这是一个最小可运行的 Symphony 配置示例
# =============================================================================

tracker:
  kind: linear
  # 从 Linear 项目 URL 中获取 slug，例如: https://linear.app/your-team/project/my-project-abc123
  # 这里的 slug 就是 "my-project-abc123"
  project_slug: "test-2ec49a1e3082"
  # 哪些状态的 ticket 会被自动认领
  active_states:
    - Todo
    - In Progress
  # 哪些状态表示工作已结束
  terminal_states:
    - Done
    - Closed
    - Cancelled
    - Canceled
    - Duplicate

polling:
  # 每 30 秒轮询一次 Linear
  interval_ms: 30000

workspace:
  # 每个 ticket 的工作目录根路径
  root: ~/code/symphony-workspaces

hooks:
  # 新建工作区时执行：clone 你的代码仓库
  after_create: |
    git clone --depth 1 git@github.com:hahaha16/andrej-karpathy-skills.git
    # 如果有依赖需要安装，在这里执行
    # npm install
    # go mod download
    # pip install -r requirements.txt

  # 每次 agent 运行前执行：拉取最新代码
  before_run: |
    git fetch origin main
    git checkout main
    git pull origin main
    # 创建以 ticket ID 命名的分支
    git checkout -b "symphony/${SYMPHONY_ISSUE_IDENTIFIER:-work}" 2>/dev/null || git checkout "symphony/${SYMPHONY_ISSUE_IDENTIFIER:-work}"

agent:
  # 最多同时运行 3 个 agent（demo 建议小一点）
  max_concurrent_agents: 3
  # 单次 session 最多运行 10 个 turn
  max_turns: 10

codex:
  # Codex 启动命令
  command: codex app-server
  # 审批策略：never = 全自动，不需要人工确认
  # 生产环境建议使用 on-failure 或 on-request
  approval_policy: never
  # sandbox 模式：只允许写入工作区目录
  thread_sandbox: workspace-write
  # 单个 turn 超时：30 分钟
  turn_timeout_ms: 1800000
---

你正在处理一个 Linear 工单 `{{ issue.identifier }}`。

{% if attempt %}
## 续接上下文

这是第 {{ attempt }} 次重试，因为工单仍处于活跃状态。
请从当前工作区状态继续，不要从头开始。
{% endif %}

## 工单信息

- 标识符: {{ issue.identifier }}
- 标题: {{ issue.title }}
- 当前状态: {{ issue.state }}
- 标签: {{ issue.labels }}
- URL: {{ issue.url }}

## 描述

{% if issue.description %}
{{ issue.description }}
{% else %}
未提供描述。
{% endif %}

## 工作指令

1. 仔细阅读工单描述，理解需求。
2. 在代码仓库中实现所需的更改。
3. 编写或更新相关测试。
4. 确保所有测试通过。
5. 提交代码并创建 Pull Request。
6. 在 PR 描述中说明所做的更改。

## 约束

- 只在提供的仓库副本中工作，不要触碰其他路径。
- 不要修改与工单无关的代码。
- 如果遇到无法解决的阻塞问题，记录下来并停止。
- 最终输出只报告已完成的操作和遇到的阻塞。
