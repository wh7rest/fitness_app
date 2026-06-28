import tkinter as tk
from tkinter import messagebox, ttk

from db.database import get_connection


class TrainersTab:
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

        tk.Label(
            card,
            text="Тренеры",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#111827",
        ).pack(anchor="w", padx=16, pady=(14, 4))
        tk.Label(
            card,
            text="Управление данными тренеров фитнес-клуба",
            font=("Helvetica", 9),
            bg="#ffffff",
            fg="#6b7280",
        ).pack(anchor="w", padx=16, pady=(0, 4))

        self.count_label = tk.Label(
            card,
            text="Всего тренеров: 0",
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
        ttk.Button(
            btn_frame, text="Добавить тренера", command=self.open_add_window
        ).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Изменить", command=self.open_edit_window).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Удалить тренера", command=self.delete_trainer).pack(
            side="left", padx=4
        )

        table_frame = tk.Frame(card, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.tree = ttk.Treeview(
            table_frame,
            style="App.Treeview",
            columns=("id", "name", "spec", "phone"),
            show="headings",
            height=15,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("spec", text="Специализация")
        self.tree.heading("phone", text="Телефон")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=260)
        self.tree.column("spec", width=220)
        self.tree.column("phone", width=140)

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
                "SELECT id, full_name, specialization, phone FROM trainers ORDER BY full_name"
            )
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row["id"],
                        row["full_name"],
                        row["specialization"],
                        row["phone"],
                    ),
                )
            self.count_label.config(text=f"Всего тренеров: {len(rows)}")
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось загрузить данные: {e}")
        finally:
            if conn:
                conn.close()

    def open_add_window(self):
        win = tk.Toplevel(self.parent)
        win.title("Добавление тренера")
        win.geometry("400x320")
        win.transient(self.parent)
        win.grab_set()
        win.configure(bg="#ffffff")

        tk.Label(
            win,
            text="Добавление тренера",
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

        tk.Label(form, text="Специализация", bg="#ffffff", anchor="w").pack(fill="x")
        spec = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        spec.pack(pady=(4, 10), ipady=4)

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

        def save():
            full_name = name.get().strip()
            specialization = spec.get().strip()
            phone_value = phone.get().strip()

            if not full_name:
                messagebox.showerror("Ошибка ввода", "Поле ФИО обязательно")
                return

            conn = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO trainers (full_name, specialization, phone) VALUES (?, ?, ?)",
                    (full_name, specialization, phone_value),
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
            messagebox.showwarning("Предупреждение", "Выберите тренера")
            return

        values = self.tree.item(selected[0], "values")
        trainer_id = int(values[0])

        win = tk.Toplevel(self.parent)
        win.title("Редактирование тренера")
        win.geometry("400x320")
        win.transient(self.parent)
        win.grab_set()
        win.configure(bg="#ffffff")

        tk.Label(
            win,
            text="Редактирование тренера",
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

        tk.Label(form, text="Специализация", bg="#ffffff", anchor="w").pack(fill="x")
        spec = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        spec.insert(0, values[2])
        spec.pack(pady=(4, 10), ipady=4)

        tk.Label(form, text="Телефон", bg="#ffffff", anchor="w").pack(fill="x")
        phone = tk.Entry(
            form,
            width=38,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
        )
        phone.insert(0, values[3])
        phone.pack(pady=(4, 10), ipady=4)

        def update():
            full_name = name.get().strip()
            specialization = spec.get().strip()
            phone_value = phone.get().strip()

            if not full_name:
                messagebox.showerror("Ошибка ввода", "Поле ФИО обязательно")
                return

            if not messagebox.askyesno("Подтверждение", "Сохранить изменения?"):
                return

            conn = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "UPDATE trainers SET full_name = ?, specialization = ?, phone = ? WHERE id = ?",
                    (full_name, specialization, phone_value, trainer_id),
                )
                conn.commit()
                win.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось изменить данные: {e}")
            finally:
                if conn:
                    conn.close()

        ttk.Button(win, text="Сохранить изменения", command=update).pack(pady=10)

    def delete_trainer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тренера")
            return

        values = self.tree.item(selected[0], "values")
        trainer_id = int(values[0])

        if not messagebox.askyesno(
            "Подтверждение", "Вы действительно хотите удалить тренера?"
        ):
            return

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM sessions WHERE trainer_id = ?", (trainer_id,)
            )
            if cur.fetchone()[0] > 0:
                messagebox.showerror(
                    "Ошибка удаления",
                    "Нельзя удалить тренера, так как он привязан к активным сессиям",
                )
                return

            cur.execute("DELETE FROM trainers WHERE id = ?", (trainer_id,))
            conn.commit()
            self.load()
        except Exception as e:
            messagebox.showerror("Ошибка удаления", f"Сбой операции: {e}")
        finally:
            if conn:
                conn.close()
