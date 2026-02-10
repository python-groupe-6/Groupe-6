import subprocess
import sys
import os

def check_dependencies():
    """Checks if spacy model is installed, if not, downloads it."""
    try:
        import spacy
        import fpdf
        try:
            spacy.load("fr_core_news_sm")
        except OSError:
            print("Downloading French NLP model...")
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "fr_core_news_sm"])
    except ImportError:
        print("Missing dependencies. Please run 'pip install -r requirements.txt' first.")
        return False
    return True

def start_app():
    """Launches the Streamlit app."""
    if check_dependencies():
        print("Launching EduQuiz AI...")
        # Path to app.py in the same directory
        app_path = os.path.join(os.path.dirname(__file__), "app.py")
        subprocess.run(["streamlit", "run", app_path])
    else:
        print("Failed to start application due to missing dependencies.")

if __name__ == "__main__":
    start_app()
