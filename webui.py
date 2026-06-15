# webui.py
import uuid
import gradio as gr
from webui.chat_with_agent_api import chat_with_agent
from webui.knowledgebase_api import create_kb, delete_kb, upload_docs, list_kbs, update


def generate_session_id():
    return str(uuid.uuid4())


def on_app_load():
    return generate_session_id()


# 将 Gradio 默认的历史格式（列表的列表）转换为 OpenAI 消息列表
def convert_history_to_messages(history):
    """history: [[user, assistant], ...] 格式 -> [{"role": "user", "content": ...}, {"role": "assistant", "content": ...}]"""
    messages = []
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        if bot_msg is not None:
            messages.append({"role": "assistant", "content": bot_msg})
    return messages


# 将 OpenAI 消息列表转换为 Gradio 默认历史格式（用于更新界面）
def convert_messages_to_history(messages):
    history = []
    for i in range(0, len(messages), 2):
        if i + 1 < len(messages):
            history.append([messages[i]["content"], messages[i + 1]["content"]])
        else:
            history.append([messages[i]["content"], None])
    return history


# 异步生成器：逐块返回回答，供 Gradio 流式显示
async def respond(message, history, sys_prompt, history_len, temperature, max_tokens, stream, session_state):
    # 将 Gradio 默认格式的 history 转换为 OpenAI 消息格式
    messages_history = convert_history_to_messages(history)
    full_response = ""
    # 消费异步生成器
    async for chunk in chat_with_agent(
        message, messages_history, sys_prompt, history_len,
        temperature, max_tokens, stream, session_state
    ):
        full_response += chunk
        yield full_response  # 每次返回当前累积的完整回复，Gradio 会更新 chatbot


# 异步生成器：处理发送消息并流式更新聊天记录
async def send_message(message, history, *args):
    if not message:
        yield history, ""
        return
    # 先添加用户消息（临时显示），然后流式填充 assistant 回复
    history.append([message, None])  # assistant 回复暂时为 None
    # 累积生成器返回的回复片段
    full_reply = ""
    async for reply_chunk in respond(message, history[:-1], *args):  # 传入去掉最后一条（用户消息）的历史，避免重复
        # 更新 history 中最后一条的 assistant 内容
        history[-1][1] = reply_chunk
        full_reply = reply_chunk
        yield history, ""  # 每次 yield 刷新界面，并清空输入框
    # 最终确保输入框清空
    yield history, ""


with gr.Blocks(fill_width=True, fill_height=True) as demo:
    session_state = gr.State(value=on_app_load)

    with gr.Tab("🤖 聊天机器人"):
        gr.Markdown("## 🤖 聊天机器人")
        with gr.Row():
            with gr.Column(scale=1, variant="panel"):
                sys_prompt = gr.Textbox(label="系统提示语",
                                        value="You are a helpful assistant. Answer questions in chinese !")
                history_len = gr.Slider(minimum=-1, maximum=10, value=-1, label="保留历史消息的数量")
                temperature = gr.Slider(minimum=0.01, maximum=2.0, value=0.5, step=0.01, label="temperature")
                max_tokens = gr.Slider(minimum=64, maximum=1024, value=512, step=8, label="max_length")
                stream = gr.Checkbox(label="stream", value=True)
            with gr.Column(scale=10):
                chatbot = gr.Chatbot(height=600)  # 没有 type 参数，使用默认格式
                msg = gr.Textbox(label="输入消息", lines=2, placeholder="在这里输入...")
                with gr.Row():
                    send_btn = gr.Button("发送", variant="primary")
                    clear_btn = gr.Button("清空对话")

        # 绑定事件，注意 send_message 是异步生成器
        send_btn.click(
            send_message,
            [msg, chatbot, sys_prompt, history_len, temperature, max_tokens, stream, session_state],
            [chatbot, msg]
        )
        msg.submit(
            send_message,
            [msg, chatbot, sys_prompt, history_len, temperature, max_tokens, stream, session_state],
            [chatbot, msg]
        )
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg])

    # 知识库管理部分（保持不变，略）
    with gr.Tab("知识库管理"):
        gr.Markdown("## 📚 知识库管理")
        with gr.Row():
            kb_name = gr.Textbox(label="知识库名称", placeholder="请输入知识库名称")
        with gr.Row():
            kb_info = gr.Textbox(label="知识库描述", placeholder="请输入知识库描述")
        with gr.Row():
            message_box = gr.Markdown(visible=False)
        with gr.Row():
            create_button = gr.Button("创建知识库")
            delete_button = gr.Button("删除知识库")
        kbs = list_kbs()['choices']
        with gr.Row():
            kb_name_upload = gr.Dropdown(label="选择知识库", choices=kbs)
        with gr.Row():
            file_uploaded = gr.Files(label="已选择的文件", visible=False)
        with gr.Row():
            file_upload = gr.Files(label="选择文件")
        with gr.Row():
            chunk_size = gr.Number(label="知识库中单段文本最大长度(chunk_size)", value=128, minimum=1, maximum=800)
            chunk_overlap = gr.Number(label="知识库中相邻文本重合长度(chunk_overlap)", value=20, minimum=0, maximum=400)
        with gr.Row():
            upload_button = gr.Button("上传并向量化")
        with gr.Row():
            upload_message_box = gr.Markdown(visible=False)

        create_button.click(create_kb, [kb_name, kb_info], [message_box, kb_name, kb_info]).then(fn=list_kbs,
                                                                                                 outputs=kb_name_upload)
        delete_button.click(delete_kb, [kb_name_upload], [message_box, kb_name]).then(fn=list_kbs,
                                                                                      outputs=kb_name_upload)
        file_upload.upload(fn=update, inputs=[file_upload], outputs=[file_uploaded, file_upload])
        upload_button.click(upload_docs, [kb_name_upload, file_uploaded, chunk_size, chunk_overlap],
                            [upload_message_box, file_uploaded])

demo.launch()