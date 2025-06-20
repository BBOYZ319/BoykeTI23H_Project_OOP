from data.database import connect_db
from models.user import User

# Fungsi register

def register(username, password):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        print(f"[SERVER] Registrasi berhasil untuk user: {username}")
        return True
    except Exception as e:
        print("[SERVER] ERROR saat registrasi:", e)
        return False
    finally:
        db.close()

# Fungsi login

def login(username, password):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            print(f"[SERVER] Login berhasil: {username}")
            return User(user_id=result[0], username=result[1], password=result[2])
        else:
            print(f"[SERVER] Login gagal untuk user: {username}")
            return None
    except Exception as e:
        print("[SERVER] ERROR saat login:", e)
        return None
    finally:
        db.close()

# Fungsi hapus akun

def delete_account(user):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM files WHERE user_id = %s", (user.user_id,))
        cursor.execute("DELETE FROM users WHERE id = %s", (user.user_id,))
        db.commit()
        print(f"[SERVER] Akun user '{user.username}' dan semua file terkait berhasil dihapus.")
        return True
    except Exception as e:
        print("[SERVER] ERROR saat hapus akun:", e)
        return False
    finally:
        db.close()

__all__ = ["register", "login", "delete_account"]
