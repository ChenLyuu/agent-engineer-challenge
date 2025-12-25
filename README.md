# Agent Engineer Challenge

欢迎参加 Agent 工程师笔试。本项目使用现代化的 Python 工具链 `uv` 进行管理。

本项目旨在考察你构建 LLM 应用的核心工程能力，包括 **Prompt 攻防**、**API 鲁棒性设计** 以及 **复杂任务的工作流编排**。

我们推崇现代化的 Python 开发体验，本项目使用 **[uv](https://github.com/astral-sh/uv)** 进行依赖管理。

## 🛠️ 环境准备

### 1. 安装 uv
无需配置复杂的 virtualenv，请先安装 `uv`：

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 配置 API Key
本测试完全基于 **DeepSeek-V3** 模型。你需要准备 DeepSeek 官方 https://api.deepseek.com 的 API Key，或者任何兼容 OpenAI API 的模型。

请在终端设置环境变量：

```bash
# macOS / Linux
export DEEPSEEK_API_KEY="sk-your-api-key"
export DEEPSEEK_BASE_URL="https://api.deepseek.com"


# Windows (PowerShell)
$env:DEEPSEEK_API_KEY="sk-your-api-key"
$env:DEEPSEEK_BASE_URL="https://api.deepseek.com"
```

## 📝 题目列表

请进入 `challenges/` 目录，完成以下三个 Python 脚本中的 `# TODO` 部分。
利用 `uv` 的内联脚本特性，你可以直接运行它们，依赖会自动安装。

### 1️⃣ 任务一：结构化提取与防御 (`01_extraction.py`)
*   **目标**：编写 System Prompt，从杂乱的用户输入中提取标准 JSON。
*   **考察点**：JSON 格式控制、Prompt Injection 防御（防止用户套话）。
*   **运行命令**：
    ```bash
    uv run challenges/01_extraction.py
    ```

### 2️⃣ 任务二：长文生成工作流 (`02_workflow.py`)
*   **目标**：设计一个 Agent，通过“大纲规划 -> 循环撰写 -> 上下文传递”的流程生成万字长文。
*   **考察点**：Context Window 管理（如何避免 Token 溢出）、状态流转、DeepSeek 模型控制。
*   **运行命令**：
    ```bash
    uv run challenges/02_workflow.py
    ```

---

## 📦 提交要求 (Definition of Done)

请严格按照以下标准提交，**缺一不可**：

### 1. 代码提交
*   Fork 本仓库，将修改后的代码推送到你的 GitHub 仓库。
*   或者将项目打包为 ZIP 发送。

### 2. 飞书文档 (Feishu Doc) 📄
请提供一个飞书文档链接（开启“任何人可阅读”权限），文档需包含：
*   **思路解析**：针对每个任务，解释你为什么这么写 Prompt？你是如何处理 Context 限制的？
*   **Bad Case 复盘**：在调试过程中，DeepSeek 模型出现过什么幻觉或错误？你是如何修正的？

### 3. 运行结果截图 📸
请在飞书文档中附带以下截图，证明代码可运行：
*   **任务一**：成功提取 JSON 的终端输出截图，以及**成功拦截注入攻击**的截图。
*   **任务二**：完整生成文章的日志流截图，以及最终生成的 Markdown 文件预览。

---

祝你好运！期待看到你的 Agent 作品。