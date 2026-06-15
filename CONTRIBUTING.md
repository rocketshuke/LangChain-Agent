# 🤝 贡献指南

感谢您考虑为 **LangChain Agent** 项目贡献代码！以下指南将帮助您快速上手。

---

## 📋 目录

- [行为准则](#行为准则)
- [如何报告问题](#如何报告问题)
- [提交 Pull Request](#提交-pull-request)
- [开发环境搭建](#开发环境搭建)
- [代码规范](#代码规范)
- [测试规范](#测试规范)
- [LangChain 最佳实践](#langchain-最佳实践)

---

## 行为准则

本项目采用友善、包容的协作氛围。请确保：
- 尊重每一位贡献者
- 接受建设性的批评
- 关注项目整体利益而非个人偏好

---

## 如何报告问题

1. **搜索已有 Issues** — 避免重复提交
2. **明确描述**：
   - 使用的 Python 版本、操作系统
   - 完整的错误堆栈（Traceback）
   - 最小复现步骤
   - 期望行为 vs 实际行为
3. **标签建议**：
   - `bug` — 缺陷报告
   - `enhancement` — 功能建议
   - `question` — 使用疑问

---

## 提交 Pull Request

### 流程

1. **Fork 本仓库**
2. **创建特性分支**：
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **进行修改**，并确保测试通过
4. **提交代码**：
   ```bash
   git commit -m "feat: 添加XX功能"  # 使用约定式提交
   ```
5. **推送到你的仓库**：
   ```bash
   git push origin feature/your-feature-name
   ```
6. **创建 Pull Request**，描述改动内容

### PR 检查清单

- [ ] 代码遵循 PEP 8 规范
- [ ] 新增功能有对应的测试覆盖
- [ ] 所有现有测试通过
- [ ] 更新了相关文档（README、API 文档等）
- [ ] 没有引入额外的未使用依赖
- [ ] 没有将 API Key 等敏感信息硬编码或提交

---

## 开发环境搭建

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/langchain-agent.git
cd langchain-agent

# 2. 创建 conda 环境
conda create -n langchain-agent-dev python=3.12
conda activate langchain-agent-dev

# 3. 安装开发依赖
pip install -r requirements.txt
pip install pytest pytest-asyncio

# 4. 配置 API 密钥
cp .env.example .env  # 或手动创建
# 编辑 .env 填入你的 API Key
```

---

## 代码规范

### Python 规范

- 遵循 **PEP 8** 编码风格
- 使用有意义的变量和函数命名（中文注释可保留）
- 函数需包含类型注解（Type Hints）
- 类和函数添加 docstring（中英文均可）
- 行长度建议不超过 100 字符

### 提交信息规范

使用 **[约定式提交 (Conventional Commits)](https://www.conventionalcommits.org/)**：

```
<type>: <简短描述>

<详细说明（可选）>
```

- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链

**示例：**
```
feat: 添加天气查询工具的温度单位选择功能
fix: 修复知识库搜索返回空结果时的异常处理
docs: 更新 API 文档中的请求示例
```

---

## 测试规范

- 使用 `pytest` 作为测试框架
- 测试文件命名：`test_*.py` 或 `*_test.py`
- 对每个新添加的工具或 API 端点编写测试
- 测试应可独立运行，不依赖外部 API（使用 mock）
- 运行测试前请确保虚拟环境已激活：

```bash
# 运行所有测试
pytest -v

# 运行烟雾测试
python test_smoke_upgrade.py
```

---

## LangChain 最佳实践

### Agent 开发

- 新工具请使用 `@tool` 装饰器（LangChain 推荐方式）或 `Tool` 类
- Tool 的 `description` 字段应详细、准确 —— LLM 通过它决定何时调用
- 工具函数的输入/输出签名应清晰明确

### 知识库（RAG）

- 新增文档加载器注册到 `knowledgebase_server/loader/loader.py`
- 文本分割参数 `chunk_size` 和 `chunk_overlap` 应根据文档类型调整
- 混合检索权重可根据业务场景调整（当前为 BM25:0.5 + FAISS:0.5）

### 依赖管理

- 核心 LangChain 包使用**精确版本号**固定（`==`），避免意外升级导致兼容性问题
- 其他依赖使用范围版本号（`>=`）
- 新增依赖前考虑是否可通过现有工具组合实现

### 导入规范

```
# ✅ 正确的导入方式
from langchain_core.tools import Tool
from langchain_deepseek import ChatDeepSeek
from langchain_classic.agents import create_react_agent

# ❌ 避免的旧导入（LangChain 1.x 中已废弃）
from langchain.llms import OpenAI       # 改用 langchain_openai
from langchain.chains import LLMChain   # 改用 LangGraph/Runnable
```

---

再次感谢您的贡献！ 🙌
