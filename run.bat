@echo off
title TRỢ LÝ ẢO RAG
chcp 65001 > nul
cls

:: Kích hoạt môi trường ảo đã tạo từ trước
call .venv\Scripts\activate

:: Chạy thẳng ứng dụng Streamlit
streamlit run app.py