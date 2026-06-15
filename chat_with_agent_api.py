# 定义后台 API 的 URL
import json
import httpx

chat_with_agent_url = "http://127.0.0.1:6605/chat/agent_chat"
chat_url = "http://127.0.0.1:6605/chat/chat"


async def chat_with_agent(
    message: str,
    history: list,
    sys_prompt: str,
    history_len: int,
    temperature: float,
    max_tokens: int,
    stream: bool,
    session_id: str,
):
    """异步生成器：将用户消息发送到 FastAPI 后端，流式返回回答片段。

    Args:
        message: 用户输入的文本（纯字符串，不含文件）。
        history: OpenAI 格式的历史消息列表。
        sys_prompt: 系统提示语。
        history_len: 保留的历史消息数量。
        temperature: LLM 采样温度。
        max_tokens: 最大 token 数。
        stream: 是否启用流式输出。
        session_id: 会话标识。
    """
    # 构建请求数据（当前 UI 仅支持文本输入，不含文件）
    data = {
        "query": message,
        "sys_prompt": sys_prompt,
        "history_len": history_len,
        "history": [str(h) for h in history],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "session_id": session_id,
    }

    # 使用 httpx.AsyncClient 发送异步 POST 请求
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            async with client.stream("POST", chat_with_agent_url, data=data) as response:
                if response.status_code == 200:
                    chunks = ""
                    async for chunk in response.aiter_bytes():
                        if chunk:
                            try:
                                chunk_data = json.loads(chunk)
                                chunks += chunk_data.get("answer", "")
                                yield chunks
                            except json.JSONDecodeError:
                                # 忽略非 JSON 片段（如 HTTP 分块传输的空行）
                                continue
                else:
                    error_detail = ""
                    try:
                        body = await response.aread()
                        error_detail = body.decode("utf-8")
                    except Exception:
                        pass
                    yield f"请求失败 (HTTP {response.status_code}): {error_detail}"

        except httpx.RemoteProtocolError as e:
            # 后端在流式传输中提前关闭连接（通常是 LLM API key 无效或后端异常）
            yield f"后端响应中断：{e}"
        except httpx.ReadError as e:
            yield f"读取后端响应时出错：{e}"
        except httpx.TimeoutException:
            yield "请求超时，请检查后台服务器是否正常运行。"
        except httpx.ConnectError:
            yield "无法连接到后台服务器，请确认 app_server.py 已启动 (127.0.0.1:6605)。"
        except Exception as e:
            yield f"发生错误：{e}"
