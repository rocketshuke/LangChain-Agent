# 🤖 LangChain Agent — 智能代理系统

> **基于 LangChain 1.3.9 构建的智能代理系统**，集成了 DeepSeek 大语言模型、多工具调用、知识库管理（RAG）以及 Web 可视化界面。

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-1.3.9-green)](https://pypi.org/project/langchain/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 目录

- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [快速开始](#-快速开始)
- [配置说明](#-配置说明)
- [使用示例](#-使用示例)
- [API 文档](#-api-文档)
- [项目结构](#-项目结构)
- [升级说明](#-升级说明)
- [运行测试](#-运行测试)
- [如何贡献](#-如何贡献)
- [许可证](#-许可证)

---

## ✨ 功能特性

- **🧠 智能对话代理** — 基于 DeepSeek 大模型 + ReAct 推理框架，通过 LangChain Agent 自主决策调用工具
- **🔧 多功能工具箱** — 集成 5 个内置工具：
  - 🌤️ **天气查询** — 查询全球城市实时天气
  - 🔍 **网络搜索** — 通过 SerpAPI 获取最新资讯
  - 📚 **知识库搜索** — 从本地 FAISS 向量库检索相关内容（RAG）
  - ⏰ **当前时间** — 获取服务器当前时间
  - 💻 **代码解释器** — 在沙箱中执行 Python 代码并返回结果
- **📁 知识库管理** — 支持上传多种格式文档（TXT/PDF/CSV/MD/DOCX 等）、自动分块向量化、FAISS 存储、混合检索（稠密 + BM25 稀疏）
- **🌐 双界面支持**：
  - **FastAPI Web API** — RESTful 接口，支持流式 SSE 输出
  - **Gradio Web UI** — 用户友好的图形化聊天界面
- **📎 文件对话** — 上传文档作为上下文与 AI 对话
- **📜 历史对话** — 可配置保留轮次的历史消息

---

## 🛠 技术栈

| 类别 | 技术 |
|------|------|
| **AI 框架** | LangChain 1.3.9, LangGraph 1.2.5 |
| **大语言模型** | DeepSeek Chat (通过 langchain-deepseek) |
| **向量存储** | FAISS (faiss-cpu) |
| **嵌入模型** | BGE-large-zh-v1.5 / SiliconFlow API |
| **检索策略** | 混合检索 (稠密向量 + BM25 稀疏), EnsembleRetriever |
| **API 服务** | FastAPI, Uvicorn |
| **Web UI** | Gradio 6.x |
| **数据库** | SQLite + SQLAlchemy 2.0 |
| **文档处理** | PyMuPDF (PDF), python-docx (DOCX), pypdf, Unstructured |
| **代码沙箱** | CodeBox (LocalBox) |
| **分词** | jieba (中文分词 for BM25) |

---

## 🚀 快速开始

### 前置要求

- Python >= 3.10
- pip / conda
- （可选）Docker — 用于 CodeBox 代码解释器沙箱

### 1️⃣ 克隆项目

```bash
git clone https://github.com/yourusername/langchain-agent.git
cd langchain-agent
```

### 2️⃣ 创建虚拟环境

```bash
# 使用 conda（推荐）
conda create -n langchain-agent python=3.12
conda activate langchain-agent

# 或使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 4️⃣ 配置环境变量

```bash
# 复制 .env 文件或手动创建
# 编辑 .env 填入你的 API Key
```

编辑 `.env` 文件：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

> **获取 API Key：**
> - DeepSeek: [https://platform.deepseek.com](https://platform.deepseek.com)
> - SerpAPI（网络搜索）: [https://serpapi.com](https://serpapi.com)
> - 心知天气（天气查询）: [https://www.seniverse.com](https://www.seniverse.com)
> - SiliconFlow（嵌入模型）: [https://siliconflow.cn](https://siliconflow.cn) （可选）

### 5️⃣ 启动服务

```bash
# 启动 FastAPI 后端服务（端口 6605）
python app_server.py
```

服务启动后，API 文档自动可用：
- Swagger UI: http://localhost:6605/docs
- ReDoc: http://localhost:6605/redoc

### 6️⃣ 启动 Web UI（可选）

在另一个终端中：

```bash
# 确保后端已启动，然后运行 Gradio UI
python webui.py
```

Gradio UI 将启动在 http://localhost:7860

---

## 🔧 配置说明

项目通过 `configs/setting.py` 和 `.env` 文件进行配置：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | - |
| `DEEPSEEK_BASE_URL` | API 端点 | `https://api.deepseek.com` |
| `chat_model_name` | 对话模型名称 | `deepseek-chat` |
| `embedding_model_path` | 本地嵌入模型路径 | `./models/.../bge-large-zh-v1___5` |
| `KB_DIR` | 知识库存储目录 | `./knowledgebases` |
| `SQLALCHEMY_DATABASE_URI` | 数据库连接 URI | `sqlite:///./db_server/data/info.db` |
| `TIME_OUT` | API 超时时间(秒) | `60` |
| `MEDIA_DIR` | 媒体文件目录 | `./temp/medias` |

---

## 📖 使用示例

### API 请求示例

**对话请求：**

```bash
curl -X POST http://localhost:6605/chat/agent_chat \
  -F "query=今天北京的天气怎么样？" \
  -F "sys_prompt=You are a helpful assistant." \
  -F "temperature=0.5" \
  -F "max_tokens=1024"
```

**创建知识库：**

```bash
curl -X POST http://localhost:6605/knowledgebase/create_kb \
  -H "Content-Type: application/json" \
  -d '{"kb_name": "my_knowledge", "kb_info": "我的知识库"}'
```

**上传文档到知识库：**

```bash
curl -X POST http://localhost:6605/knowledgebase/upload_docs \
  -F "kb_name=my_knowledge" \
  -F "files=@/path/to/document.pdf" \
  -F "chunk_size=128" \
  -F "chunk_overlap=20"
```

**搜索知识库：**

```bash
curl -X POST http://localhost:6605/knowledgebase/search_kb \
  -H "Content-Type: application/json" \
  -d '{"kb_name": "my_knowledge", "query": "搜索关键词"}'
```

---

## 📘 API 文档

### 聊天模块 (`/chat`)

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/chat/agent_chat` | Agent 对话（流式响应） |

### 知识库模块 (`/knowledgebase`)

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/knowledgebase/create_kb` | 创建知识库 |
| DELETE | `/knowledgebase/delete_kb` | 删除知识库 |
| GET | `/knowledgebase/list_kbs` | 列出所有知识库 |
| POST | `/knowledgebase/upload_docs` | 上传文档并向量化 |
| POST | `/knowledgebase/delete_docs` | 删除知识库中的文档 |
| POST | `/knowledgebase/search_kb` | 搜索知识库 |

---

## 📁 项目结构

```
langchain-agent/
├── app_server.py                 # FastAPI 应用入口
├── webui.py                      # Gradio Web UI 入口
├── chat/
│   └── chat_routes.py            # 对话 API 路由（Agent 调用逻辑）
├── knowledgebase_server/
│   ├── kb_routes.py              # 知识库管理 API 路由
│   ├── kb_routes_local.py        # 知识库管理（本地模型版本）
│   ├── loader/
│   │   └── loader.py             # 文档加载器工厂
│   └── splitter/
│       └── splitter.py           # 文本分割器（预留）
├── tools/
│   ├── tools_select.py           # 工具注册中心
│   ├── weather_check.py          # 天气查询工具
│   ├── web_search.py             # 网络搜索工具
│   ├── knowledge_search.py       # 知识库搜索工具
│   ├── code_interpreter.py       # Python 代码解释器
│   └── get_time.py               # 时间查询工具
├── utils/
│   ├── callback.py               # 自定义流式回调处理器
│   ├── load_docs.py              # 文档内容读取工具
│   └── downloader.py             # 文件下载工具
├── configs/
│   ├── setting.py                # 全局配置
│   └── prompt.py                 # 提示词模板
├── db_server/
│   ├── base.py                   # SQLAlchemy 数据库模型
│   └── knowledge_base_repository.py  # 知识库 CRUD 操作
├── webui/
│   ├── chat_with_agent_api.py    # Gradio 聊天 API 封装
│   └── knowledgebase_api.py      # Gradio 知识库 API 封装
├── knowledgebases/               # FAISS 知识库存储目录
├── data/                         # 上传文件存储目录
├── temp/                         # 临时文件/媒体目录
├── requirements.txt              # 项目依赖
├── setup.py                      # Python 包配置
├── pyproject.toml                # Python 项目元数据
├── test_smoke_upgrade.py         # 烟雾测试脚本
└── .env                          # 环境变量（API Key 等）
```

---

## 📦 升级说明

本项目已升级至 **LangChain 1.3.9**（截至 2026-06-15 的最新稳定版本），同时升级了所有相关包：

| 包名 | 版本 |
|------|------|
| langchain | **1.3.9** |
| langchain-core | **1.4.7** |
| langchain-classic | **1.0.8** |
| langchain-community | **0.4.2** |
| langchain-deepseek | **1.1.0** |
| langchain-openai | **1.3.2** |
| langchain-text-splitters | **1.1.2** |

> 注意：LangChain 1.x 要求 **Python >= 3.10**。升级过程中使用了 `langchain-classic` 包保留旧版 ReAct Agent (`create_react_agent` + `AgentExecutor`) 的兼容性。
>
> 详细迁移信息请参阅 [LANGCHAIN_UPGRADE_REPORT.md](LANGCHAIN_UPGRADE_REPORT.md)。

---

## 🧪 运行测试

```bash
# 运行烟雾测试（验证升级后所有模块导入和基本功能正常）
conda activate RAG
python test_smoke_upgrade.py
```

测试覆盖：版本检查、核心 API 导入、项目模块导入、FAISS 向量存储、文本分割、提示词模板组装等 48 个用例。

---

## 🤝 如何贡献

👋 欢迎贡献代码、报告问题或提出新功能建议！

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的贡献指南。

---

## 📄 许可证

本项目采用 MIT 许可证 — 详见 [LICENSE](LICENSE) 文件。
