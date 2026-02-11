
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

with open("result.txt", "w", encoding="utf-8") as f:
    try:
        genai.configure(api_key=api_key)
        f.write("Configured API\n")
        
        # List models to see what's available
        f.write("Available models:\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"- {m.name}\n")
        
        f.write("\nTesting gemini-1.5-flash:\n")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Hello")
        f.write(f"SUCCESS: {response.text}\n")
        
    except Exception as e:
        f.write(f"\nERROR: {str(e)}\n")
print("Done")
