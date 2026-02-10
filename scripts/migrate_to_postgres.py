import sqlite3
import psycopg2
import io
import os
from dotenv import load_dotenv

# Robust .env loading for Windows encoding issues (like 'é' in passwords)
env_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(env_path):
    try:
        # Try UTF-8 first
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fallback to Latin-1/Windows-1252 for special characters like 'é'
        with open(env_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    try:
        load_dotenv(stream=io.StringIO(content))
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement du .env : {e}")

def migrate():
    # SQLite connection
    sqlite_path = os.path.join(os.getcwd(), 'data', 'db.sqlite3')
    if not os.path.exists(sqlite_path):
        # Try outside data folder if not found
        sqlite_path = os.path.join(os.getcwd(), 'db.sqlite3')
        if not os.path.exists(sqlite_path):
            print("❌ Fichier SQLite introuvable (tenté data/db.sqlite3 et ./db.sqlite3)")
            return

    try:
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # PostgreSQL connection
        print("🔌 Tentative de connexion à PostgreSQL...")
        
        # Verify credentials
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        dbname = os.getenv('DB_NAME', 'eduquiz_db')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD')
        
        if not password:
            print("❌ Erreur : Le mot de passe (DB_PASSWORD) n'est pas renseigné dans le .env")
            return

        # Clean password (remove quotes if load_dotenv didn't)
        password = password.strip('"').strip("'")

        print(f"📡 Paramètres : Host={host}, Port={port}, DB={dbname}, User={user}")
        
        try:
            # Force standard environment variables
            os.environ['PGCLIENTENCODING'] = 'utf-8'
            
            pg_conn = psycopg2.connect(
                host=host,
                port=port,
                database=dbname,
                user=user,
                password=password,
                connect_timeout=5
            )
        except Exception as conn_err:
            # Detect exact error type from bytes
            raw_err = repr(conn_err)
            if "authentification par mot de passe" in raw_err or "password authentication failed" in raw_err.lower():
                print("\n❌ ERREUR : Le mot de passe pour l'utilisateur 'postgres' est INCORRECT.")
                print(f"🔑 Le script a essayé d'utiliser : {password}")
                print("\n💡 SOLUTIONS :")
                print("1. Vérifiez si vous n'avez pas fait de faute de frappe dans le .env")
                print("2. Essayez d'enlever les guillemets dans le .env (ex: DB_PASSWORD=Chireb@224)")
                print("3. Si vous avez oublié votre mot de passe, vous pouvez le réinitialiser dans pgAdmin.")
            else:
                print(f"❌ La connexion à PostgreSQL a échoué (Erreur: {raw_err})")
            return

        pg_cursor = pg_conn.cursor()
        
        # 1. Create table in PG if not exists
        pg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS score_history (
                id SERIAL PRIMARY KEY,
                score INTEGER NOT NULL,
                time_elapsed VARCHAR(50),
                quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                num_questions INTEGER,
                difficulty VARCHAR(50)
            )
        """)
        
        # 2. Fetch from SQLite
        print("📥 Récupération des données SQLite...")
        sqlite_cursor.execute("SELECT score, time_elapsed, quiz_date, num_questions, difficulty FROM score_history")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print("ℹ️ Aucun score à migrer.")
            return

        # 3. Insert into PG
        print(f"📤 Migration de {len(rows)} scores vers PostgreSQL...")
        for row in rows:
            pg_cursor.execute("""
                INSERT INTO score_history (score, time_elapsed, quiz_date, num_questions, difficulty)
                VALUES (%s, %s, %s, %s, %s)
            """, row)
        
        pg_conn.commit()
        print("✅ Migration terminée avec succès !")
        
    except Exception as e:
        err_msg = str(e).encode('utf-8', 'replace').decode('utf-8')
        print(f"❌ Erreur lors de la migration : {err_msg}")
    finally:
        if 'sqlite_conn' in locals(): sqlite_conn.close()
        if 'pg_conn' in locals(): pg_conn.close()

if __name__ == "__main__":
    migrate()
