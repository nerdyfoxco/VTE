from sqlalchemy.orm import Session
from vte.db import SessionLocal, engine
from vte.orm import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_admin():
    db = SessionLocal()
    try:
        # Check if exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin already exists.")
            return

        print("Seeding Admin User...")
        hashed_password = pwd_context.hash("admin123")
        new_user = User(
            username="admin",
            email="admin@vte.example.com",
            hashed_password=hashed_password,
            role="admin",
            is_active=True
        )
        db.add(new_user)
        db.commit()
        print("Admin Seeded (admin/admin123).")
    except Exception as e:
        print(f"Failed to seed admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
