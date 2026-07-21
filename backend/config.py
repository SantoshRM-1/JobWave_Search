import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"), override=True)
load_dotenv(dotenv_path=os.path.join(os.getcwd(), "backend", ".env"), override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
if not GROQ_API_KEY:
    print("GROQ_API_KEY not found. Resume extraction and job search will use local fallbacks.")

GROQ_MODEL = "llama-3.3-70b-versatile"
