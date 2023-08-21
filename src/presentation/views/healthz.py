import logging

from fastapi import APIRouter

health_check_router = APIRouter(tags=["health"])

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@health_check_router.get("/healthz")
async def healthz():
    return {"status": "OK"}


@health_check_router.get("/readiness")
async def readiness():
    return {"status": "OK"}
