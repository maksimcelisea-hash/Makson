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

def run_optimized_voting(votes_count=200):
    """Вычислительный эксперимент: пакетная запись голосов одной транзакцией"""
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    start_time = time.time()
    
    # Открываем транзакцию вручную — данные будут копиться в оперативной памяти
    cursor.execute("BEGIN TRANSACTION;")
    
    for i in range(votes_count):
        cursor.execute(
            "INSERT INTO votes (poll_id, candidate_id, voter_hash, timestamp) VALUES (?, ?, ?, ?)",
            (5, 1, f"hash_user_{i}", time.time())
        )
        
    # Один финальный commit на весь пакет из 200 голосов
    conn.commit() 
    
    duration = time.time() - start_time
    conn.close()
    print(f"[Версия 2.0] Приложение голосования. Обработано {votes_count} голосов.")
    print(f"[Версия 2.0] Время выполнения (с транзакцией): {duration:.4f} сек.")
    return duration

if __name__ == "__main__":
    # Сбрасываем старую БД перед тестом
    if os.path.exists('voting_system.db'):
        os.remove('voting_system.db')
        
    init_db()
    run_optimized_voting()
