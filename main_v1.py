# main_v1.py (Часть 1 из 2)
import sqlite3
import tkinter as tk
from tkinter import messagebox


def init_db_v1_add_only():
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


class SimpleAddWindow:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Приложение голосования (Целищев) - База данных v1.0")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        init_db_v1_add_only()

        tk.Label(self.root, text="Регистрация нового голосования (Версия 1):", font=("Arial", 11, "bold")).pack(pady=10)

        tk.Label(self.root, text="Тема / Название опроса:", font=("Arial", 10)).pack(pady=2)
        self.entry_title = tk.Entry(self.root, font=("Arial", 10), width=35)
        self.entry_title.pack(pady=2)

        tk.Label(self.root, text="Общее число избирателей в регионе:", font=("Arial", 10)).pack(pady=2)
        self.entry_pop = tk.Entry(self.root, font=("Arial", 10), width=35)
        self.entry_pop.pack(pady=2)
        # main_v1.py (Часть 2 из 2)
        tk.Button(self.root, text="Сохранить в базу данных", command=self.add_poll_to_db, bg="#4CAF50", fg="white",
                  font=("Arial", 10, "bold"), width=22).pack(pady=20)

    def add_poll_to_db(self):
        title = self.entry_title.get().strip()
        population_str = self.entry_pop.get().strip()

        if not title or not population_str:
            messagebox.showwarning("Внимание", "Заполните все доступные поля ввода!")
            return

        try:
            population = int(population_str)
            if population <= 0:
                raise ValueError

            conn = sqlite3.connect('voting_system.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO polls (title, candidate_a, votes_a, candidate_b, votes_b, total_population) 
                VALUES (?, 'Кандидат 1', 0, 'Кандидат 2', 0, ?)
            """, (title, population))
            conn.commit()
            conn.close()

            self.entry_title.delete(0, tk.END)
            self.entry_pop.delete(0, tk.END)
            messagebox.showinfo("Успех", "Голосование успешно добавлено в базу данных!")

        except ValueError:
            messagebox.showerror("Ошибка ввода", "Число избирателей должно быть целым положительным числом!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleAddWindow(root)
    root.mainloop()
