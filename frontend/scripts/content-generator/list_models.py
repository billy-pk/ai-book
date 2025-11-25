import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
MODEL_API_KEY = os.getenv("MODEL_API_KEY")
if not MODEL_API_KEY:
    print("MODEL_API_KEY not found.")
else:
    genai.configure(api_key=MODEL_API_KEY)
    print("Available models:")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"  {m.name}")