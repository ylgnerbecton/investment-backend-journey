from typing import Optional, List, Union
from pydantic import BaseSettings, Field, validator, AnyHttpUrl


class Settings(BaseSettings):
    """Main settings class. The fields of this class are automatically populated from the environment variables or
    their default values when an instance of this class is created."""

    API_ROOT_PATH: Optional[str] = Field(None, env="API_ROOT_PATH")
    DEBUG: bool = Field(default=False)
    USE_FAKE_AUTHORIZATION: bool = Field(default=False)
    ENVIRONMENT_NAME: str = Field(env="ENVIRONMENT_NAME", default="dev")
    DATABASE_URL: Optional[str] = Field(None, env="DATABASE_URL")
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    class Config:
        env_file = ".env"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[str, List[str]]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v: Optional[str], values) -> str:
        if v is None and values.get("ENVIRONMENT_NAME") == "dev":
            return "mysql+mysqldb://user:user_password@db_financial_investment:3306/financial_investment_db"
        return v


settings = Settings()
