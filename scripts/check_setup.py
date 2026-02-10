import os
import sys
from dotenv import load_dotenv

# Load env vars
load_dotenv()

print("--- Environment Check ---")
print(f"GOOGLE_API_KEY present: {'GOOGLE_API_KEY' in os.environ}")

print("\n--- Spacy Check ---")
try:
    import spacy
    print(f"Spacy version: {spacy.__version__}")
    try:
        nlp = spacy.load("fr_core_news_sm")
        print("Model 'fr_core_news_sm' loaded successfully.")
    except OSError:
        print("Model 'fr_core_news_sm' NOT found. You may need to run: python -m spacy download fr_core_news_sm")
    except Exception as e:
        print(f"Error loading model: {e}")
except Exception as e:
    print(f"Spacy import failed: {e}")

print("\n--- Database Check ---")
try:
    import psycopg2
    print(f"Psycopg2 version: {psycopg2.__version__}")
    
    # Defaults from database.py
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    dbname = os.getenv('DB_NAME', 'eduquiz_db')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', '')
    
    print(f"Attempting connection to: postgres://{user}:***@{host}:{port}/{dbname}")
    
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=dbname,
            user=user,
            password=password
        )
        print("Connection SUCCESS.")
        conn.close()
    except Exception as e:
        print(f"Connection FAILED: {e}")
        
except ImportError:
    print("Psycopg2 not installed.")
