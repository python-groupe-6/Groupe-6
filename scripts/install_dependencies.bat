@echo off
echo ==========================================
echo Installation des dependances EduQuiz AI
echo ==========================================

set PYTHON_PATH="C:\Users\Soumah\AppData\Local\Programs\Python\Python312\python.exe"

echo Verification de Python...
if exist %PYTHON_PATH% (
    echo Python 3.14 detecte a : %PYTHON_PATH%
    set PYTHON_CMD=%PYTHON_PATH%
) else (
    echo Python 3.14 non trouve a l'emplacement standard. Test de la commande 'python'...
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python
    ) else (
        echo [ERREUR] Python n'est pas detecte.
        echo Veuillez installer Python 3.14 depuis https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

echo.
echo Creation de l'environnement virtuel (.venv)...
if exist .venv (
    echo L'environnement existe deja.
) else (
    %PYTHON_CMD% -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERREUR] Impossible de creer l'environnement virtuel.
        pause
        exit /b 1
    )
)

echo.
echo Activation de l'environnement virtuel...
call .venv\Scripts\activate

echo.
echo Installation des paquets depuis requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERREUR] Echec de l'installation des dependances.
    pause
    exit /b 1
)

echo.
echo Configuration de la base de donnees Django...
python manage.py migrate
if %errorlevel% neq 0 (
    echo [AVERTISSEMENT] Echec des migrations. Verifiez vos parametres Django.
)

echo.
echo ==========================================
echo INSTALLATION TERMINEE AVEC SUCCES !
echo ==========================================
echo Vous pouvez maintenant lancer l'application Django avec :
echo   .venv\Scripts\activate
echo   python manage.py runserver
echo ==========================================
pause
