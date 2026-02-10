@echo off
cd /d "%~dp0"
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please create it first.
    pause
    exit /b
)
echo Starting EduQuiz AI...
.venv\Scripts\python -m streamlit run app.py
pause
