import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import Settings

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

settings = Settings()
database_url = settings.DATABASE_URL


class DatabaseConnectionHandler:
    def __init__(self, connection_string: str = database_url):
        self._connection_string = connection_string
        self._engine = self._create_engine()
        self.session = None

    def _create_engine(self):
        logger.info(f"Creating engine for connection string: {self._connection_string}")
        return create_engine(self._connection_string)

    def __enter__(self):
        session_maker = sessionmaker(bind=self._engine)
        self.session = session_maker()
        logger.info(f"Session started for connection string: {self._connection_string}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session is not None:
            self.session.close()
            logger.info(
                f"Session closed for connection string: {self._connection_string}"
            )
            if exc_type or exc_val or exc_tb:
                logger.error(
                    f"Exception during database operation: {exc_val}",
                    exc_info=(exc_type, exc_val, exc_tb),
                )
