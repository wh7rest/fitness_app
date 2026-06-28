import tkinter as tk
from tkinter import messagebox, ttk

from db.database import get_connection


class ServicesTab:
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

        title_text = "Услуги" if self.is_admin else "Доступные услуги"
        tk.Label(
            card,
            text=title_text,
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(anchor="w", padx=16, pady=(14, 4))

        subtitle_text = (
            "Управление услугами, ценой и длительностью"
            if self.is_admin
            else "Просмотр доступных услуг фитнес-клуба"
        )
        tk.Label(
            card, text=subtitle_text, font=("Helvetica", 9), bg="#ffffff", fg="#6b7280"
        ).pack(anchor="w", padx=16, pady=(0, 4))

        self.count_label = tk.Label(
            card,
            text="Всего услуг: 0",
            font=("Helvetica", 9),
            bg="#ffffff",
            fg="#6b7280",
        )
        self.count_label.pack(anchor="w", padx=16, pady=(0, 10))

        btn_frame = tk.Frame(card, bg="#ffffff")
        btn_frame.pack(fill="x", padx=16, pady=(0, 10))

        # Перевод кнопок на ttk.Button
        ttk.Button(btn_frame, text="Обновить", command=self.load).pack(
            side="left", padx=4
        )

        if self.is_admin:
            ttk.Button(
                btn_frame, text="Добавить услугу", command=self.open_add_window
            ).pack(side="left", padx=4)
            ttk.Button(btn_frame, text="Изменить", command=self.open_edit_window).pack(
                side="left", padx=4
            )
            ttk.Button(
                btn_frame, text="Удалить услугу", command=self.delete_service
            ).pack(side="left", padx=4)

        table_frame = tk.Frame(card, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.tree = ttk.Treeview(
            table_frame,
            style="App.Treeview",
            columns=("id", "name", "price", "duration"),
            show="headings",
            height=15,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название услуги")
        self.tree.heading("price", text="Цена")
        self.tree.heading("duration", text="Длительность (мин)")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=300)
        self.tree.column("price", width=120, anchor="center")
        self.tree.column("duration", width=150, anchor="center")

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
            cur.execute("SELECT id, name, price, duration FROM services ORDER BY name")
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert(
                    "", "end", values=(r["id"], r["name"], r["price"], r["duration"])
                )
            self.count_label.config(text=f"Всего услуг: {len(rows)}")
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось загрузить данные: {e}")
        finally:
            if conn:
                conn.close()

    def validate_service_data(self, name, price, duration):
        if not name.strip():
            messagebox.showerror("Ошибка ввода", "Название услуги обязательно")
            return False
        try:
            if float(price) < 0:
                messagebox.showerror("Ошибка ввода", "Цена не может быть отрицательной")
                return False
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Цена должна быть числом")
            return False
        try:
            if int(duration) <= 0:
                messagebox.showerror(
                    "Ошибка ввода", "Длительность должна быть больше 0"
                )
                return False
        except ValueError:
            messagebox.showerror(
                "Ошибка ввода", "Длительность должна быть целым числом"
            )
            return False
        return True

    def open_add_window(self):
        win = tk.Toplevel(self.parent)
        win.title("Добавление услуги")
        win.geometry("400x320")
        win.transient(self.parent)
        win.grab_set()
        win.configure(bg="#ffffff")

        tk.Label(
            win,
            text="Добавление услуги",
            font=("Helvetica", 13, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(pady=(14, 12))
        form = tk.Frame(win, bg="#ffffff")
        form.pack(padx=20, fill="x")

        tk.Label(form, text="Название услуги", bg="#ffffff", anchor="w").pack(fill="x")
        name = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        name.pack(pady=(4, 10), ipady=4)

        tk.Label(form, text="Цена", bg="#ffffff", anchor="w").pack(fill="x")
        price = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        price.pack(pady=(4, 10), ipady=4)

        tk.Label(form, text="Длительность (мин)", bg="#ffffff", anchor="w").pack(
            fill="x"
        )
        duration = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        duration.pack(pady=(4, 10), ipady=4)

        def save():
            service_name = name.get().strip()
            price_value = price.get().strip()
            duration_value = duration.get().strip()

            if not self.validate_service_data(
                service_name, price_value, duration_value
            ):
                return

            conn = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO services (name, price, duration) VALUES (?, ?, ?)",
                    (service_name, float(price_value), int(duration_value)),
                )
                conn.commit()
                win.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
            finally:
                if conn:
                    conn.close()

        ttk.Button(win, text="Сохранить", command=save).pack(pady=10)

    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите услугу")
            return

        values = self.tree.item(selected[0], "values")
        service_id = int(values[0])

        win = tk.Toplevel(self.parent)
        win.title("Редактирование услуги")
        win.geometry("400x320")
        win.transient(self.parent)
        win.grab_set()
        win.configure(bg="#ffffff")

        tk.Label(
            win,
            text="Редактирование услуги",
            font=("Helvetica", 13, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(pady=(14, 12))
        form = tk.Frame(win, bg="#ffffff")
        form.pack(padx=20, fill="x")

        tk.Label(form, text="Название услуги", bg="#ffffff", anchor="w").pack(fill="x")
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

        tk.Label(form, text="Цена", bg="#ffffff", anchor="w").pack(fill="x")
        price = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        price.insert(0, values[2])
        price.pack(pady=(4, 10), ipady=4)

        tk.Label(form, text="Длительность (мин)", bg="#ffffff", anchor="w").pack(
            fill="x"
        )
        duration = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        duration.insert(0, values[3])
        duration.pack(pady=(4, 10), ipady=4)

        def update():
            service_name = name.get().strip()
            price_value = price.get().strip()
            duration_value = duration.get().strip()

            if not self.validate_service_data(
                service_name, price_value, duration_value
            ):
                return

            if not messagebox.askyesno("Подтверждение", "Сохранить изменения?"):
                return

            conn = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "UPDATE services SET name = ?, price = ?, duration = ? WHERE id = ?",
                    (service_name, float(price_value), int(duration_value), service_id),
                )
                conn.commit()
                win.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить: {e}")
            finally:
                if conn:
                    conn.close()

        ttk.Button(win, text="Сохранить изменения", command=update).pack(pady=10)

    def delete_service(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите услугу")
            return

        values = self.tree.item(selected[0], "values")
        service_id = int(values[0])

        if not messagebox.askyesno(
            "Подтверждение", "Вы действительно хотите удалить услугу?"
        ):
            return

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM sessions WHERE service_id = ?", (service_id,)
            )
            if cur.fetchone()[0] > 0:
                messagebox.showerror(
                    "Ошибка удаления",
                    "Нельзя удалить услугу, так как она используется в сессиях",
                )
                return

            cur.execute("DELETE FROM services WHERE id = ?", (service_id,))
            conn.commit()
            self.load()
        except Exception as e:
            messagebox.showerror("Ошибка удаления", f"Сбой операции: {e}")
        finally:
            if conn:
                conn.close()
