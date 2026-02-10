
import os
import sys
from dotenv import load_dotenv

# Try to load .env
load_dotenv()

print("--- System Diagnostics ---")
print(f"Python Version: {sys.version}")

# Check API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY is NOT set in environment.")
elif api_key == "YOUR_API_KEY_HERE":
    print("❌ OPENAI_API_KEY is still set to placeholder 'YOUR_API_KEY_HERE'.")
else:
    print(f"✅ OPENAI_API_KEY is set (Length: {len(api_key)})")
    # Masked preview
    print(f"   Preview: {api_key[:8]}...{api_key[-4:]}")

# Test OpenAI Connection
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI library imported successfully.")
    
    # Try a minimal completion
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("✅ OpenAI Request Success!")
    except Exception as e:
        print(f"❌ OpenAI Request FAILED: {str(e)}")
except ImportError:
    print("❌ OpenAI library is NOT installed.")

# Test Spacy (with crash protection)
print("\n--- Spacy Diagnostics ---")
try:
    import spacy
    print("✅ Spacy library imported successfully.")
    try:
        # This is where the Pydantic error usually happens
        nlp = spacy.load("fr_core_news_sm")
        print("✅ French model 'fr_core_news_sm' loaded successfully.")
    except Exception as e:
        print(f"❌ French model 'fr_core_news_sm' loading failed.")
        print(f"   Error Detail: {str(e)}")
        if "REGEX" in str(e):
            print("   💡 TIP: This is a known Pydantic/Spacy conflict. Try: pip install 'pydantic<2.0'")
except Exception as e:
    print(f"❌ Spacy Diagnostics crashed: {str(e)}")
