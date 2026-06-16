import os
import streamlit as st
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

class Config:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    CHROMA_DIR = "./chroma_db"
    RAW_DATA_DIR = "./data/raw"
    
    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("LỖI: Chưa cấu hình GROQ_API_KEY trong file .env!")
