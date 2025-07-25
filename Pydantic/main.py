import gradio as gr
from agent import football_agent

async def user_send(message, history):
    result = await football_agent.run(message)
    reply = result.output
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ]
    return history, ""

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Football Bot", type="messages")
    msg = gr.Textbox(label="Nhập câu hỏi về cầu thủ / đội bóng")
    clear = gr.Button("Xóa hội thoại")

    msg.submit(user_send, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: ([], ""), None, [chatbot, msg])

demo.launch(share=True)
