"""
Database module for EduQuiz AI.
Handles PostgreSQL connection with automatic fallback to SQLite for local development.
"""

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    psycopg2 = None
    sql = None
import sqlite3
import os
from datetime import datetime
try:
    from dotenv import load_dotenv
    import io
    # Robust .env loading for Windows encoding issues
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(env_path, 'r', encoding='latin-1') as f:
                content = f.read()
        load_dotenv(stream=io.StringIO(content))
    else:
        load_dotenv()
except ImportError:
    pass

# Configuration PostgreSQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'eduquiz_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Variable globale pour suivre le mode actuel
CURRENT_DB_MODE = "None" 

def get_connection():
    """
    Tente une connexion PostgreSQL, sinon bascule sur SQLite.
    Retourne (connexion, type_db) où type_db est 'postgres' ou 'sqlite'.
    """
    global CURRENT_DB_MODE
    
    # Tentative PostgreSQL
    if DB_CONFIG['password'] and psycopg2: # On ne tente que si un mot de passe est configuré et le pilote présent
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            CURRENT_DB_MODE = "PostgreSQL"
            return conn, "postgres"
        except Exception as e:
            # Silently check if we should fallback (print only for debugging)
            pass

    # Fallback SQLite
    try:
        # DB is now in ../data/ relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'data', 'db.sqlite3')
        conn = sqlite3.connect(db_path, check_same_thread=False)
        CURRENT_DB_MODE = "SQLite"
        return conn, "sqlite"
    except Exception as e:
        print(f"Erreur connexion SQLite: {e}")
        CURRENT_DB_MODE = "Error"
        return None, None

def get_db_mode():
    return CURRENT_DB_MODE

def init_database():
    """
    Initialise la base de données selon le moteur connecté.
    """
    conn, db_type = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Syntaxe SQL adaptée
        if db_type == 'postgres':
            create_query = """
                CREATE TABLE IF NOT EXISTS score_history (
                    id SERIAL PRIMARY KEY,
                    score INTEGER NOT NULL,
                    time_elapsed VARCHAR(50),
                    quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    num_questions INTEGER,
                    difficulty VARCHAR(50)
                )
            """
        else: # sqlite
            create_query = """
                CREATE TABLE IF NOT EXISTS score_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score INTEGER NOT NULL,
                    time_elapsed TEXT,
                    quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    num_questions INTEGER,
                    difficulty TEXT
                )
            """
            
        cursor.execute(create_query)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Database initialization error ({db_type}): {e}")
        return False

def save_score(score, time_elapsed, num_questions=5, difficulty="Standard"):
    """
    Sauvegarde le score en s'adaptant à la syntaxe SQL (%s vs ?).
    """
    conn, db_type = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        if db_type == 'postgres':
            query = """
                INSERT INTO score_history (score, time_elapsed, num_questions, difficulty)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (score, time_elapsed, num_questions, difficulty))
        else:
            query = """
                INSERT INTO score_history (score, time_elapsed, num_questions, difficulty)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (score, time_elapsed, num_questions, difficulty))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving score: {e}")
        return False

def get_score_history(limit=10):
    """
    Récupère l'historique des scores.
    """
    conn, db_type = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        if db_type == 'postgres':
            query = """
                SELECT score, time_elapsed, quiz_date, num_questions, difficulty
                FROM score_history
                ORDER BY quiz_date DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
        else:
            query = """
                SELECT score, time_elapsed, quiz_date, num_questions, difficulty
                FROM score_history
                ORDER BY quiz_date DESC
                LIMIT ?
            """
            cursor.execute(query, (limit,))
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Standardisation du format de date
        history = []
        for row in rows:
            # row[2] peut être string (sqlite) ou datetime (postgres)
            date_val = row[2]
            if isinstance(date_val, str):
                try:
                    # SQLite default timestamp format: YYYY-MM-DD HH:MM:SS
                    dt_obj = datetime.strptime(date_val.split('.')[0], "%Y-%m-%d %H:%M:%S")
                    formatted_date = dt_obj.strftime("%d/%m %H:%M")
                except:
                    formatted_date = date_val
            elif isinstance(date_val, datetime):
                formatted_date = date_val.strftime("%d/%m %H:%M")
            else:
                formatted_date = ""

            history.append({
                'score': row[0],
                'time': row[1],
                'date': formatted_date,
                'num_questions': row[3],
                'difficulty': row[4]
            })
        
        return history
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

def get_stats():
    """
    Récupère les statistiques globales.
    """
    conn, db_type = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_quizzes,
                AVG(score) as avg_score,
                MAX(score) as best_score
            FROM score_history
        """)
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return {
                'total_quizzes': row[0] or 0,
                'avg_score': round(row[1], 1) if row[1] else 0,
                'best_score': row[2] or 0
            }
        return None
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return None
