import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import re

# ============ KONFIGURASI WARNA ============
BG_COLOR = "#1e1e2e"
CARD_COLOR = "#2a2a3e"
ACCENT = "#7c3aed"
ACCENT_HOVER = "#6d28d9"
TEXT_COLOR = "#ffffff"
TEXT_MUTED = "#a1a1aa"
ENTRY_BG = "#3a3a4e"
SUCCESS = "#10b981"
DANGER = "#ef4444"


# ============ DATABASE ============
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password):
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hash_password(password)),
        )
        conn.commit()
        conn.close()
        return True, "Registrasi berhasil!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username sudah digunakan!"
        elif "email" in str(e):
            return False, "Email sudah terdaftar!"
        return False, "Data sudah ada!"
    except Exception as e:
        return False, f"Error: {e}"


def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hash_password(password)),
    )
    user = c.fetchone()
    conn.close()
    return user


# ============ WIDGET KUSTOM ============
class ModernButton(tk.Button):
    """Tombol dengan efek hover"""
    def __init__(self, parent, text, command, bg=ACCENT, hover=ACCENT_HOVER, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=TEXT_COLOR,
            activebackground=hover,
            activeforeground=TEXT_COLOR,
            font=("Segoe UI", 11, "bold"),
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10,
            **kwargs,
        )
        self.default_bg = bg
        self.hover_bg = hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        self.config(bg=self.hover_bg)

    def _on_leave(self, e):
        self.config(bg=self.default_bg)


class ModernEntry(tk.Frame):
    """Entry dengan placeholder & styling"""
    def __init__(self, parent, placeholder="", show=None):
        super().__init__(parent, bg=ENTRY_BG, highlightthickness=1,
                         highlightbackground=ENTRY_BG, highlightcolor=ACCENT)
        self.placeholder = placeholder
        self.show_char = show

        self.entry = tk.Entry(
            self, bd=0, bg=ENTRY_BG, fg=TEXT_MUTED,
            font=("Segoe UI", 11), insertbackground=TEXT_COLOR,
            show="" if show else "",
        )
        self.entry.pack(fill="x", padx=10, pady=8)
        self.entry.insert(0, placeholder)

        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, e):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=TEXT_COLOR)
            if self.show_char:
                self.entry.config(show=self.show_char)

    def _on_focus_out(self, e):
        if self.entry.get() == "":
            self.entry.config(fg=TEXT_MUTED, show="")
            self.entry.insert(0, self.placeholder)

    def get(self):
        val = self.entry.get()
        if val == self.placeholder:
            return ""
        return val

    def clear(self):
        self.entry.delete(0, tk.END)
        self._on_focus_out(None)


