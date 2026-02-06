import shutil
import os
from datetime import datetime
from spine.db.engine import SQLALCHEMY_DATABASE_URL

def backup_db(backup_dir="backups", retention_days=7):
    """
    Gap 106: Local Backup Strategy.
    Snapshots the SQLite DB to a local backup folder.
    """
    if "sqlite" not in SQLALCHEMY_DATABASE_URL:
        print("Skipping local backup: Not using SQLite.")
        return

    # Extract path from URL (remove sqlite:///)
    db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"vte_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)

    print(f"Backing up {db_path} to {backup_path}...")
    try:
        shutil.copy2(db_path, backup_path)
        print("Backup successful.")
    except Exception as e:
        print(f"Backup failed: {e}")
        return

    # Rotation Policy (Gap 113 Partial)
    print("Running rotation policy...")
    for f in os.listdir(backup_dir):
        f_path = os.path.join(backup_dir, f)
        if os.path.isfile(f_path) and f.startswith("vte_backup_"):
            # Check age
            file_time = datetime.fromtimestamp(os.path.getmtime(f_path))
            age_days = (datetime.now() - file_time).days
            if age_days > retention_days:
                print(f"Deleting old backup: {f} ({age_days} days old)")
                os.remove(f_path)

if __name__ == "__main__":
    backup_db()
