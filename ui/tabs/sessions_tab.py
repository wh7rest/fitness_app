import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from db.database import get_connection


class SessionsTab:
    def __init__(self, parent, current_user):
        self.parent = parent
        self.current_user = current_user
        self.is_admin = current_user["role"] == "admin"

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

        title_text = "Сессии" if self.is_admin else "Покупка услуг"
        tk.Label(
            card,
            text=title_text,
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(anchor="w", padx=16, pady=(14, 4))

        subtitle_text = (
            "Связи между клиентами, тренерами, услугами и датой проведения"
            if self.is_admin
            else "Выберите услугу и оформите тренировочную сессию"
        )
        tk.Label(
            card, text=subtitle_text, font=("Helvetica", 9), bg="#ffffff", fg="#6b7280"
        ).pack(anchor="w", padx=16, pady=(0, 4))

        self.count_label = tk.Label(
            card,
            text="Всего сессий: 0",
            font=("Helvetica", 9),
            bg="#ffffff",
            fg="#6b7280",
        )
        self.count_label.pack(anchor="w", padx=16, pady=(0, 10))

        btn_frame = tk.Frame(card, bg="#ffffff")
        btn_frame.pack(fill="x", padx=16, pady=(0, 10))

        ttk.Button(btn_frame, text="Обновить", command=self.load).pack(
            side="left", padx=4
        )

        if self.is_admin:
            ttk.Button(
                btn_frame, text="Добавить сессию", command=self.open_add_window
            ).pack(side="left", padx=4)
            ttk.Button(btn_frame, text="Изменить", command=self.open_edit_window).pack(
                side="left", padx=4
            )
            ttk.Button(
                btn_frame, text="Удалить сессию", command=self.delete_session
            ).pack(side="left", padx=4)
        else:
            ttk.Button(
                btn_frame, text="Купить услугу", command=self.open_purchase_window
            ).pack(side="left", padx=4)

        table_frame = tk.Frame(card, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.tree = ttk.Treeview(
            table_frame,
            style="App.Treeview",
            columns=("id", "client", "trainer", "service", "date"),
            show="headings",
            height=15,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("client", text="Клиент")
        self.tree.heading("trainer", text="Тренер")
        self.tree.heading("service", text="Услуга")
        self.tree.heading("date", text="Дата")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("client", width=220)
        self.tree.column("trainer", width=220)
        self.tree.column("service", width=220)
        self.tree.column("date", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if self.is_admin:
            self.tree.bind("<Double-1>", lambda event: self.open_edit_window())

        self.load()

    def load(self):
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            if self.is_admin:
                cur.execute("""
                    SELECT s.id, c.full_name AS c_name, t.full_name AS t_name, sv.name AS s_name, s.session_date
                    FROM sessions s
                    JOIN clients c ON s.client_id = c.id
                    JOIN trainers t ON s.trainer_id = t.id
                    JOIN services sv ON s.service_id = sv.id
                    ORDER BY s.session_date DESC, s.id DESC
                """)
            else:
                cur.execute(
                    """
                    SELECT s.id, c.full_name AS c_name, t.full_name AS t_name, sv.name AS s_name, s.session_date
                    FROM sessions s
                    JOIN clients c ON s.client_id = c.id
                    JOIN trainers t ON s.trainer_id = t.id
                    JOIN services sv ON s.service_id = sv.id
                    WHERE c.email = ?
                    ORDER BY s.session_date DESC, s.id DESC
                """,
                    (self.current_user["username"],),
                )

            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row["id"],
                        row["c_name"],
                        row["t_name"],
                        row["s_name"],
                        row["session_date"],
                    ),
                )

            self.count_label.config(
                text=f"Всего сессий: {len(rows)}"
                if self.is_admin
                else f"Мои покупки: {len(rows)}"
            )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить таблицу: {e}")
        finally:
            if conn:
                conn.close()

    def is_valid_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def open_purchase_window(self):
        win = tk.Toplevel(self.parent)
        win.title("Покупка услуги")
        win.geometry("440x380")
        win.transient(self.parent)
        win.grab_set()
        win.configure(bg="#ffffff")

        tk.Label(
            win,
            text="Покупка услуги",
            font=("Helvetica", 13, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(pady=(14, 12))

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT id, full_name FROM clients WHERE email = ?",
                (self.current_user["username"],),
            )
            client = cur.fetchone()

            if not client:
                cur.execute(
                    "INSERT INTO clients (full_name, phone, email, membership_start, membership_end) VALUES (?, ?, ?, DATE('now'), DATE('now','+1 year'))",
                    (self.current_user["username"], "", self.current_user["username"]),
                )
                conn.commit()
                cur.execute(
                    "SELECT id, full_name FROM clients WHERE email = ?",
                    (self.current_user["username"],),
                )
                client = cur.fetchone()

            cur.execute("SELECT id, full_name FROM trainers ORDER BY full_name")
            trainers = cur.fetchall()
            cur.execute("SELECT id, name, price, duration FROM services ORDER BY name")
            services = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить списки: {e}")
            win.destroy()
            return
        finally:
            if conn:
                conn.close()

        form = tk.Frame(win, bg="#ffffff")
        form.pack(padx=20, fill="x")

        tk.Label(form, text="Клиент", bg="#ffffff", anchor="w").pack(fill="x")
        client_entry = tk.Entry(
            form, width=41, font=("Helvetica", 10), bg="#ffffff", fg="#000000"
        )
        client_entry.insert(0, client["full_name"])
        client_entry.config(state="disabled")
        client_entry.pack(pady=(4, 10), ipady=4)

        tk.Label(form, text="Тренер", bg="#ffffff", anchor="w").pack(fill="x")
        trainer_combo = ttk.Combobox(
            form,
            state="readonly",
            width=38,
            values=[f"{row['id']} - {row['full_name']}" for row in trainers],
        )
        trainer_combo.pack(pady=(4, 10))

        tk.Label(form, text="Услуга", bg="#ffffff", anchor="w").pack(fill="x")
        service_combo = ttk.Combobox(
            form,
            state="readonly",
            width=38,
            values=[
                f"{row['id']} - {row['name']} | {row['price']} руб." for row in services
            ],
        )
        service_combo.pack(pady=(4, 10))

        tk.Label(form, text="Дата (ГГГГ-ММ-ДД)", bg="#ffffff", anchor="w").pack(
            fill="x"
        )
        date_entry = tk.Entry(
            form,
            width=41,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=(4, 10), ipady=4)

        def purchase():
            if (
                not trainer_combo.get()
                or not service_combo.get()
                or not date_entry.get().strip()
            ):
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return

            client_id = int(client["id"])
            trainer_id = int(trainer_combo.get().split(" - ")[0])
            service_id = int(service_combo.get().split(" - ")[0])
            session_date = date_entry.get().strip()

            if not self.is_valid_date(session_date):
                messagebox.showerror("Ошибка даты", "Формат даты: ГГГГ-ММ-ДД")
                return

            db_conn = None
            try:
                db_conn = get_connection()
                db_cur = db_conn.cursor()
                db_cur.execute(
                    "SELECT COUNT(*) FROM sessions WHERE client_id = ? AND trainer_id = ? AND service_id = ? AND session_date = ?",
                    (client_id, trainer_id, service_id, session_date),
                )
                if db_cur.fetchone()[0] > 0:
                    messagebox.showerror("Ошибка", "Такая покупка уже оформлена")
                    return

                db_cur.execute(
                    "INSERT INTO sessions (client_id, trainer_id, service_id, session_date) VALUES (?, ?, ?, ?)",
                    (client_id, trainer_id, service_id, session_date),
                )
                db_conn.commit()
                messagebox.showinfo("Успешно", "Услуга успешно приобретена")
                win.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror(
                    "Ошибка транзакции", f"Не удалось завершить операцию: {e}"
                )
            finally:
                if db_conn:
                    db_conn.close()

        # Кнопка перенесена внутрь form для корректного расчета высоты на macOS
        ttk.Button(form, text="Купить", command=purchase).pack(pady=15)

    def open_add_window(self):
        win = tk.Toplevel(self.parent)
        win.title("Добавление сессии")
        win.geometry("440x420")
        win.transient(self.parent)
        win.grab_set()
        win.configure(bg="#ffffff")

        tk.Label(
            win,
            text="Добавление сессии",
            font=("Helvetica", 13, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(pady=(14, 12))

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, full_name FROM clients ORDER BY full_name")
            clients = cur.fetchall()
            cur.execute("SELECT id, full_name FROM trainers ORDER BY full_name")
            trainers = cur.fetchall()
            cur.execute("SELECT id, name FROM services ORDER BY name")
            services = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные СУБД: {e}")
            win.destroy()
            return
        finally:
            if conn:
                conn.close()

        form = tk.Frame(win, bg="#ffffff")
        form.pack(padx=20, fill="x")

        tk.Label(form, text="Клиент", bg="#ffffff", anchor="w").pack(fill="x")
        client_combo = ttk.Combobox(
            form,
            state="readonly",
            width=38,
            values=[f"{row['id']} - {row['full_name']}" for row in clients],
        )
        client_combo.pack(pady=(4, 10))

        tk.Label(form, text="Тренер", bg="#ffffff", anchor="w").pack(fill="x")
        trainer_combo = ttk.Combobox(
            form,
            state="readonly",
            width=38,
            values=[f"{row['id']} - {row['full_name']}" for row in trainers],
        )
        trainer_combo.pack(pady=(4, 10))

        tk.Label(form, text="Услуга", bg="#ffffff", anchor="w").pack(fill="x")
        service_combo = ttk.Combobox(
            form,
            state="readonly",
            width=38,
            values=[f"{row['id']} - {row['name']}" for row in services],
        )
        service_combo.pack(pady=(4, 10))

        tk.Label(form, text="Дата (ГГГГ-ММ-ДД)", bg="#ffffff", anchor="w").pack(
            fill="x"
        )
        date_entry = tk.Entry(
            form,
            width=41,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        date_entry.pack(pady=(4, 10), ipady=4)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def save():
            if (
                not client_combo.get()
                or not trainer_combo.get()
                or not service_combo.get()
                or not date_entry.get().strip()
            ):
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return

            client_id = int(client_combo.get().split(" - ")[0])
            trainer_id = int(trainer_combo.get().split(" - ")[0])
            service_id = int(service_combo.get().split(" - ")[0])
            session_date = date_entry.get().strip()

            if not self.is_valid_date(session_date):
                messagebox.showerror("Ошибка даты", "Формат даты: ГГГГ-ММ-ДД")
                return

            db_conn = None
            try:
                db_conn = get_connection()
                db_cur = db_conn.cursor()
                db_cur.execute(
                    "SELECT COUNT(*) FROM sessions WHERE client_id = ? AND trainer_id = ? AND service_id = ? AND session_date = ?",
                    (client_id, trainer_id, service_id, session_date),
                )
                if db_cur.fetchone()[0] > 0:
                    messagebox.showerror("Ошибка", "Такая сессия уже назначена")
                    return

                db_cur.execute(
                    "INSERT INTO sessions (client_id, trainer_id, service_id, session_date) VALUES (?, ?, ?, ?)",
                    (client_id, trainer_id, service_id, session_date),
                )
                db_conn.commit()
                win.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror("Ошибка сохранения", f"Сбой операции: {e}")
            finally:
                if db_conn:
                    db_conn.close()

        ttk.Button(form, text="Сохранить", command=save).pack(pady=15)

    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сессию")
            return

        values = self.tree.item(selected[0], "values")
        session_id = int(values[0])
        current_client = values[1]
        current_trainer = values[2]
        current_service = values[3]
        current_date = values[4]

        win = tk.Toplevel(self.parent)
        win.title("Редактирование сессии")
        win.geometry("440x420")
        win.transient(self.parent)
        win.grab_set()
        win.configure(bg="#ffffff")

        tk.Label(
            win,
            text="Редактирование сессии",
            font=("Helvetica", 13, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(pady=(14, 12))

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, full_name FROM clients ORDER BY full_name")
            clients = cur.fetchall()
            cur.execute("SELECT id, full_name FROM trainers ORDER BY full_name")
            trainers = cur.fetchall()
            cur.execute("SELECT id, name FROM services ORDER BY name")
            services = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные СУБД: {e}")
            win.destroy()
            return
        finally:
            if conn:
                conn.close()

        client_values = [f"{row['id']} - {row['full_name']}" for row in clients]
        trainer_values = [f"{row['id']} - {row['full_name']}" for row in trainers]
        service_values = [f"{row['id']} - {row['name']}" for row in services]

        form = tk.Frame(win, bg="#ffffff")
        form.pack(padx=20, fill="x")

        tk.Label(form, text="Клиент", bg="#ffffff", anchor="w").pack(fill="x")
        client_combo = ttk.Combobox(
            form, state="readonly", width=38, values=client_values
        )
        client_combo.pack(pady=(4, 10))

        tk.Label(form, text="Тренер", bg="#ffffff", anchor="w").pack(fill="x")
        trainer_combo = ttk.Combobox(
            form, state="readonly", width=38, values=trainer_values
        )
        trainer_combo.pack(pady=(4, 10))

        tk.Label(form, text="Услуга", bg="#ffffff", anchor="w").pack(fill="x")
        service_combo = ttk.Combobox(
            form, state="readonly", width=38, values=service_values
        )
        service_combo.pack(pady=(4, 10))

        tk.Label(form, text="Дата (ГГГГ-ММ-ДД)", bg="#ffffff", anchor="w").pack(
            fill="x"
        )
        date_entry = tk.Entry(
            form,
            width=41,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        date_entry.pack(pady=(4, 10), ipady=4)
        date_entry.insert(0, current_date)

        for item in client_values:
            if item.endswith(current_client):
                client_combo.set(item)
                break
        for item in trainer_values:
            if item.endswith(current_trainer):
                trainer_combo.set(item)
                break
        for item in service_values:
            if item.endswith(current_service):
                service_combo.set(item)
                break

        def update():
            if (
                not client_combo.get()
                or not trainer_combo.get()
                or not service_combo.get()
                or not date_entry.get().strip()
            ):
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return

            client_id = int(client_combo.get().split(" - ")[0])
            trainer_id = int(trainer_combo.get().split(" - ")[0])
            service_id = int(service_combo.get().split(" - ")[0])
            session_date = date_entry.get().strip()

            if not self.is_valid_date(session_date):
                messagebox.showerror("Ошибка даты", "Формат даты: ГГГГ-ММ-ДД")
                return

            if not messagebox.askyesno("Подтверждение", "Сохранить изменения?"):
                return

            db_conn = None
            try:
                db_conn = get_connection()
                db_cur = db_conn.cursor()
                db_cur.execute(
                    "SELECT COUNT(*) FROM sessions WHERE client_id = ? AND trainer_id = ? AND service_id = ? AND session_date = ? AND id != ?",
                    (client_id, trainer_id, service_id, session_date, session_id),
                )
                if db_cur.fetchone()[0] > 0:
                    messagebox.showerror("Ошибка", "Такая сессия уже существует")
                    return

                db_cur.execute(
                    "UPDATE sessions SET client_id = ?, trainer_id = ?, service_id = ?, session_date = ? WHERE id = ?",
                    (client_id, trainer_id, service_id, session_date, session_id),
                )
                db_conn.commit()
                win.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror("Ошибка обновления", f"Сбой операции: {e}")
            finally:
                if db_conn:
                    db_conn.close()

        ttk.Button(form, text="Сохранить изменения", command=update).pack(pady=15)

    def delete_session(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сессию")
            return

        values = self.tree.item(selected[0], "values")
        session_id = int(values[0])

        if not messagebox.askyesno(
            "Подтверждение", "Вы действительно хотите удалить сессию?"
        ):
            return

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            conn.commit()
            self.load()
        except Exception as e:
            messagebox.showerror("Ошибка удаления", f"Сбой СУБД: {e}")
        finally:
            if conn:
                conn.close()
