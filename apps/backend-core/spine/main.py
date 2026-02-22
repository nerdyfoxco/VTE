from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from spine.api.routers import queue, admin, auth, users
from spine.core.concurrency import SimpleConcurrencyMiddleware
from spine.api.routers import queue, admin, auth, users
from spine.core.concurrency import SimpleConcurrencyMiddleware
from spine.db.engine import engine, Base

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Gap 161: HSTS (Strict-Transport-Security)
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        # Gap 162: CSP (Content-Security-Policy)
        response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data: https:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        # Gap 163: X-Frame-Options
        response.headers["X-Frame-Options"] = "DENY"
        # Gap 164: Referrer-Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Additional Hardening
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response

app = FastAPI(title="VTE Spine", version="0.1.0")

# SECURITY LAYER 1: Headers (Fastest Rejection)
app.add_middleware(SecurityHeadersMiddleware)

# SECURITY LAYER 2: Concurrency (Load Shedding)
app.add_middleware(SimpleConcurrencyMiddleware)

# SECURITY LAYER 3: CORS (Access Control)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Lock down in Layer 6
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(queue.router, prefix="/api/v1", tags=["queue"])
app.include_router(admin.router, prefix="/api/v1", tags=["admin"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth", "connect"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "spine"}
