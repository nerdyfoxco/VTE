import sqlite3
import uuid
from datetime import datetime

def seed_filter_data():
    conn = sqlite3.connect('C:\\Bintloop\\VTE\\apps\\backend-core\\vte_backend.db')
    cursor = conn.cursor()
    
    # Add COMPLETED Items
    print("Seeding COMPLETED items...")
    for i in range(3):
        item_id = str(uuid.uuid4())
        title = f"Completed Item {i+1}"
        priority = 1
        sla = datetime.utcnow()
        status = "COMPLETED"
        
        cursor.execute(
            "INSERT INTO queue_items (id, title, priority, sla_deadline, status) VALUES (?, ?, ?, ?, ?)",
            (item_id, title, priority, sla, status)
        )
    
    conn.commit()
    print("Seeding Done.")
    conn.close()

if __name__ == "__main__":
    seed_filter_data()
