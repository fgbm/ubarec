import tempfile
from enum import Enum
from typing import Optional

from pydantic import (
    BaseSettings,
    HttpUrl,
    DirectoryPath
)


class DatabaseType(str, Enum):
    mssql = 'mssql'
    postgres = 'postgres'


class Settings(BaseSettings):
    service_name: str = 's3'
    endpoint_url: HttpUrl = 'https://storage.yandexcloud.net'
    region_name: str = 'ru-central1'
    access_key: str
    secret_key: str
    bucket_name: str
    zip_password: Optional[str] = None
    db_type: DatabaseType = DatabaseType.mssql
    db_host: str = 'localhost'
    db_port: int = 1433
    db_username: str
    db_password: str
    db_driver: str = ''
    temp_path: DirectoryPath = tempfile.gettempdir()
    log_path: DirectoryPath = None
    debug: bool = False
    filename_prefix: str = '{hostname}__{backup_name}__'

    class Config:
        env_prefix = 'UBAREC_'

    @property
    def s3_connection(self):
        return {
            'service_name'         : self.service_name,
            'endpoint_url'         : self.endpoint_url,
            'region_name'          : self.region_name,
            'aws_access_key_id'    : self.access_key,
            'aws_secret_access_key': self.secret_key
        }


settings = Settings()
