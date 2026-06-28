import tkinter as tk
from tkinter import messagebox

from db.database import get_connection


class RegisterWindow:
    def __init__(self, parent):
        self.parent = parent

        self.win = tk.Toplevel(parent)
        self.win.title("Регистрация")
        self.win.geometry("460x540")
        self.win.resizable(False, False)
        self.win.configure(bg="#ffffff")
        self.win.transient(parent)
        self.win.grab_set()

        tk.Label(
            self.win,
            text="Регистрация",
            font=("Arial", 22, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(pady=(35, 4))

        tk.Label(
            self.win,
            text="Создание нового аккаунта",
            font=("Arial", 11),
            bg="#ffffff",
            fg="#6b7280",
        ).pack(pady=(0, 30))

        tk.Label(
            self.win,
            text="Логин",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#111827",
            anchor="w",
        ).pack(fill="x", padx=45, pady=(5, 2))

        self.username_entry = tk.Entry(
            self.win,
            font=("Arial", 14),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            bd=1,
            relief="solid",
        )
        self.username_entry.pack(fill="x", padx=45, pady=(0, 15))

        tk.Label(
            self.win,
            text="Пароль",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#111827",
            anchor="w",
        ).pack(fill="x", padx=45, pady=(5, 2))

        self.password_entry = tk.Entry(
            self.win,
            show="*",
            font=("Arial", 14),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            bd=1,
            relief="solid",
        )
        self.password_entry.pack(fill="x", padx=45, pady=(0, 15))

        tk.Label(
            self.win,
            text="Повторите пароль",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#111827",
            anchor="w",
        ).pack(fill="x", padx=45, pady=(5, 2))

        self.confirm_entry = tk.Entry(
            self.win,
            show="*",
            font=("Arial", 14),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            bd=1,
            relief="solid",
        )
        self.confirm_entry.pack(fill="x", padx=45, pady=(0, 35))

        self.register_button = tk.Button(
            self.win,
            text="Зарегистрироваться",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            highlightbackground="#ffffff",
            command=self.register,
        )
        self.register_button.pack(fill="x", padx=45, pady=5, ipady=4)

        self.username_entry.focus()

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if not username or not password or not confirm:
            messagebox.showwarning("Предупреждение", "Заполните все поля")
            return

        if len(username) < 3:
            messagebox.showerror(
                "Ошибка ввода", "Логин должен содержать минимум 3 символа"
            )
            return

        if len(password) < 3:
            messagebox.showerror(
                "Ошибка ввода", "Пароль должен содержать минимум 3 символа"
            )
            return

        if password != confirm:
            messagebox.showerror("Ошибка ввода", "Пароли не совпадают")
            return

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            exists = cur.fetchone()[0]

            if exists > 0:
                messagebox.showerror(
                    "Ошибка регистрации", "Пользователь уже существует"
                )
                return

            cur.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES (?, ?, 'client')
            """,
                (username, password),
            )

            conn.commit()
            messagebox.showinfo("Успешно", "Аккаунт успешно создан")
            self.win.destroy()

        except Exception as e:
            messagebox.showerror(
                "Ошибка базы данных", f"Не удалось выполнить регистрацию: {e}"
            )
        finally:
            if conn:
                conn.close()