# ============ APLIKASI UTAMA ============
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Login & Registrasi")
        self.geometry("900x600")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        # Center window
        self.update_idletasks()
        w, h = 900, 600
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        init_db()
        self.current_user = None
        self.show_login()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ---------- LOGIN PAGE ----------
    def show_login(self):
        self.clear_window()
        self._build_auth_layout(
            title="Selamat Datang Kembali",
            subtitle="Silakan login untuk melanjutkan",
            button_text="LOGIN",
            on_submit=self.handle_login,
            switch_text="Belum punya akun? Daftar di sini",
            switch_command=self.show_register,
            is_register=False,
        )

    # ---------- REGISTER PAGE ----------
    def show_register(self):
        self.clear_window()
        self._build_auth_layout(
            title="Buat Akun Baru",
            subtitle="Isi data berikut untuk mendaftar",
            button_text="DAFTAR",
            on_submit=self.handle_register,
            switch_text="Sudah punya akun? Login di sini",
            switch_command=self.show_login,
            is_register=True,
        )

    # ---------- SHARED AUTH LAYOUT ----------
    def _build_auth_layout(self, title, subtitle, button_text,
                           on_submit, switch_text, switch_command, is_register):
        # Frame kiri (branding)
        left = tk.Frame(self, bg=ACCENT, width=380)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="🔐", font=("Segoe UI Emoji", 60),
                 bg=ACCENT, fg=TEXT_COLOR).pack(pady=(120, 20))
        tk.Label(left, text="SecureApp", font=("Segoe UI", 26, "bold"),
                 bg=ACCENT, fg=TEXT_COLOR).pack()
        tk.Label(left, text="Platform aman untuk kebutuhanmu",
                 font=("Segoe UI", 11), bg=ACCENT, fg="#e9d5ff").pack(pady=5)
        tk.Label(left, text="• Password di-hash SHA-256\n• Data tersimpan lokal\n• UI modern & responsif",
                 font=("Segoe UI", 10), bg=ACCENT, fg="#e9d5ff",
                 justify="left").pack(pady=40, padx=40, anchor="w")

        # Frame kanan (form)
        right = tk.Frame(self, bg=BG_COLOR)
        right.pack(side="right", fill="both", expand=True)

        container = tk.Frame(right, bg=CARD_COLOR)
        container.place(relx=0.5, rely=0.5, anchor="center", width=420, height=460 if is_register else 400)

        tk.Label(container, text=title, font=("Segoe UI", 20, "bold"),
                 bg=CARD_COLOR, fg=TEXT_COLOR).pack(pady=(30, 5))
        tk.Label(container, text=subtitle, font=("Segoe UI", 10),
                 bg=CARD_COLOR, fg=TEXT_MUTED).pack(pady=(0, 20))

        # Username
        tk.Label(container, text="Username", font=("Segoe UI", 10, "bold"),
                 bg=CARD_COLOR, fg=TEXT_MUTED, anchor="w").pack(fill="x", padx=35)
        self.username_entry = ModernEntry(container, "Masukkan username")
        self.username_entry.pack(fill="x", padx=35, pady=(5, 12))

        # Email (hanya register)
        if is_register:
            tk.Label(container, text="Email", font=("Segoe UI", 10, "bold"),
                     bg=CARD_COLOR, fg=TEXT_MUTED, anchor="w").pack(fill="x", padx=35)
            self.email_entry = ModernEntry(container, "contoh@email.com")
            self.email_entry.pack(fill="x", padx=35, pady=(5, 12))

        # Password
        tk.Label(container, text="Password", font=("Segoe UI", 10, "bold"),
                 bg=CARD_COLOR, fg=TEXT_MUTED, anchor="w").pack(fill="x", padx=35)
        self.password_entry = ModernEntry(container, "Masukkan password", show="•")
        self.password_entry.pack(fill="x", padx=35, pady=(5, 12))

        # Konfirmasi Password (hanya register)
        if is_register:
            tk.Label(container, text="Konfirmasi Password",
                     font=("Segoe UI", 10, "bold"),
                     bg=CARD_COLOR, fg=TEXT_MUTED, anchor="w").pack(fill="x", padx=35)
            self.confirm_entry = ModernEntry(container, "Ulangi password", show="•")
            self.confirm_entry.pack(fill="x", padx=35, pady=(5, 12))

        # Tombol submit
        ModernButton(container, button_text, on_submit).pack(
            fill="x", padx=35, pady=(15, 10)
        )

        # Link switch
        switch = tk.Label(container, text=switch_text, font=("Segoe UI", 9, "underline"),
                          bg=CARD_COLOR, fg=ACCENT, cursor="hand2")
        switch.pack(pady=(5, 25))
        switch.bind("<Button-1>", lambda e: switch_command())

        # Bind Enter
        self.bind("<Return>", lambda e: on_submit())

    # ---------- HANDLERS ----------
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan password wajib diisi!")
            return

        user = login_user(username, password)
        if user:
            self.current_user = user[1]
            messagebox.showinfo("Sukses", f"Selamat datang, {user[1]}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Gagal", "Username atau password salah!")

    def handle_register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        # Validasi
        if not all([username, email, password, confirm]):
            messagebox.showwarning("Peringatan", "Semua field wajib diisi!")
            return

        if len(username) < 3:
            messagebox.showwarning("Peringatan", "Username minimal 3 karakter!")
            return

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showwarning("Peringatan", "Format email tidak valid!")
            return

        if len(password) < 6:
            messagebox.showwarning("Peringatan", "Password minimal 6 karakter!")
            return

        if password != confirm:
            messagebox.showerror("Gagal", "Password dan konfirmasi tidak sama!")
            return

        success, msg = register_user(username, email, password)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.show_login()
        else:
            messagebox.showerror("Gagal", msg)

    # ---------- DASHBOARD ----------
    def show_dashboard(self):
        self.clear_window()
        self.unbind("<Return>")

        # Topbar
        topbar = tk.Frame(self, bg=CARD_COLOR, height=70)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="🏠  Dashboard", font=("Segoe UI", 16, "bold"),
                 bg=CARD_COLOR, fg=TEXT_COLOR).pack(side="left", padx=25)

        ModernButton(topbar, "Logout", self.handle_logout,
                     bg=DANGER, hover="#dc2626").pack(side="right", padx=20, pady=15)

        tk.Label(topbar, text=f"👤 {self.current_user}",
                 font=("Segoe UI", 11), bg=CARD_COLOR, fg=TEXT_MUTED).pack(
            side="right", padx=15
        )

        # Content
        content = tk.Frame(self, bg=BG_COLOR)
        content.pack(fill="both", expand=True, padx=40, pady=40)

        card = tk.Frame(content, bg=CARD_COLOR)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="🎉", font=("Segoe UI Emoji", 60),
                 bg=CARD_COLOR, fg=TEXT_COLOR).pack(pady=(60, 10))

        tk.Label(card, text=f"Halo, {self.current_user}!",
                 font=("Segoe UI", 24, "bold"),
                 bg=CARD_COLOR, fg=TEXT_COLOR).pack()

        tk.Label(card, text="Kamu berhasil login ke aplikasi.",
                 font=("Segoe UI", 12), bg=CARD_COLOR, fg=TEXT_MUTED).pack(pady=10)

        tk.Label(card,
                 text="Silakan kembangkan aplikasi ini sesuai kebutuhanmu.\n"
                      "Kamu bisa menambahkan fitur seperti profil, settings, dll.",
                 font=("Segoe UI", 10), bg=CARD_COLOR, fg=TEXT_MUTED,
                 justify="center").pack(pady=20)

    def handle_logout(self):
        if messagebox.askyesno("Logout", "Yakin ingin logout?"):
            self.current_user = None
            self.show_login()


# ============ MAIN ============
if __name__ == "__main__":
    app = App()
    app.mainloop()