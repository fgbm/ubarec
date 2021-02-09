from __future__ import annotations
from enum import Enum

from appdirs import user_config_dir
from pathlib import Path
import json
import typer
import tempfile

APPNAME = 'ubarec'
VERSION = '0.1'
CONFIG_FILE = Path(user_config_dir(APPNAME, False, VERSION)) / 'config.json'


class DatabaseType(str, Enum):
    mssql = 'mssql'
    postgres = 'postgres'


class Config:
    def __init__(
            self,
            service_name: str = 's3',
            endpoint_url: str = 'https://storage.yandexcloud.net',
            region_name: str = 'ru-central1',
            aws_access_key_id: str = '',
            aws_secret_access_key: str = '',
            bucket_name: str = '',
            zip_password: str = '',
            db_type: DatabaseType = DatabaseType.mssql,
            db_host: str = 'localhost',
            db_port: int = 1433,
            db_username: str = '',
            db_password: str = '',
            db_driver: str = '{SQL Server}',
            temp_path: str = tempfile.gettempdir()
    ):
        self.service_name = service_name
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket_name
        self.zip_password = zip_password
        self.db_type = db_type
        self.db_host = db_host
        self.db_port = db_port
        self.db_username = db_username
        self.db_password = db_password
        self.db_driver = db_driver
        self.temp_path = temp_path

    @property
    def s3_connection(self):
        return {k: v for k, v in self.__dict__.items() if k in (
            'service_name', 'endpoint_url', 'region_name', 'aws_access_key_id', 'aws_secret_access_key'
        )}

    @property
    def mssql_connection_string(self) -> str:
        return ';'.join([
            f'SERVER={self.db_host}',
            f'PORT={self.db_port}',
            f'UID={self.db_username}',
            f'PWD={self.db_password}',
            f'DRIVER={self.db_driver}'
        ])

    @classmethod
    def read(cls, on_err_init:bool = True) -> Config:
        try:
            with open(CONFIG_FILE, 'r', encoding='utf8') as config_file:
                return cls(**json.load(config_file))
        except FileNotFoundError:
            if on_err_init:
                typer.echo('Configuration file not found, \U00002708 parameters must be entered')
                config = Config()
                config.initialize()
                config.save()
                return config

    def save(self):
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf8') as config_file:
            json.dump(self.__dict__, config_file, indent=4)

    def initialize(self):
        self.service_name = typer.prompt('Service name', self.service_name)
        self.endpoint_url = typer.prompt('Endpoint URL', self.endpoint_url)
        self.region_name = typer.prompt('Region name', self.region_name)
        self.aws_access_key_id = typer.prompt('S3 accesss id key', hide_input=True)
        self.aws_secret_access_key = typer.prompt('S3 accesss secret key', hide_input=True)
        self.bucket_name = typer.prompt('Bucket name', self.bucket_name)
        self.zip_password = typer.prompt('7z password', hide_input=True)
        self.db_type = typer.prompt('Database type', self.db_type, type=DatabaseType)
        self.db_host = typer.prompt('Database hostname', self.db_host)
        self.db_port = typer.prompt('Database connection port', self.db_port, type=int)
        self.db_username = typer.prompt('Database username', self.db_username)
        self.db_password = typer.prompt('Database password', self.db_password)
        self.db_driver = typer.prompt('Database ODBC driver name', self.db_driver)
        self.temp_path = typer.prompt('Location for temporary files', self.temp_path)
