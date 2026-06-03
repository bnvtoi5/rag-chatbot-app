import os
import sys

# --- PHÒNG THỦ GIẢM TẢI RAM CHO MÁY 8GB (BẮT BUỘC ĐỂ TRÊN ĐẦU FILE) ---
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import operator
import re  # NÂNG CẤP: Thêm thư viện xử lý Regex để ép xuống dòng nguồn trích dẫn
import streamlit as st
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Import cấu hình và mạng lưới Agent từ thư mục src/
from src.config import Config
from src.agents.graph import agent_app

# Import trực tiếp hàm xử lý từ file run_ingest.py
from run_ingest import main as run_ingestion_process

# Tải biến môi trường và kiểm tra API Key
load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    st.error("LỖI: Chưa cấu hình GROQ_API_KEY trong file .env!")
    st.stop()

# Đảm bảo thư mục data đầu vào luôn tồn tại
if not os.path.exists(Config.RAW_DATA_DIR):
    os.makedirs(Config.RAW_DATA_DIR)

# --- CẤU HÌNH GIAO DIỆN STREAMLIT WEB UI ---
st.set_page_config(page_title="AI Multi-Agent RAG", page_icon="🤖", layout="wide")

# Khởi tạo trạng thái kiểm soát bộ nhớ trang (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False  # Trạng thái khóa ô chat khi AI đang chạy

