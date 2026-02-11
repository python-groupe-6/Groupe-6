@echo off
echo Starting EduQuiz AI (Django)...
echo Activating virtual environment...
REM call .venv\Scripts\activate
REM Using explicit path to ensure correct environment
.venv\Scripts\python manage.py runserver 8001
pause
