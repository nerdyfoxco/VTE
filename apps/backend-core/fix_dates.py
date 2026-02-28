import sqlite3

def fix():
    conn = sqlite3.connect('vte_backend.db')
    cur = conn.cursor()
    cur.execute("UPDATE queue_items SET created_at = replace(created_at, ' ', 'T') || 'Z' WHERE created_at IS NOT NULL AND created_at NOT LIKE '%Z'")
    cur.execute("UPDATE queue_items SET sla_deadline = replace(sla_deadline, ' ', 'T') || 'Z' WHERE sla_deadline IS NOT NULL AND sla_deadline NOT LIKE '%Z'")
    conn.commit()
    conn.close()
    print("Dates fixed.")

if __name__ == '__main__':
    fix()
