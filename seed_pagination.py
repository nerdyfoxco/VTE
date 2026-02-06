import sqlite3
import uuid
from datetime import datetime, timedelta

def seed_pagination_data():
    conn = sqlite3.connect('C:\\Bintloop\\VTE\\apps\\backend-core\\vte_backend.db')
    cursor = conn.cursor()
    
    # Check current count
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables found: {tables}")

        cursor.execute("SELECT COUNT(*) FROM queue_items")
        count = cursor.fetchone()[0]
        print(f"Current Row Count: {count}")
    except Exception as e:
        print(f"Error accessing DB: {e}")
        return
    
    if count < 15:
        to_add = 15 - count
        print(f"Adding {to_add} rows...")
        for i in range(to_add):
            item_id = str(uuid.uuid4())
            title = f"Pagination Test Item {i+1}"
            priority = (i % 3) + 1
            sla = datetime.utcnow() + timedelta(days=i)
            status = "PENDING"
            
            cursor.execute(
                "INSERT INTO queue_items (id, title, priority, sla_deadline, status) VALUES (?, ?, ?, ?, ?)",
                (item_id, title, priority, sla, status)
            )
        conn.commit()
        print("Seeding Complete.")
    else:
        print("Data sufficient.")
        
    conn.close()

if __name__ == "__main__":
    seed_pagination_data()
