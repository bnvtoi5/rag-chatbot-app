import operator
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END

# Import trực tiếp các hàm xử lý từ 2 file độc lập vừa tạo ở trên
from src.agents.supervisor import supervisor_node
from src.agents.rag_agent import rag_node

# 1. Định nghĩa trạng thái hệ thống (State)
class AgentState(TypedDict):
    messages: Annotated[List[dict], operator.add]
    next_step: str
    context: str
    final_answer: str

# 2. Định nghĩa hàm Router để điều hướng phân nhánh
def router(state: AgentState):
    return state["next_step"]

# 3. Kết nối sơ đồ mạng lưới Agent (Graph)
workflow = StateGraph(AgentState)

# Đăng ký các Node chức năng
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("rag_agent", rag_node)

# Thiết lập luồng chạy dữ liệu giữa các Agent
workflow.set_entry_point("supervisor")
workflow.add_conditional_edges("supervisor", router, {"RAG": "rag_agent", "END": END})
workflow.add_edge("rag_agent", END)

# Đóng gói đồ thị ứng dụng
agent_app = workflow.compile()
