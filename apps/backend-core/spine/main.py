
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from spine.api.routers import auth
from spine.config import settings

app = FastAPI(title=settings.APP_NAME, version="2.0", description=f"Env: {settings.VTE_ENV}")

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from spine.core.rate_limit import limiter

# Attach to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class TenantContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Preflight Check for CORS
        if request.method == "OPTIONS":
             return await call_next(request)

        # Skip health check
        if request.url.path in ["/health", "/docs", "/openapi.json"]:
            return await call_next(request)
            
        # Allow Auth Routes (Login, Reset) without Tenant Context
        if request.url.path.startswith("/auth/"):
             return await call_next(request)

        tenant_id = request.headers.get("X-Tenant-ID")
        if not tenant_id:
             # Fail-Closed: No Tenant Context = No Service
             return JSONResponse(status_code=403, content={"error": "ERR_TENANT_CONTEXT", "message": "Missing X-Tenant-ID header"})
        
        # Store in state
        request.state.tenant_id = tenant_id
        response = await call_next(request)
        return response

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        # Preflight Check for CORS
        if request.method == "OPTIONS":
            return await call_next(request)

        if request.url.path in ["/health", "/docs", "/openapi.json"]:
            return await call_next(request)

        # Allow Auth Routes (Login, Reset) without Token
        if request.url.path.startswith("/auth/"):
             # Except /auth/me which is protected (handled by router if needed, or check)
             if request.url.path != "/auth/me":
                 return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(status_code=401, content={"error": "ERR_AUTH", "message": "Missing Authorization header"})
        
        # PWM: Real JWT Validation
        from spine.iam.jwt import verify_token
        
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        payload = verify_token(token)
        
        if not payload:
             return JSONResponse(status_code=401, content={"error": "ERR_AUTH", "message": "Invalid or Expired Token"})
        
        # Store User Context
        request.state.user = payload 

        response = await call_next(request)
        return response

app.add_middleware(AuthMiddleware)
app.add_middleware(TenantContextMiddleware)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

from spine.api.routers import payments, workflow, hitl, sys_admin, settings, cases
app.include_router(payments.router) 
app.include_router(workflow.router, prefix="/workflow", tags=["Workflow"])
app.include_router(hitl.router) 
app.include_router(cases.router, prefix="/api/cases", tags=["Cases"])
app.include_router(sys_admin.router)
app.include_router(settings.router)

from spine.api.routers import inventory
app.include_router(inventory.router, prefix="/api") 

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.0", "north_star": "KWD-2"}

@app.get("/")
def root():
    return {"message": "VTE Kernel Online"}
