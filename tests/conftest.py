import pytest
import httpx
import pymysql

from fastapi import FastAPI
from src.presentation.views import health_check_router, AssetView, UserView, OrderView
from src.config import Settings


@pytest.fixture(scope="module", name="settings")
def settings() -> Settings:
    return Settings(
        DATABASE_URL="mysql+pymysql://user:user_password@db_financial_investment:3306/financial_investment_db",
    )


@pytest.fixture(scope="module")
def mysql_db_session(settings):
    url_components = settings.DATABASE_URL.split("//")[1].split("@")
    user_info = url_components[0].split(":")
    db_info = url_components[1].split("/")

    host_info = db_info[0].split(":")
    db_name = db_info[1]

    user = user_info[0]
    password = user_info[1]
    host = host_info[0]
    port = int(host_info[1])

    connection = pymysql.connect(
        host=host, port=port, user=user, password=password, db=db_name
    )
    yield connection.cursor()
    connection.close()


@pytest.fixture
def assert_all_responses_were_requested() -> bool:
    return False


@pytest.fixture(scope="module")
def test_app(settings):
    app = FastAPI(root_path=settings.API_ROOT_PATH)
    app.include_router(health_check_router)
    app.include_router(AssetView().get_router())
    app.include_router(UserView().get_router())
    app.include_router(OrderView().get_router())
    return app


@pytest.fixture
async def test_client(test_app):
    async with httpx.AsyncClient(
        app=test_app, base_url="http://localhost:8010"
    ) as client:
        yield client
