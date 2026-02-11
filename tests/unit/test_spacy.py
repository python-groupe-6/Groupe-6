import sys
print(f"Python Version: {sys.version}")
try:
    import spacy
    print("Spacy imported successfully.")
    import pydantic.v1
    print("Pydantic v1 imported successfully.")
except Exception as e:
    print(f"Error: {e}")
