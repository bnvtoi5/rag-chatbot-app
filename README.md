# -_- coding: utf-8 -_-

content = """# Enterprise Multi-Agent RAG System 🤖📦

Hệ thống Chatbot tra cứu tài liệu nội bộ doanh nghiệp ứng dụng kiến trúc Đa tác nhân (Multi-Agent Workflow) qua **LangGraph**, lưu trữ vector cục bộ bằng **ChromaDB**, và vận hành tối ưu trên phần cứng văn phòng (**RAM 8GB**).

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Framework](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![Database](https://img.shields.io/badge/ChromaDB-Local--Vector-green)
![OS](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey)

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)

| Thành phần         | Công nghệ tích hợp | Chi tiết cấu hình                                            |
| :----------------- | :----------------- | :----------------------------------------------------------- |
| **Frontend UI**    | `Streamlit`        | Giao diện Web trực quan, thân thiện                          |
| **Orchestration**  | `LangGraph`        | Điều phối luồng tư duy Stateful Multi-Agent                  |
| **Storage**        | `ChromaDB`         | Cơ sở dữ liệu Vector lưu trữ vật lý cục bộ                   |
| **LLM Backbone**   | `Llama 3.1`        | Vận hành thông qua Groq API Cloud (Tốc độ cực cao)           |
| **Text Embedding** | `HuggingFace`      | Mô hình nhúng đa ngôn ngữ cục bộ (`paraphrase-multilingual`) |

---

## 📂 Cấu Trúc Thư Mục Dự Án (Project Structure)

```text
├── data/
│   ├── raw/            # Chứa file tài liệu mới tải lên (.txt, .pdf)
│   └── processed/      # Tự động lưu trữ file gốc sau khi nạp xong
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
├── setup.bat / setup_mac.command # Script cài đặt tự động 1-click
├── run.bat / run_mac.command     # Script chạy ứng dụng nhanh 1-click
└── requirements.txt     # Danh sách các thư viện phần mềm bắt buộc cài đặt

```text
## 📥 Tải Mã Nguồn (Chung cho cả hai hệ điều hành)
Tại trang GitHub này, bấm vào nút mã màu xanh Code (ở góc trên bên phải).

Chọn Download ZIP.

Sau khi tải xong, hãy giải nén file ZIP đó vào một thư mục trên máy tính của bạn.
---
## 🪟 HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY TRÊN WINDOWS
⚠️ Yêu cầu hệ thống: Máy tính cần cài đặt sẵn Python 3.10+ và bắt buộc phải tích chọn mục "Add Python to PATH" trong quá trình cài đặt.

🔹 1. Quy trình cài đặt lần đầu
Bước 1.1: Truy cập vào thư mục dự án đã giải nén, tìm và nhấp đúp chuột vào file setup.bat.

Bước 1.2: Màn hình console màu đen sẽ hiện ra -> Bạn hãy dán mã GROQ_API_KEY của mình vào -> Nhấn Enter.

Bước 1.3: Chờ hệ thống tự động thiết lập môi trường ảo (.venv) và tải thư viện. Khi màn hình hiện thông báo [THANH CONG], bạn có thể tắt cửa sổ đó đi.

🔹 2. Quy trình chạy ứng dụng hàng ngày
Bước 2.1: Nhấp đúp chuột vào file run.bat.

Bước 2.2: Hệ thống sẽ khởi động nền tảng Web và tự động mở trình duyệt tại địa chỉ: http://localhost:8501.

## 🍏 HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY TRÊN MACOS
⚠️ Yêu cầu hệ thống: Máy tính cần cài đặt sẵn Python 3.10+.

🔸 1. Cấp quyền thực thi file (Bắt buộc làm lần đầu)
Do cơ chế bảo mật của macOS bảo vệ nghiêm ngặt các file tải từ Internet, bạn cần mở khóa hai file chạy theo các bước sau:

Bước 1.1: Mở ứng dụng Terminal trên máy Mac.

Bước 1.2: Gõ lệnh cd <dấu cách> Kéo và thả thư mục dự án của bạn vào cửa sổ Terminal -> Nhấn Enter.

Bước 1.3: Gõ lệnh trong terminal này và ấn Enter: chmod +x setup_mac.command run_mac.command

🔸 2. Quy trình cài đặt lần đầu
Bước 2.1: Nhấp đúp chuột vào file setup_mac.command.

Bước 2.2: Khi màn hình Terminal hiện yêu cầu nhập Key -> Dán mã GROQ_API_KEY của bạn vào -> Nhấn Enter.

Bước 2.3: Chờ hệ thống cài đặt tự động. Sau khi hoàn tất thành công, bạn có thể đóng tab Terminal này lại.

🔸 3. Quy trình chạy ứng dụng hàng ngày
Bước 3.1: Nhấp đúp chuột vào file run_mac.command.

Bước 3.2: Giao diện ứng dụng Streamlit sẽ tự động được mở trên trình duyệt Safari hoặc Chrome của bạn.
```
