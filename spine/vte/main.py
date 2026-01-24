from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from vte.db import get_db
from vte.api.routes import router as api_router

app = FastAPI(
    title="VTE Proof Spine API",
    description="The immutable authority for Verified Transaction execution.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1", tags=["Decision Core"])

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
