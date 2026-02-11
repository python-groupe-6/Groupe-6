@echo off
echo ==========================================
echo Lancement du serveur Django EduQuiz AI
echo ==========================================

if not exist .venv (
    echo [ERREUR] L'environnement virtuel .venv est introuvable.
    echo Veuillez d'abord executer install_dependencies.bat
    pause
    exit /b 1
)

echo Activation de l'environnement virtuel...
call .venv\Scripts\activate

echo Lancement du serveur...
python manage.py runserver

pause
