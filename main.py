import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from auth.auth import register, login, delete_account
from models.storage import Storage

current_user = None
dashboard_frame = None  # Global untuk digunakan lintas fungsi


def on_register():
    username = entry_user.get()
    password = entry_pass.get()
    if username and password:
        register(username, password)
        messagebox.showinfo("Registrasi", "Registrasi berhasil.")
    else:
        messagebox.showwarning("Input Error", "Isi username dan password.")


def on_login():
    global current_user
    username = entry_user.get()
    password = entry_pass.get()
    user = login(username, password)
    if user:
        current_user = user
        messagebox.showinfo("Login", f"Selamat datang, {user.username}")
        print(f"[SERVER] User '{user.username}' berhasil login.")
        open_dashboard()
    else:
        messagebox.showerror("Login Gagal", "Username atau password salah.")


def choose_and_backup():
    if not current_user:
        messagebox.showerror("Akses Ditolak", "Silakan login terlebih dahulu.")
        return

    file_path = filedialog.askopenfilename()
    if file_path:
        storage = Storage(current_user)
        storage.backup_file_from_local(file_path)
        messagebox.showinfo("Sukses", f"File '{os.path.basename(file_path)}' berhasil dibackup.")
        
        try:
            if dashboard_frame and dashboard_frame.winfo_exists():
                refresh_file_list(dashboard_frame)
        except tk.TclError:
            print("[SERVER] Gagal refresh file list karena frame tidak tersedia.")


def on_delete_account():
    global current_user, dashboard_frame
    confirm = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus akun ini?")
    if confirm:
        if delete_account(current_user):
            messagebox.showinfo("Sukses", "Akun berhasil dihapus.")
            current_user = None
            try:
                if dashboard_frame and dashboard_frame.winfo_exists():
                    dashboard_frame.winfo_toplevel().destroy()
            except tk.TclError:
                pass
            root.deiconify()
        else:
            messagebox.showerror("Gagal", "Terjadi kesalahan saat menghapus akun.")


def delete_selected_file(frame, filename):
    storage = Storage(current_user)
    confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus file '{filename}'?")
    if confirm:
        success = storage.delete_file(filename)
        if success:
            messagebox.showinfo("Berhasil", f"File '{filename}' berhasil dihapus.")
            try:
                if frame and frame.winfo_exists():
                    refresh_file_list(frame)
            except tk.TclError:
                print("[SERVER] Frame tidak tersedia saat refresh file.")
        else:
            messagebox.showerror("Gagal", f"Gagal menghapus file '{filename}'.")


def refresh_file_list(frame):
    try:
        storage = Storage(current_user)
        files = storage.list_files()

        for widget in frame.winfo_children():
            widget.destroy()

        for filename in files:
            row = ttk.Frame(frame)
            row.pack(pady=2, anchor="w")

            lbl = ttk.Label(row, text=filename, width=25)
            lbl.pack(side=tk.LEFT, padx=5)

            btn_del = ttk.Button(row, text="Hapus", command=lambda f=filename: delete_selected_file(frame, f))
            btn_del.pack(side=tk.RIGHT, padx=3)

            btn_dl = ttk.Button(row, text="Unduh", command=lambda f=filename: download_selected_file(f))
            btn_dl.pack(side=tk.RIGHT, padx=3)

    except tk.TclError as e:
        print(f"[SERVER] Gagal refresh file list: {e}")


def download_selected_file(filename):
    storage = Storage(current_user)
    success = storage.download_file(filename)
    if success:
        messagebox.showinfo("Berhasil", f"File '{filename}' berhasil diunduh.")
    else:
        messagebox.showerror("Gagal", f"File '{filename}' gagal diunduh.")


def open_dashboard():
    global dashboard_frame
    dashboard = tk.Toplevel(root)
    dashboard.title("Beranda OUO")
    dashboard.geometry("400x450")
    dashboard.configure(bg="#1e1e2f")

    ttk.Label(
        dashboard, 
        text=f"Selamat datang, {current_user.username}",
        font=("Segoe UI", 12, "bold"),
        foreground="white",
        background="#1e1e2f"
    ).pack(pady=10)

    ttk.Button(dashboard, text="Backup File dari Komputer", command=choose_and_backup).pack(pady=5)
    ttk.Button(dashboard, text="Hapus Akun", command=on_delete_account).pack(pady=5)

    ttk.Label(dashboard, text="File Anda:", background="#1e1e2f", foreground="white").pack(pady=(15, 5))

    dashboard_frame = ttk.Frame(dashboard)
    dashboard_frame.pack(fill="both", expand=True)

    refresh_file_list(dashboard_frame)


# === Main Window ===
root = tk.Tk()
root.title("OUO - Login/Register")
root.geometry("400x350")
root.configure(bg="#1e1e2f")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Segoe UI", 10))
style.configure("TEntry", padding=5, font=("Segoe UI", 10))
style.configure("TButton", padding=6, font=("Segoe UI", 10), background="#4f89c6", foreground="white")

ttk.Label(root, text="Username").pack(pady=(30, 5))
entry_user = ttk.Entry(root, width=30)
entry_user.pack()

ttk.Label(root, text="Password").pack(pady=(15, 5))
entry_pass = ttk.Entry(root, show="*", width=30)
entry_pass.pack()

ttk.Button(root, text="Login", command=on_login).pack(pady=(25, 10))
ttk.Button(root, text="Register", command=on_register).pack()

print("[SERVER] GUI OUO aktif. Menunggu user...")
root.mainloop()
