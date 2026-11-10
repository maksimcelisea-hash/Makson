import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import math


def init_db_v2():
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS polls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            candidate_a TEXT NOT NULL,
            votes_a INTEGER NOT NULL,
            candidate_b TEXT NOT NULL,
            votes_b INTEGER NOT NULL,
            total_population INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


class MainWindow:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Приложение голосования (Целищев) - Панель Администратора v2.0")
        self.root.geometry("800x580")

        init_db_v2()

        input_frame = tk.LabelFrame(self.root, text=" Регистрация нового голосования ", font=("Arial", 10, "bold"),
                                    padx=10, pady=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(input_frame, text="Тема опроса:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.ent_title = tk.Entry(input_frame, width=25)
        self.ent_title.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Всего избирателей в регионе:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.ent_pop = tk.Entry(input_frame, width=15)
        self.ent_pop.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Кандидат 1 (Имя):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.ent_cand_a = tk.Entry(input_frame, width=25)
        self.ent_cand_a.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Голосов за Кандидата 1:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.ent_votes_a = tk.Entry(input_frame, width=15)
        self.ent_votes_a.grid(row=1, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Кандидат 2 (Имя):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.ent_cand_b = tk.Entry(input_frame, width=25)
        self.ent_cand_b.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Голосов за Кандидата 2:").grid(row=2, column=2, sticky="w", padx=5, pady=2)
        self.ent_votes_b = tk.Entry(input_frame, width=15)
        self.ent_votes_b.grid(row=2, column=3, padx=5, pady=2)

        tk.Button(input_frame, text="Сохранить голосование в БД", command=self.save_poll, bg="#2196F3", fg="white",
                  font=("Arial", 9, "bold")).grid(row=3, column=0, columnspan=4, pady=8)

        tk.Label(self.root, text="Архив проведенных голосований:", font=("Arial", 10, "bold")).pack(anchor="w", padx=15)

        self.table = ttk.Treeview(self.root, columns=("id", "title", "cand_a", "v_a", "cand_b", "v_b", "pop"),
                                  show="headings", height=6)
        self.table.heading("id", text="ID")
        self.table.heading("title", text="Тема опроса")
        self.table.heading("cand_a", text="Кандидат 1")
        self.table.heading("v_a", text="Голоса 1")
        self.table.heading("cand_b", text="Кандидат 2")
        self.table.heading("v_b", text="Голоса 2")
        self.table.heading("pop", text="Всего граждан")

        self.table.column("id", width=40, anchor="center")
        self.table.column("v_a", width=70, anchor="center")
        self.table.column("v_b", width=70, anchor="center")
        self.table.column("pop", width=100, anchor="center")
        self.table.pack(fill="x", padx=15, pady=5)
        experiment_frame = tk.LabelFrame(self.root,
                                         text=" Вычислительный эксперимент (Оценка погрешности результатов) ",
                                         font=("Arial", 10, "bold"), fg="darkblue", padx=10, pady=10)
        experiment_frame.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Label(experiment_frame, text="Шаг 1: Выберите строку голосования в таблице выше",
                 font=("Arial", 9, "italic"), fg="gray").pack(anchor="w")

        control_subframe = tk.Frame(experiment_frame)
        control_subframe.pack(fill="x", pady=5)

        tk.Button(control_subframe, text="Рассчитать математическую погрешность выборки",
                  command=self.run_voting_experiment, bg="#4CAF50", fg="white", font=("Arial", 9, "bold")).pack(
            side="left", pady=5)

        self.lbl_experiment_result = tk.Label(experiment_frame,
                                              text="Ожидание выбора данных для математического моделирования...",
                                              font=("Courier", 10), fg="gray", justify="left", anchor="w")
        self.lbl_experiment_result.pack(fill="both", expand=True, pady=10)

        self.update_table_data()

    def save_poll(self):
        try:
            title = self.ent_title.get().strip()
            cand_a = self.ent_cand_a.get().strip()
            cand_b = self.ent_cand_b.get().strip()
            v_a = int(self.ent_votes_a.get())
            v_b = int(self.ent_votes_b.get())
            pop = int(self.ent_pop.get())

            if not title or not cand_a or not cand_b or v_a < 0 or v_b < 0 or pop <= 0 or (v_a + v_b) > pop:
                raise ValueError

            conn = sqlite3.connect('voting_system.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO polls (title, candidate_a, votes_a, candidate_b, votes_b, total_population) VALUES (?, ?, ?, ?, ?, ?)",
                (title, cand_a, v_a, cand_b, v_b, pop))
            conn.commit()
            conn.close()

            self.update_table_data()
            messagebox.showinfo("Успех", "Данные голосования внесены в базу!")
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Проверьте поля! Число голосов не должно превышать общее население.")

    def update_table_data(self):
        for row in self.table.get_children():
            self.table.delete(row)
        conn = sqlite3.connect('voting_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM polls")
        for item in cursor.fetchall():
            self.table.insert("", "end", values=item)
        conn.close()

    def run_voting_experiment(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите запись из таблицы!")
            return

        db_row = self.table.item(selected)['values']
        poll_title = db_row[1]
        cand_a_name = db_row[2]
        v_a = int(db_row[3])
        cand_b_name = db_row[4]
        v_b = int(db_row[5])
        pop = int(db_row[6])

        sample_size = v_a + v_b
        if sample_size == 0:
            messagebox.showwarning("Внимание", "В данном голосовании еще никто не принял участие.")
            return

        turnout = (sample_size / pop) * 100
        share_a = (v_a / sample_size) * 100
        share_b = (v_b / sample_size) * 100

        p = v_a / sample_size
        z = 1.96
        margin_of_error = z * math.sqrt((p * (1 - p)) / sample_size) * 100

        if margin_of_error == 0:
            margin_of_error = 1.5

        if margin_of_error < 5.0 and turnout > 30:
            status_text = "ВЫСОКАЯ ЛЕГИТИМНОСТЬ. Выборка репрезентативна."
            text_color = "green"
        else:
            status_text = "НИЗКАЯ СТАБИЛЬНОСТЬ. Погрешность высока из-за малой явки."
            text_color = "red"

        report = (
            f"=== РЕЗУЛЬТАТЫ МАТЕМАТИЧЕСКОГО ЭКСПЕРИМЕНТА ===\n"
            f"Голосование: '{poll_title}'\n"
            f"Текущая явка избирателей: {turnout:.2f}% ({sample_size} из {pop} граждан)\n"
            f"Распределение: {cand_a_name} - {share_a:.1f}% | {cand_b_name} - {share_b:.1f}%\n"
            f"Статистическая погрешность (Margin of Error): ±{margin_of_error:.2f}%\n"
            f"АНАЛИЗ ДАННЫХ: {status_text}"
        )
        self.lbl_experiment_result.config(text=report, fg=text_color)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
