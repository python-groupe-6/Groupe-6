@echo off
echo Starting EduQuiz AI (Django)...
echo Activating virtual environment...
REM call .venv\Scripts\activate
REM Using explicit path to ensure correct environment
.venv_new\Scripts\python manage.py runserver
pause
