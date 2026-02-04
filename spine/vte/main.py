from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from vte.db import get_db
from vte.api import routes, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="VTE Proof Spine API",
    description="The immutable authority for Verified Transaction execution.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Development: Allow all (fixes localhost vs 127.0.0.1 issues)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from vte.db import engine, Base
from vte.orm import EvidenceBundle, DecisionObject # Ensure models are registered

# MVP: Force Table Creation (Bypassing Alembic for immediate deployment)
# WARN: Dropping all data on startup!
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(routes.router, prefix="/api/v1", tags=["Decision Core"])

@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """
    Verifies API is up and DB is reachable.
    """
    try:
        # Simple query to check DB connection
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "version": "1.0.0"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

@app.get("/", tags=["System"])
def root():
    return {"message": "VTE Proof Spine is Active. Trust but Verify."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
