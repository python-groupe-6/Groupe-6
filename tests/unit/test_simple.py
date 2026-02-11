
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

try:
    genai.configure(api_key=api_key)
    # Essai avec gemini-1.5-flash qui est plus stable/répandu
    model = genai.GenerativeModel("gemini-1.5-flash")
    print(f"Testing model: gemini-1.5-flash")
    response = model.generate_content("Hello")
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"ERROR: {e}")
