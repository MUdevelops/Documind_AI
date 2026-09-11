import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.db.session import init_db

settings = get_settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("documind")

app = FastAPI(
    title="DocuMind API",
    description="AI-Powered Document Intelligence Platform -- local-first RAG over your own documents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_and_logging(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.monotonic()
    response = await call_next(request)
    duration_ms = int((time.monotonic() - start) * 1000)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_id=%s method=%s path=%s status=%s duration_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Never leak internals; return a clean, structured 422.
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("DocuMind API starting up (env=%s)", settings.ENV)


@app.get("/", tags=["root"])
def root():
    return {"name": "DocuMind API", "docs": "/docs", "health": "/api/v1/health"}


@app.get("/health", tags=["health"], summary="Top-level health check alias")
def health_alias():
    from app.api.v1.health import health

    return health()


app.include_router(api_router, prefix="/api/v1")
