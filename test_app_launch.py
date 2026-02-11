try:
    from src.quiz_generator import QuizGenerator
    print("QuizGenerator imported successfully.")
    generator = QuizGenerator()
    print("QuizGenerator initialized.")
    if generator.nlp is None:
        print("Confirmed: Spacy NLP is None (Fallback mode active).")
    else:
        print("Surprise: Spacy NLP loaded?")
except Exception as e:
    print(f"CRITICAL FAIL: {e}")
    import traceback
    traceback.print_exc()
