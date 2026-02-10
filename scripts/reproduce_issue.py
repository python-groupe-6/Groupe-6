
import os
from quiz_generator import QuizGenerator

def test_num_questions():
    generator = QuizGenerator()
    test_text = """
    Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability 
    with the use of significant indentation. Python is dynamically-typed and garbage-collected. 
    It supports multiple programming paradigms, including structured, object-oriented and functional programming.
    It was created by Guido van Rossum and first released in 1991.
    The Python Software Foundation (PSF) is a non-profit organization which holds the copyright to the Python programming language.
    PyPy is a fast, compliant interpreter of the Python language.
    CPython is the reference implementation of the Python language.
    Anaconda is a distribution of the Python and R programming languages for scientific computing.
    Jupyter Notebook is a web-based interactive computing platform.
    """
    
    for count in [3, 5, 8]:
        print(f"\nRequesting {count} questions...")
        quiz = generator.generate_quiz(test_text, num_questions=count)
        print(f"Generated {len(quiz)} questions.")
        if len(quiz) != count:
            print(f"FAILED: Expected {count}, got {len(quiz)}")
        else:
            print("SUCCESS")

if __name__ == "__main__":
    test_num_questions()
