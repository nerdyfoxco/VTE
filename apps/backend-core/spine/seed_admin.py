from spine.db.engine import SessionLocal
from spine.db.models import DBUser
from spine.core.security import SecurityService

db = SessionLocal()

# Check if user exists
if not db.query(DBUser).filter_by(username="admin").first():
    print("Seeding Admin User...")
    admin = DBUser(
        username="admin",
        password_hash=SecurityService.get_password_hash("Admin@123456!"), # Meets complexity
        role="admin",
        tenant_id="system",
        email_verified=True,
        mfa_enabled=False
    )
    db.add(admin)
    db.commit()
    print("Admin Seeded.")
else:
    print("Admin already exists.")

db.close()
