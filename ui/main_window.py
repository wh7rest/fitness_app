import os
import tkinter as tk
from tkinter import messagebox, ttk

from ui.tabs.clients_tab import ClientsTab
from ui.tabs.services_tab import ServicesTab
from ui.tabs.sessions_tab import SessionsTab
from ui.tabs.trainers_tab import TrainersTab


class MainWindow:
    def __init__(self, current_user):
        self.current_user = current_user
        self.is_admin = current_user["role"] == "admin"

        self.root = tk.Tk()

        icon_path = os.path.abspath(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        self.root.title("Система учёта фитнес-клуба")
        self.root.geometry("1100x650")
        self.root.minsize(980, 580)
        self.root.configure(bg="#f3f4f6")

        self.setup_styles()
        self.build_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TNotebook", background="#f3f4f6", borderwidth=0)
        style.configure(
            "App.TNotebook.Tab",
            background="#e5e7eb",
            foreground="#111827",
            padding=(18, 10),
            font=("Helvetica", 10, "bold"),
            borderwidth=0,
        )
        style.map(
            "App.TNotebook.Tab",
            background=[("selected", "#ffffff"), ("active", "#dbeafe")],
            foreground=[("selected", "#2563eb"), ("active", "#111827")],
        )
        style.configure(
            "App.Treeview",
            background="#ffffff",
            foreground="#111827",
            fieldbackground="#ffffff",
            rowheight=32,
            font=("Helvetica", 10),
            borderwidth=0,
            relief="flat",
        )
        style.map(
            "App.Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", "#111827")],
        )
        style.configure(
            "App.Treeview.Heading",
            background="#f9fafb",
            foreground="#111827",
            font=("Helvetica", 10, "bold"),
            padding=8,
            borderwidth=0,
            relief="flat",
        )

    def build_layout(self):
        header_frame = tk.Frame(self.root, bg="#f3f4f6", height=90)
        header_frame.pack(fill="x", padx=18, pady=(16, 8))
        header_frame.pack_propagate(False)

        right_header = tk.Frame(header_frame, bg="#f3f4f6")
        right_header.pack(side="right", fill="y", pady=10)

        # Перевод кнопки на ttk.Button для фикса на Mac
        ttk.Button(
            right_header, text="О разработчике", command=self.open_about_window
        ).pack(side="right", padx=5, pady=5)

        role_text = "Администратор" if self.is_admin else "Клиент"

        tk.Label(
            header_frame,
            text="Система учёта фитнес-клуба",
            font=("Helvetica", 22, "bold"),
            fg="#111827",
            bg="#f3f4f6",
        ).pack(anchor="w", pady=(8, 2))

        tk.Label(
            header_frame,
            text=f"Пользователь: {self.current_user['username']} | Роль: {role_text}",
            font=("Helvetica", 10),
            fg="#6b7280",
            bg="#f3f4f6",
        ).pack(anchor="w")

        content_frame = tk.Frame(self.root, bg="#f3f4f6")
        content_frame.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        notebook = ttk.Notebook(content_frame, style="App.TNotebook")
        notebook.pack(fill="both", expand=True)

        if self.is_admin:
            clients_tab = ClientsTab(notebook)
            trainers_tab = TrainersTab(notebook)
            services_tab = ServicesTab(notebook, self.current_user)
            sessions_tab = SessionsTab(notebook, self.current_user)

            notebook.add(clients_tab.frame, text="Клиенты")
            notebook.add(trainers_tab.frame, text="Тренеры")
            notebook.add(services_tab.frame, text="Услуги")
            notebook.add(sessions_tab.frame, text="Сессии")
        else:
            services_tab = ServicesTab(notebook, self.current_user)
            sessions_tab = SessionsTab(notebook, self.current_user)

            notebook.add(services_tab.frame, text="Услуги")
            notebook.add(sessions_tab.frame, text="Покупка услуг")

    def open_about_window(self):
        win = tk.Toplevel(self.root)
        win.title("О разработчике")
        win.geometry("520x360")
        win.transient(self.root)
        win.grab_set()
        win.configure(bg="#ffffff")
        win.resizable(False, False)

        tk.Label(
            win,
            text="ПАСПОРТ ПРОЕКТА",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#1e40af",
        ).pack(pady=(20, 5))

        tk.Label(
            win,
            text="Итоговая экзаменационная работа",
            font=("Helvetica", 10, "italic"),
            bg="#ffffff",
            fg="#6b7280",
        ).pack(pady=(0, 15))

        info_frame = tk.Frame(win, bg="#ffffff")
        info_frame.pack(padx=35, fill="x")

        # Расширенный профессиональный академический шаблон данных
        labels = [
            ("Разработчик:", "Рихтер Егор Викторович"),
            ("Статус:", "Студент 1-го курса, группы 184518 (ИС-11)"),
            ("Специальность:", "09.02.07 Информационные системы и программирование"),
            ("Дисциплина:", "Основы Алгоритмизации и программирования"),
            ("Тема проекта:", "«Система учета клиентов и услуг фитнес-клуба»"),
            ("СУБД:", "SQLite3 (Реляционная база данных)"),
            ("Графический стек:", "Tkinter /ttk (Кроссплатформенный GUI)"),
            ("Год разработки:", "2026 год"),
        ]

        for idx, (key, value) in enumerate(labels):
            tk.Label(
                info_frame,
                text=key,
                font=("Helvetica", 10, "bold"),
                bg="#ffffff",
                fg="#374151",
                anchor="w",
            ).grid(row=idx, column=0, sticky="w", pady=4)
            # Включаем автоматический перенос длинных строк для названий тем и специальностей
            tk.Label(
                info_frame,
                text=value,
                font=("Helvetica", 10),
                bg="#ffffff",
                fg="#4b5563",
                anchor="w",
                wraplength=300,
                justify="left",
            ).grid(row=idx, column=1, sticky="w", padx=15, pady=4)

        ttk.Button(win, text="Закрыть окно", command=win.destroy).pack(pady=25)

    def run(self):
        self.root.mainloop()
