from spine.db.engine import engine, SessionLocal, Base
from spine.db.models import DBQueueItem
from datetime import datetime, timedelta

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if we need to seed
    if db.query(DBQueueItem).count() == 0:
        print("Seeding Initial Data for Kevin...")
        items = [
            DBQueueItem(
                id="q-1",
                priority=1,
                sla_deadline=datetime.utcnow() + timedelta(hours=1),
                assigned_to="Kevin",
                title="Review High Risk Delinquency: User #1234",
                status="PENDING",
                tenant_id="tenant_A"
            ),
            DBQueueItem(
                id="q-2",
                priority=2,
                sla_deadline=datetime.utcnow() + timedelta(hours=24),
                assigned_to="Kevin",
                title="Approve Payment Exception: ID #999",
                status="PENDING",
                tenant_id="tenant_A"
            ),
            DBQueueItem(
                id="q-3",
                priority=3,
                sla_deadline=datetime.utcnow() - timedelta(hours=1),
                assigned_to="Kevin",
                title="Overdue Review: User #5678",
                status="PENDING",
                tenant_id="tenant_A"
            )
        ]
        db.add_all(items)

    # Seed User
    from spine.db.models import DBUser
    # Simple hash for demo (in prod use bcrypt)
    # mock hash for 'admin' is 'admin' (demo only)
    if db.query(DBUser).count() == 0:
        print("Seeding Users...")
        kevin = DBUser(
            username="kevin@anchorrealtypa.com", 
            password_hash="admin", # In real app, hash this!
            role="admin",
            tenant_id="tenant_A"
        )
        db.add(kevin)
        
    db.commit()
    print("Seeding Complete.")
    
    db.close()

if __name__ == "__main__":
    init_db()
