import sqlite3
import time
import os

def init_db():
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER,
            candidate_id INTEGER,
            voter_hash TEXT,
            timestamp REAL
        )
    ''')
    conn.commit()
    conn.close()

def run_voting_experiment(votes_count):
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    start_time = time.time()
    
    for i in range(votes_count):
        cursor.execute(
            "INSERT INTO votes (poll_id, candidate_id, voter_hash, timestamp) VALUES (?, ?, ?, ?)",
            (5, 1, f"hash_user_{i}", time.time())
        )
        conn.commit() 
        
    duration = time.time() - start_time
    conn.close()
    print(f"\n[Версия 1.0] Успешно обработано {votes_count} голосов.")
    print(f"[Версия 1.0] Время выполнения (без оптимизации): {duration:.4f} сек.")
    return duration

def main():
    init_db()
    while True:
        print("\n========================================")
        print("  ПРИЛОЖЕНИЕ ГОЛОСОВАНИЯ [ВЕРСИЯ 1.0]   ")
        print("========================================")
        print("1. Запустить вычислительный эксперимент")
        print("2. Очистить базу данных")
        print("3. Выйти из программы")
        print("========================================")
        
        choice = input("Выберите действие (1-3): ").strip()
        
        if choice == '1':
            try:
                count = int(input("Введите количество голосов для генерации (например, 200): "))
                if count <= 0:
                    print("Количество голосов должно быть больше нуля!")
                    continue
                run_voting_experiment(count)
            except ValueError:
                print("Ошибка: введите корректное целое число!")
        
        elif choice == '2':
            if os.path.exists('voting_system.db'):
                try:
                    os.remove('voting_system.db')
                    init_db()
                    print("База данных успешно очищена и пересоздана.")
                except PermissionError:
                    print("Ошибка: файл БД заблокирован другой программой!")
            else:
                print("Файл базы данных не найден.")
                
        elif choice == '3':
            print("Завершение работы программы. До свидания!")
            break
        else:
            print("Неверный ввод! Пожалуйста, выберите пункт от 1 до 3.")

if __name__ == "__main__":
    main()
