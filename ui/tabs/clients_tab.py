import tkinter as tk
from tkinter import messagebox, ttk

from db.database import get_connection


class ClientsTab:
    def __init__(self, parent):
        self.parent = parent

        self.frame = tk.Frame(parent, bg="#f3f4f6")
        self.frame.pack(fill="both", expand=True)

        card = tk.Frame(
            self.frame,
            bg="#ffffff",
            bd=0,
            highlightthickness=1,
            highlightbackground="#e5e7eb",
        )
        card.pack(fill="both", expand=True, padx=10, pady=10)

        title = tk.Label(
            card,
            text="Клиенты",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#111827",
        )
        title.pack(anchor="w", padx=16, pady=(14, 4))

        subtitle = tk.Label(
            card,
            text="Добавление, редактирование и удаление клиентов клуба",
            font=("Helvetica", 9),
            bg="#ffffff",
            fg="#6b7280",
        )
        subtitle.pack(anchor="w", padx=16, pady=(0, 4))

        self.count_label = tk.Label(
            card,
            text="Всего клиентов: 0",
            font=("Helvetica", 9),
            bg="#ffffff",
            fg="#6b7280",
        )
        self.count_label.pack(anchor="w", padx=16, pady=(0, 10))

        btn_frame = tk.Frame(card, bg="#ffffff")
        btn_frame.pack(fill="x", padx=16, pady=(0, 10))

        # Использование ttk.Button гарантирует видимость на Mac
        ttk.Button(btn_frame, text="Обновить", command=self.load).pack(
            side="left", padx=4
        )
        ttk.Button(
            btn_frame, text="Добавить клиента", command=self.open_add_window
        ).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Изменить", command=self.open_edit_window).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Удалить клиента", command=self.delete_client).pack(
            side="left", padx=4
        )

        table_frame = tk.Frame(card, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.tree = ttk.Treeview(
            table_frame,
            style="App.Treeview",
            columns=("id", "name", "phone", "email", "start", "end"),
            show="headings",
            height=15,
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Email")
        self.tree.heading("start", text="Начало")
        self.tree.heading("end", text="Окончание")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=220)
        self.tree.column("phone", width=130)
        self.tree.column("email", width=220)
        self.tree.column("start", width=120, anchor="center")
        self.tree.column("end", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda event: self.open_edit_window())
        self.load()

    def load(self):
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT id, full_name, phone, email, membership_start, membership_end FROM clients ORDER BY full_name"
            )
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        r["id"],
                        r["full_name"],
                        r["phone"],
                        r["email"],
                        r["membership_start"],
                        r["membership_end"],
                    ),
                )
            self.count_label.config(text=f"Всего клиентов: {len(rows)}")
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось загрузить данные: {e}")
        finally:
            if conn:
                conn.close()

    def validate_client_data(self, full_name, phone, email):
        if not full_name.strip():
            messagebox.showerror("Ошибка ввода", "Поле ФИО обязательно")
            return False
        if not phone.strip() or len(phone.strip()) < 5:
            messagebox.showerror("Ошибка ввода", "Введите корректный номер телефона")
            return False
        if email.strip() and "@" not in email.strip():
            messagebox.showerror("Ошибка ввода", "Некорректный email")
            return False
        return True

    def open_add_window(self):
        win = tk.Toplevel(self.parent)
        win.title("Добавление клиента")
        win.geometry("400x340")
        win.transient(self.parent)
        win.grab_set()
        win.configure(bg="#ffffff")

        tk.Label(
            win,
            text="Добавление клиента",
            font=("Helvetica", 13, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(pady=(14, 12))
        form = tk.Frame(win, bg="#ffffff")
        form.pack(padx=20, fill="x")

        tk.Label(form, text="ФИО", bg="#ffffff", anchor="w").pack(fill="x")
        name = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        name.pack(pady=(4, 10), ipady=4)

        tk.Label(form, text="Телефон", bg="#ffffff", anchor="w").pack(fill="x")
        phone = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        phone.pack(pady=(4, 10), ipady=4)

        tk.Label(form, text="Email", bg="#ffffff", anchor="w").pack(fill="x")
        email = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        email.pack(pady=(4, 10), ipady=4)

        def save():
            full_name = name.get().strip()
            phone_value = phone.get().strip()
            email_value = email.get().strip()

            if not self.validate_client_data(full_name, phone_value, email_value):
                return

            conn = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO clients (full_name, phone, email, membership_start, membership_end)
                    VALUES (?, ?, ?, DATE('now'), DATE('now','+1 year'))
                """,
                    (full_name, phone_value, email_value),
                )
                conn.commit()
                win.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить: {e}")
            finally:
                if conn:
                    conn.close()

        ttk.Button(win, text="Сохранить", command=save).pack(pady=10)

    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите клиента")
            return

        values = self.tree.item(selected[0], "values")
        client_id = int(values[0])

        win = tk.Toplevel(self.parent)
        win.title("Редактирование клиента")
        win.geometry("400x340")
        win.transient(self.parent)
        win.grab_set()
        win.configure(bg="#ffffff")

        tk.Label(
            win,
            text="Редактирование клиента",
            font=("Helvetica", 13, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(pady=(14, 12))
        form = tk.Frame(win, bg="#ffffff")
        form.pack(padx=20, fill="x")

        tk.Label(form, text="ФИО", bg="#ffffff", anchor="w").pack(fill="x")
        name = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        name.insert(0, values[1])
        name.pack(pady=(4, 10), ipady=4)

        tk.Label(form, text="Телефон", bg="#ffffff", anchor="w").pack(fill="x")
        phone = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        phone.insert(0, values[2])
        phone.pack(pady=(4, 10), ipady=4)

        tk.Label(form, text="Email", bg="#ffffff", anchor="w").pack(fill="x")
        email = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        email.insert(0, values[3])
        email.pack(pady=(4, 10), ipady=4)

        def update():
            full_name = name.get().strip()
            phone_value = phone.get().strip()
            email_value = email.get().strip()

            if not self.validate_client_data(full_name, phone_value, email_value):
                return

            if not messagebox.askyesno("Подтверждение", "Сохранить изменения?"):
                return

            conn = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    UPDATE clients
                    SET full_name = ?, phone = ?, email = ?
                    WHERE id = ?
                """,
                    (full_name, phone_value, email_value, client_id),
                )
                conn.commit()
                win.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror("Ошибка обновления", f"Не удалось обновить: {e}")
            finally:
                if conn:
                    conn.close()

        ttk.Button(win, text="Сохранить изменения", command=update).pack(pady=10)

    def delete_client(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите клиента")
            return

        values = self.tree.item(selected[0], "values")
        client_id = int(values[0])

        if not messagebox.askyesno(
            "Подтверждение", "Вы действительно хотите удалить клиента?"
        ):
            return

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM sessions WHERE client_id = ?", (client_id,)
            )
            if cur.fetchone()[0] > 0:
                messagebox.showerror(
                    "Ошибка удаления",
                    "Нельзя удалить клиента, так как он привязан к сессиям тренировок",
                )
                return

            cur.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            conn.commit()
            self.load()
        except Exception as e:
            messagebox.showerror("Ошибка удаления", f"Сбой операции: {e}")
        finally:
            if conn:
                conn.close()
