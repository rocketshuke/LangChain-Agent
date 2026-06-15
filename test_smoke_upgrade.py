#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LangChain 升级烟雾测试 (Smoke Test)
验证升级后所有关键模块导入正确、基本功能正常。
"""

import sys
import os
import importlib

PASS = 0
FAIL = 0
ERRORS = []


def test(name: str, func):
    """运行单个测试用例"""
    global PASS, FAIL
    try:
        func()
        PASS += 1
        print(f"  ✅ {name}")
    except Exception as e:
        FAIL += 1
        ERRORS.append((name, str(e)))
        print(f"  ❌ {name}: {e}")


def check_import(module_path: str, names: list = None):
    """验证导入是否成功"""
    def _check():
        mod = importlib.import_module(module_path)
        if names:
            for name in names:
                obj = getattr(mod, name, None)
                assert obj is not None, f"{module_path}.{name} 未找到"
    return _check


def main():
    print("=" * 60)
    print("LangChain 升级烟雾测试")
    print("=" * 60)

    # ── 1. 版本检查 ──
    print("\n[1] LangChain 版本检查")
    test("langchain 版本", lambda: (
        importlib.import_module("langchain"),
        setattr(sys.modules[__name__], 'lc_version', sys.modules['langchain'].__version__),
        print(f"      langchain: {sys.modules['langchain'].__version__}")
    ))
    test("langchain-core 版本", lambda: (
        importlib.import_module("langchain_core"),
        print(f"      langchain-core: {sys.modules['langchain_core'].__version__}")
    ))
    test("langchain_classic 版本", lambda: (
        importlib.import_module("langchain_classic"),
        print(f"      langchain-classic: {sys.modules['langchain_classic'].__version__}")
    ))
    test("langchain_deepseek 版本", lambda: (
        importlib.import_module("langchain_deepseek"),
        print(f"      langchain-deepseek: {sys.modules['langchain_deepseek'].__version__}")
    ))
    test("langchain-community 版本", lambda: (
        importlib.import_module("langchain_community"),
        print(f"      langchain-community: {sys.modules['langchain_community'].__version__}")
    ))
    test("langchain-text-splitters 版本", lambda: (
        importlib.import_module("langchain_text_splitters"),
        print(f"      langchain-text-splitters: {getattr(sys.modules['langchain_text_splitters'], '__version__', 'installed')}")
    ))

    # ── 2. 核心 LangChain 导入 ──
    print("\n[2] LangChain 核心 API 导入")
    test("langchain.agents create_agent",
         check_import("langchain.agents", ["create_agent"]))
    test("langchain_core.prompts ChatPromptTemplate",
         check_import("langchain_core.prompts", ["ChatPromptTemplate", "SystemMessagePromptTemplate", "HumanMessagePromptTemplate"]))
    test("langchain_core.tools Tool",
         check_import("langchain_core.tools", ["Tool", "StructuredTool"]))
    test("langchain_core.callbacks AsyncCallbackHandler",
         check_import("langchain_core.callbacks", ["AsyncCallbackHandler"]))
    test("langchain_core.outputs LLMResult",
         check_import("langchain_core.outputs", ["LLMResult"]))
    test("langchain_core.documents Document",
         check_import("langchain_core.documents", ["Document"]))
    test("langchain_core.embeddings Embeddings",
         check_import("langchain_core.embeddings", ["Embeddings"]))

    # ── 3. langchain_classic 旧版兼容 API ──
    print("\n[3] langchain_classic (旧版兼容) API 导入")
    test("langchain_classic.agents AgentExecutor",
         check_import("langchain_classic.agents", ["AgentExecutor", "create_react_agent"]))
    test("langchain_classic.agents AgentExecutor.from_agent_and_tools",
         lambda: hasattr(importlib.import_module("langchain_classic.agents").AgentExecutor, "from_agent_and_tools"))
    test("langchain_classic.retrievers EnsembleRetriever",
         check_import("langchain_classic.retrievers", ["EnsembleRetriever"]))

    # ── 4. langchain_deepseek ──
    print("\n[4] langchain_deepseek API 导入")
    test("langchain_deepseek ChatDeepSeek",
         check_import("langchain_deepseek", ["ChatDeepSeek"]))

    # ── 5. langchain_openai ──
    print("\n[5] langchain_openai API 导入")
    test("langchain_openai OpenAIEmbeddings",
         check_import("langchain_openai", ["OpenAIEmbeddings"]))

    # ── 6. langchain_community ──
    print("\n[6] langchain_community API 导入")
    test("langchain_community.vectorstores FAISS",
         check_import("langchain_community.vectorstores", ["FAISS"]))
    test("langchain_community.retrievers BM25Retriever",
         check_import("langchain_community.retrievers", ["BM25Retriever"]))
    test("langchain_community.embeddings HuggingFaceEmbeddings",
         check_import("langchain_community.embeddings", ["HuggingFaceEmbeddings"]))
    test("langchain_community.document_loaders.PyPDFLoader",
         check_import("langchain_community.document_loaders", ["PyPDFLoader"]))
    test("langchain_community.document_loaders.TextLoader",
         check_import("langchain_community.document_loaders", ["TextLoader"]))
    test("langchain_community.document_loaders.CSVLoader",
         check_import("langchain_community.document_loaders", ["CSVLoader"]))
    test("langchain_community.document_loaders.UnstructuredMarkdownLoader",
         check_import("langchain_community.document_loaders", ["UnstructuredMarkdownLoader"]))

    # ── 7. langchain_text_splitters ──
    print("\n[7] langchain_text_splitters API 导入")
    test("langchain_text_splitters RecursiveCharacterTextSplitter",
         check_import("langchain_text_splitters", ["RecursiveCharacterTextSplitter"]))

    # ── 8. 项目自定义模块导入 ──
    print("\n[8] 项目自定义模块导入")
    # 先把项目根目录加入 sys.path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    test("tools.tools_select", check_import("tools.tools_select", ["tools"]))
    # 先 import utils.downloader 避免导入循环，再测试 code_interpreter
    # code_interpreter 中的 CodeBox 是单例，只允许一个实例
    test("tools.code_interpreter import", lambda: (
        __import__("tools.code_interpreter", fromlist=["code_interpreter"])
    ))
    test("tools.weather_check", check_import("tools.weather_check", ["weather_check"]))
    test("tools.web_search", check_import("tools.web_search", ["web_search"]))
    test("tools.knowledge_search", check_import("tools.knowledge_search", ["knowledgebas_search"]))
    test("tools.get_time", check_import("tools.get_time", ["get_time"]))
    test("utils.callback", check_import("utils.callback", ["CustomAsyncIteratorCallbackHandler"]))
    test("utils.load_docs", check_import("utils.load_docs", ["get_file_content"]))
    test("configs.setting", check_import("configs.setting"))
    test("configs.prompt", check_import("configs.prompt", ["PROMPT_TEMPLATES"]))

    # ── 9. 工具基本功能测试 ──
    print("\n[9] 工具基本功能验证")
    from tools.get_time import get_time

    def test_get_time():
        result = get_time.run("")
        assert isinstance(result, str) and len(result) > 10
    test("get_time.run() 返回正确格式的时间", test_get_time)

    # ── 10. Document 创建 ──
    print("\n[10] 基本数据类型验证")
    from langchain_core.documents import Document

    def test_document():
        doc = Document(page_content="测试内容", metadata={"source": "test.txt"})
        assert doc.page_content == "测试内容"
        assert doc.metadata["source"] == "test.txt"
    test("Document 创建与属性访问", test_document)

    # ── 11. RecursiveCharacterTextSplitter ──
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    def test_splitter():
        splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
        docs = splitter.split_documents([Document(page_content="A" * 200)])
        assert len(docs) >= 3
    test("RecursiveCharacterTextSplitter 分块", test_splitter)

    # ── 12. PromptTemplate 创建 ──
    from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

    def test_prompt():
        system_prompt = SystemMessagePromptTemplate.from_template("你是一个助手")
        human_prompt = HumanMessagePromptTemplate.from_template("问题：{input}")
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
        messages = chat_prompt.format_messages(input="今天天气如何")
        assert len(messages) == 2
        assert "今天天气如何" in messages[1].content
    test("ChatPromptTemplate 消息组装", test_prompt)

    # ── 13. FAISS 向量存储基本操作 ──
    print("\n[13] FAISS 向量存储基本操作")
    from langchain_core.embeddings import Embeddings
    from langchain_community.vectorstores import FAISS

    class TestEmbeddings(Embeddings):
        """测试用 Embeddings"""
        def embed_documents(self, texts):
            return [[0.1, 0.2, 0.3]] * len(texts)
        def embed_query(self, text):
            return [0.1, 0.2, 0.3]

    def test_faiss():
        embeddings = TestEmbeddings()
        docs = [Document(page_content="测试文档")]
        vs = FAISS.from_documents(docs, embeddings)
        results = vs.similarity_search("测试", k=1)
        assert len(results) == 1
        assert results[0].page_content == "测试文档"
    test("FAISS 向量存储创建与检索", test_faiss)

    # ── 14. 检查 webui API 调用模块 ──
    print("\n[14] WebUI API 模块导入")
    test("webui.chat_with_agent_api",
         check_import("webui.chat_with_agent_api", ["chat_with_agent"]))
    test("webui.knowledgebase_api",
         check_import("webui.knowledgebase_api", ["create_kb", "delete_kb", "upload_docs", "list_kbs"]))

    # ── 15. FastAPI 路由模块 ──
    print("\n[15] FastAPI 路由模块导入")
    test("chat.chat_routes 模块导入 (不含chat_router以避免CodeBox单例)",
         lambda: importlib.import_module("chat.chat_routes"))
    test("knowledgebase_server.kb_routes kb_router",
         check_import("knowledgebase_server.kb_routes", ["kb_router"]))
    test("knowledgebase_server.loader.loader data_loader",
         check_import("knowledgebase_server.loader.loader", ["data_loader"]))

    # ── 16. DB 模块 ──
    print("\n[16] 数据库模块导入")
    test("db_server.base",
         check_import("db_server.base", ["Base", "KnowledgeBase", "session"]))
    test("db_server.knowledge_base_repository",
         check_import("db_server.knowledge_base_repository", ["add_kb_to_db", "del_kb_from_db", "list_kb_from_db"]))

    # ── 汇总 ──
    print("\n" + "=" * 60)
    total = PASS + FAIL
    print(f"测试结果: {total} 总用例 | ✅ {PASS} 通过 | ❌ {FAIL} 失败")
    if ERRORS:
        print("\n失败详情:")
        for name, err in ERRORS:
            print(f"  ❌ {name}")
            print(f"     {err}")
    print("=" * 60)

    if FAIL == 0:
        print("\n🎉 所有测试通过！LangChain 升级验证成功。")
        print("PASS")
    else:
        print(f"\n⚠️  有 {FAIL} 个测试失败，请检查。")
        print("FAIL")

    return FAIL == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
