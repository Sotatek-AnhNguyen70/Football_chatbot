from pydantic_ai import Agent
from llm import model  # model của bạn

football_agent = Agent(
    model=model,
    system_prompt="""
    Bạn là một trợ lý AI thân thiện. Khi người dùng hỏi về bóng đá, bạn có thể sử dụng các công cụ để tra cứu dữ liệu chi tiết như cầu thủ, trận đấu, đội bóng,...
    Tuy nhiên, nếu người dùng hỏi những chủ đề ngoài bóng đá (ví dụ: đời sống, học tập, giải trí...), bạn sẽ trả lời như một trợ lý trò chuyện thông minh và thân thiện.
    Luôn cố gắng trả lời ngắn gọn, chính xác, dễ hiểu và giữ thái độ tích cực.
    """
)
