# Enterprise Multi-Agent RAG System 🤖📦

Hệ thống Chatbot tra cứu tài liệu nội bộ doanh nghiệp ứng dụng kiến trúc Đa tác nhân (Multi-Agent Workflow) qua **LangGraph**, lưu trữ vector cục bộ bằng **ChromaDB**, và vận hành tối ưu trên phần cứng văn phòng (**RAM 8GB**).

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)

- **Frontend UI:** Streamlit (Python)
- **Orchestration:** LangGraph (Stateful Multi-Agent)
- **Storage:** ChromaDB (Local Vector Database)
- **LLM Backbone:** Llama 3.1 (Thông qua Groq API Cloud)
- **Text Embedding:** Mô hình nhúng đa ngôn ngữ cục bộ (`paraphrase-multilingual`)

---

## 📂 Cấu Trúc Thư Mục Dự Án (Project Structure)

```text
├── data/
│   ├── raw/             # Thư mục chứa file tài liệu mới tải lên (.txt, .pdf)
│   └── processed/       # Thư mục tự động lưu trữ file gốc sau khi nạp xong
├── chroma_db/           # Cơ sở dữ liệu Vector lưu trữ vật lý cục bộ
├── src/
│   ├── agents/          # Tầng logic tư duy và điều phối tác nhân AI
│   │   ├── supervisor.py     # Agent trưởng phòng phân tích Intent người dùng
│   │   ├── rag_agent.py      # Agent chuyên trách tra cứu tri thức tài liệu
│   │   ├── analyst_agent.py  # Agent phân tích dữ liệu chuyên sâu
│   │   └── graph.py          # Sơ đồ mạng lưới kết nối các Agent
│   ├── database/        # Tầng kết nối và cấu hình Vector DB
│   │   ├── chroma_client.py  # Khởi tạo kết nối ChromaDB nhận/xuất dữ liệu
│   │   └── embeddings.py     # Cấu hình mô hình nhúng số hóa văn bản
│   ├── ingestion/       # Tầng tiền xử lý dữ liệu đầu vào
│   │   ├── loaders.py        # Quét và đọc cấu trúc file .txt, .pdf
│   │   └── splitter.py       # Băm nhỏ văn bản & Thuật toán tính số dòng/trang
│   ├── prompts/         # Quản lý tập trung hệ thống Prompt (Tách biệt khỏi Code)
│   │   ├── supervisor_prompt.txt
│   │   └── rag_prompt.txt
│   └── config.py        # Quản lý tập trung các hằng số hệ thống
├── .env                 # Nơi cấu hình bảo mật API Key cá nhân
├── app.py               # Giao diện chính của ứng dụng (Streamlit Web UI)
├── run_ingest.py        # Script thực thi nạp/nhúng dữ liệu tự động ngầm
└── requirements.txt     # Danh sách các thư viện phần mềm bắt buộc cài đặt


🚀 Hướng Dẫn Cài Đặt & Khởi Chạy

1. Khởi tạo môi trường (Terminal)
Bash
# Tạo và kích hoạt môi trường ảo (.venv)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Nâng cấp pip & Cài đặt thư viện
pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir -v
2. Cấu hình Biến môi trường (.env)
Tạo file .env ngang hàng với app.py và điền Groq API Key:

Đoạn mã
GROQ_API_KEY=your_groq_api_key_here

3. Chạy ứng dụng
Bash
streamlit run app.py
📖 Hướng Dẫn Sử Dụng Khi Demo
Bước 1 (Nạp dữ liệu): Nhìn sang thanh Sidebar bên trái, kéo chỉnh Chunk Size và Chunk Overlap phù hợp (Ví dụ: 400 - 100 đối với giáo án/văn bản luật). Kéo thả file tài liệu vào khung và ấn 🚀 Xác Nhận Nạp Dữ Liệu. Hệ thống sẽ tự động băm nhỏ, nhúng vector vào ChromaDB và dọn dẹp giao diện sạch sẽ khi hoàn tất.

Bước 2 (Truy vấn): Nhập câu hỏi vào khung chat chính. Mạng lưới Agent sẽ tự động phân tích ý định để đưa ra câu trả lời kèm dán nhãn trích dẫn chính xác dòng/trang của tài liệu gốc.
```
