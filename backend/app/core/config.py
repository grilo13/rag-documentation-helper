import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'RAG Documentation Helper'
    URI: str = os.getenv('URI')
    COLLECTION: str = os.getenv('COLLECTION')
    ID_KEY: str = os.getenv('ID_KEY')
    LOG_LEVEL: str = 'INFO'


settings = Settings()
