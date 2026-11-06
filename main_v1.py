import sqlite3
import time

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

def run_voting_experiment(votes_count=200):
   
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
    print(f"[Версия 1.0] Приложение голосования. Обработано {votes_count} голосов.")
    print(f"[Версия 1.0] Время выполнения (без оптимизации): {duration:.4f} сек.")
    return duration

if __name__ == "__main__":
    init_db()
    run_voting_experiment()