# NÂNG CẤP: Khởi tạo bộ đếm key để tự động xóa/reset khung file uploader
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# --- THANH SIDEBAR: KÉO THẢ & CẤU HÌNH CHUNK SIZE ---
with st.sidebar:
    st.header("📂 Quản Lý Tài Liệu")
    
    # 1. Khung kéo thả file (Dùng thuộc tính key động để có thể tự động clear danh sách file)
    uploaded_files = st.file_uploader(
        "Kéo thả hoặc chọn file tài liệu của bạn:", 
        type=["txt", "pdf"], 
        accept_multiple_files=True,
        disabled=st.session_state.is_processing,
        key=f"file_uploader_{st.session_state.uploader_key}"
    )
    
    st.divider()
    
    # 2. Khu vực cấu hình thông số Băm nhỏ tài liệu (Chunking Configuration)
    st.subheader("⚙️ Cấu hình cấu trúc Vector")
    
    selected_chunk_size = st.slider(
        "Kích thước mảnh (Chunk Size):",
        min_value=200,
        max_value=2000,
        value=1200,
        step=100,
        help="Độ dài tối đa (số ký tự) của một mảnh văn bản khi băm nhỏ. Càng lớn ngữ cảnh càng sâu nhưng máy 8GB sẽ chạy nặng hơn."
    )
    
    selected_chunk_overlap = st.slider(
        "Độ trùng lặp (Chunk Overlap):",
        min_value=0,
        max_value=400,
        value=150,
        step=50,
        help="Số lượng ký tự được gối đầu trùng nhau giữa 2 mảnh liên tiếp để tránh mất ngữ cảnh ở ranh giới cắt."
    )
    
    if selected_chunk_overlap >= selected_chunk_size:
        st.warning("⚠️ Chú ý: Độ trùng lặp không nên lớn hơn hoặc bằng Kích thước mảnh!")
    
    st.divider()
    
    # 3. Nút bấm Xác nhận nạp dữ liệu
    if uploaded_files:
        st.info(f"Đang chờ xác nhận nạp {len(uploaded_files)} file...")
        
        if st.button("🚀 Xác Nhận Nạp Dữ Liệu", use_container_width=True, type="primary", disabled=selected_chunk_overlap >= selected_chunk_size):
            with st.spinner("Đang tiến hành trích xuất và nhúng dữ liệu vào ChromaDB..."):
                try:
                    # Ghi file tạm từ trình duyệt web vào thư mục data/ của dự án
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(Config.RAW_DATA_DIR, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    
                    # Gọi trực tiếp hàm xử lý và truyền tham số động từ UI xuống
                    is_success = run_ingestion_process(
                        chunk_size=selected_chunk_size, 
                        chunk_overlap=selected_chunk_overlap
                    )
                    
                    if is_success:
                        st.success(f"🎉 Thành công! Đã nạp dữ liệu với Chunk Size: {selected_chunk_size}, Overlap: {selected_chunk_overlap}")
                        
                        # NÂNG CẤP: Thay đổi uploader_key để ép Streamlit xóa sạch các file cũ khỏi khung chọn file!
                        st.session_state.uploader_key += 1
                        st.rerun() # Reload ngay lập tức để giao diện trống sạch sẽ
                    else:
                        st.error("❌ Không tìm thấy tài liệu hợp lệ hoặc có lỗi xảy ra trong quá trình đọc file.")
                        
                except Exception as e:
                    st.error(f"Lỗi hệ thống khi xử lý dữ liệu: {str(e)}")
    else:
        st.caption("Hãy tải file lên để kích hoạt nút xác nhận.")

    st.divider()
    st.caption("UI: Streamlit | Orchestration: LangGraph | Storage: ChromaDB Local | LLM: Llama 3.1")

# --- KHU VỰC HIỂN THỊ KHUNG CHAT CHÍNH ---
st.title("🤖 Trợ lý AI Doanh Nghiệp (Multi-Agent RAG)")
st.caption("Hệ thống phân tách tài nguyên và kiểm soát luồng xử lý thông minh")

# Hiển thị lịch sử các câu chat cũ ra màn hình (Đã tối ưu cấu trúc phân tách Expander và ép xuống dòng nguồn)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and "---" in msg["content"]:
            # Tách chuỗi cũ để vẽ lại đúng cấu trúc giao diện sạch
            parts = msg["content"].split("---", 1)
            st.markdown(parts[0].strip())
            with st.expander("🔍 Xem chi tiết trích dẫn dòng gốc"):
                source_content = parts[1].strip()
                # NÂNG CẤP: Quét và ép bẻ dòng tại các vị trí [1], [1-3], [1, 2]... giúp giao diện lịch sử không bị dính liền
                formatted_source = re.sub(r'(\[\d+[\-,\d]*\])', r'\n\n\1', source_content)
                st.markdown(formatted_source.strip())
        else:
            st.markdown(msg["content"])

# Khung nhập câu hỏi (Tự động khóa hoàn toàn ô nhập khi AI đang bận xử lý)
user_query = st.chat_input(
    "Nhập câu hỏi tra cứu tài liệu nội bộ...", 
    disabled=st.session_state.is_processing
)

# Luồng xử lý khi người dùng nhấn gửi câu hỏi
if user_query:
    st.session_state.is_processing = True
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.rerun()

# Chạy luồng xử lý gọi mạng lưới Agent sau khi giao diện đã được khóa an toàn
if st.session_state.is_processing and len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    current_query = st.session_state.messages[-1]["content"]

    with st.chat_message("assistant"):
        with st.spinner("Agents đang liên lạc qua hệ thống..."):
            result = agent_app.invoke({"messages": [{"role": "user", "content": current_query}]})
            
            if "final_answer" in result and result["final_answer"]:
                full_answer = result["final_answer"]
                
                # Kiểm tra ký tự phân tách nguồn từ Prompt mới để chia khối hiển thị
                if "---" in full_answer:
                    parts = full_answer.split("---", 1)
                    main_answer = parts[0].strip()
                    source_details = parts[1].strip()
                    
                    # 1. Hiển thị nội dung phản hồi chính
                    st.markdown(main_answer)
                    
                    # 2. Đóng gói phần nguồn dài dòng vào khối thu gọn và ép xuống dòng bằng Regex
                    with st.expander("🔍 Xem chi tiết trích dẫn dòng gốc"):
                        # NÂNG CẤP: Phát hiện các nhãn số trích dẫn để chèn hai dấu xuống dòng \n\n tạo khoảng cách thông thoáng
                        formatted_source_details = re.sub(r'(\[\d+[\-,\d]*\])', r'\n\n\1', source_details)
                        st.markdown(formatted_source_details.strip())
                else:
                    st.markdown(full_answer)
                
                # Lưu toàn bộ chuỗi thô (gồm cả dấu ---) vào session_state để render lại ở vòng lặp sau
                st.session_state.messages.append({"role": "assistant", "content": full_answer})
            else:
                llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=Config.GROQ_API_KEY, temperature=0.3)
                answer = llm.invoke(f"Phản hồi ngắn gọn câu chào hoặc câu xã giao này của người dùng: {current_query}").content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            
    st.session_state.is_processing = False
    st.rerun()