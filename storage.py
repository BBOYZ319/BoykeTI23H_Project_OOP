import os
from tkinter import filedialog
from data.database import connect_db

class Storage:
    def __init__(self, user):
        self.user = user

    def backup_file_from_local(self, file_path):
        try:
            db = connect_db()
            cursor = db.cursor()

            with open(file_path, "rb") as f:
                file_data = f.read()

            filename = os.path.basename(file_path)
            cursor.execute(
                "INSERT INTO files (user_id, filename, filedata) VALUES (%s, %s, %s)",
                (self.user.user_id, filename, file_data)
            )
            db.commit()
            print(f"[SERVER] File '{filename}' berhasil dibackup.")
            return True
        except Exception as e:
            print("[SERVER] Gagal backup file:", e)
            return False
        finally:
            db.close()

    def list_files(self):
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT filename FROM files WHERE user_id = %s", (self.user.user_id,))
            files = [row[0] for row in cursor.fetchall()]
            return files
        except Exception as e:
            print("[SERVER] Gagal ambil daftar file:", e)
            return []
        finally:
            db.close()

    def delete_file(self, filename):
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM files WHERE user_id = %s AND filename = %s",
                (self.user.user_id, filename)
            )
            db.commit()
            print(f"[SERVER] File '{filename}' berhasil dihapus.")
            return True
        except Exception as e:
            print("[SERVER] Gagal menghapus file:", e)
            return False
        finally:
            db.close()

    def download_file(self, filename):
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "SELECT filedata FROM files WHERE user_id = %s AND filename = %s",
                (self.user.user_id, filename)
            )
            result = cursor.fetchone()
            if result and result[0]:
                file_data = result[0]
                save_path = filedialog.asksaveasfilename(
                    defaultextension=os.path.splitext(filename)[1],
                    initialfile=filename,
                    filetypes=[("All Files", "*.*")]
                )
                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(file_data)
                    print(f"[SERVER] File '{filename}' berhasil disimpan ke: {save_path}")
                    return True
                else:
                    print("[SERVER] Penyimpanan file dibatalkan oleh user.")
                    return False
            else:
                print(f"[SERVER] File '{filename}' tidak ditemukan di database.")
                return False
        except Exception as e:
            print("[SERVER] Gagal download file:", e)
            return False
        finally:
            db.close()
