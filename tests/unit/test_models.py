
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

models_to_test = [
    "gemini-2.0-flash-lite", 
    "gemini-flash-latest",
    "gemini-1.5-flash", 
    "gemini-1.5-pro",
    "gemini-2.0-flash" 
]

results = []

print(f"Testing {len(models_to_test)} models...")

try:
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Configuration Error: {e}")
    exit(1)

for model_name in models_to_test:
    print(f"Testing {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, reply with one word: Success.")
        print(f"SUCCESS with {model_name}: {response.text.strip()}")
        results.append(f"{model_name}: SUCCESS")
    except Exception as e:
        print(f"FAILED {model_name}: {e}")
        results.append(f"{model_name}: FAILED - {str(e)[:100]}...")

with open("result_models.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))
    
print("Done. Results saved to result_models.txt")
