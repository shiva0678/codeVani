import os
import google.generativeai as genai
from dotenv import load_dotenv

# Look for .env in the backend folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Listing available models:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
