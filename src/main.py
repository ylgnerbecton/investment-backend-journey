import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.exc import OperationalError
from pydantic import ValidationError

from slowapi import Limiter
from slowapi.util import get_remote_address

from src.config import Settings
from src.presentation.views import health_check_router, auth_router
from src.presentation.views.user import UserView
from src.presentation.views.asset import AssetView
from src.presentation.views.transaction import OrderView

settings = Settings()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    application = FastAPI(root_path="")
    application.state = type("", (), {})()
    application.state.limiter = Limiter(key_func=get_remote_address)

    add_middleware(application)
    add_routes(application)

    return application


def add_middleware(app: FastAPI):
    logger.info("Adding middleware to the app.")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["POST", "GET", "PUT", "DELETE"],
        allow_headers=["*"],
    )


def add_routes(app: FastAPI):
    logger.info("Adding routes to the app.")
    prefix = settings.API_ROOT_PATH
    app.include_router(AssetView().get_router(), prefix=prefix)
    app.include_router(UserView().get_router(), prefix=prefix)
    app.include_router(OrderView().get_router(), prefix=prefix)
    app.include_router(health_check_router, prefix=prefix)
    app.include_router(auth_router, prefix=prefix)


app = create_app()


@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url} {response.status_code} {process_time:.4f}s"
        )
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"{request.method} {request.url} {process_time:.4f}s Exception: {str(e)}"
        )
        raise e from None


@app.exception_handler(OperationalError)
async def handle_operation_error(request: Request, exc: OperationalError):
    logger.error(f"Database operation error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"Validation error while processing request: {exc}")
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


if settings.ENVIRONMENT_NAME == "dev":
    import uvicorn

    if __name__ == "__main__":
        logger.info("Starting FastAPI app in development mode.")
        uvicorn.run(app, host="0.0.0.0", port=8010)
