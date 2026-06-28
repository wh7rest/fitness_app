import os
import sys
import tkinter as tk
from tkinter import messagebox

from auth.register import RegisterWindow
from db.database import get_connection


class LoginWindow:
    def __init__(self):
        # МАТЕМАТИЧЕСКИЙ ТЕСТ ВЫПОЛНЕНИЯ КОДА
        print("\n" + "=" * 40)
        print("DEBUG: ЗАПУЩЕНА НОВАЯ ВЕРСИЯ LOGIN.PY")
        print(f"РАБОЧАЯ ДИРЕКТОРИЯ: {os.getcwd()}")
        print("=" * 40 + "\n")
        sys.stdout.flush()

        self.is_authenticated = False
        self.current_user = None

        self.root = tk.Tk()
        self.root.title("Авторизация")
        self.root.geometry("460x520")
        self.root.resizable(False, False)

        # Меняем фон на серый, чтобы проверить контрастность полей
        self.root.configure(bg="#f3f4f6")

        icon_path = os.path.abspath(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        # Текст с принудительным fg
        tk.Label(
            self.root,
            text="Вход в систему",
            font=("Arial", 22, "bold"),
            bg="#f3f4f6",
            fg="#111827",
        ).pack(pady=(45, 4))

        tk.Label(
            self.root,
            text="Система учёта фитнес-клуба",
            font=("Arial", 11),
            bg="#f3f4f6",
            fg="#6b7280",
        ).pack(pady=(0, 35))

        tk.Label(
            self.root,
            text="Логин",
            font=("Arial", 11, "bold"),
            bg="#f3f4f6",
            fg="#111827",
            anchor="w",
        ).pack(fill="x", padx=45, pady=(5, 2))

        # Добавляем явную рамку highlightbackground для macOS
        self.username_entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            highlightbackground="#d1d5db",
            highlightthickness=1,
            bd=0,
        )
        self.username_entry.pack(fill="x", padx=45, pady=(0, 20), ipady=4)

        tk.Label(
            self.root,
            text="Пароль",
            font=("Arial", 11, "bold"),
            bg="#f3f4f6",
            fg="#111827",
            anchor="w",
        ).pack(fill="x", padx=45, pady=(5, 2))

        self.password_entry = tk.Entry(
            self.root,
            show="*",
            font=("Arial", 14),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            highlightbackground="#d1d5db",
            highlightthickness=1,
            bd=0,
        )
        self.password_entry.pack(fill="x", padx=45, pady=(0, 35), ipady=4)

        self.login_button = tk.Button(
            self.root, text="Войти", font=("Arial", 12, "bold"), command=self.login
        )
        self.login_button.pack(fill="x", padx=45, pady=5, ipady=4)

        self.register_button = tk.Button(
            self.root,
            text="Создать аккаунт",
            font=("Arial", 12, "bold"),
            command=self.open_register,
        )
        self.register_button.pack(fill="x", padx=45, pady=5, ipady=4)

        self.username_entry.focus()
        self.root.bind("<Return>", lambda event: self.login())

    def open_register(self):
        RegisterWindow(self.root)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Предупреждение", "Введите логин и пароль")
            return

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, username, password, role
                FROM users
                WHERE username = ? AND password = ?
            """,
                (username, password),
            )

            user = cur.fetchone()

            if user:
                self.is_authenticated = True
                self.current_user = {
                    "id": user["id"],
                    "username": user["username"],
                    "role": user["role"],
                }
                self.root.destroy()
            else:
                messagebox.showerror("Ошибка входа", "Неверный логин или пароль")
        except Exception as e:
            messagebox.showerror(
                "Ошибка базы данных", f"Не удалось выполнить запрос: {e}"
            )
        finally:
            if conn:
                conn.close()

    def run(self):
        self.root.mainloop()
