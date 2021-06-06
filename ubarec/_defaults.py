import sys
import tempfile
from enum import Enum
from os import environ

from loguru import logger


class DatabaseType(str, Enum):
    mssql = 'mssql'
    postgres = 'postgres'


def env(key, type_, default=None, required=False):
    if key not in environ:
        if not required:
            return default
        else:
            logger.error(f"Environment variable '{key}' must be assigned")
            sys.exit(1)

    val = environ[key]

    if type_ == str:
        return val
    elif type_ == bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        logger.error(f"Invalid environment variable '{key}' (expected a boolean): '{val}'")
        sys.exit(1)

    elif type_ == int:
        try:
            return int(val)
        except ValueError:
            logger.error(f"Invalid environment variable '{key}' (expected an integer): '{val}'")
            sys.exit(1)

    else:
        try:
            return type_(val)
        except ValueError as e:
            logger.error(f"Invalid environment variable '{key}': '{e}'")
            sys.exit(1)


SERVICE_NAME = env('UBAREC_SERVICE_NAME', str, 's3')
ENDPOINT_URL = env('UBAREC_ENDPOINT_URL', str, 'https://storage.yandexcloud.net')
REGION_NAME = env('UBAREC_REGION_NAME', str, 'ru-central1')
ACCESS_KEY = env('UBAREC_ACCESS_KEY', str, required=True)
SECRET_KEY = env('UBAREC_SECRET_KEY', str, required=True)
BUCKET_NAME = env('UBAREC_BUCKET_NAME', str, required=True)
ZIP_PASSWORD = env('UBAREC_ZIP_PASSWORD', str)
DB_TYPE = env('UBAREC_DB_TYPE', DatabaseType, DatabaseType.mssql.name)
DB_HOST = env('UBAREC_DB_HOST', str, 'localhost')
DB_PORT = env('UBAREC_DB_PORT', int, 1433)
DB_USER = env('UBAREC_DB_USERNAME', str, required=True)
DB_PASS = env('UBAREC_DB_PASSWORD', str, required=True)
DB_DRIVER = env('UBAREC_DB_DRIVER', str, '')
TEMP_PATH = env('UBAREC_TEMP_PATH', str, tempfile.gettempdir())
LOG_PATH = env('UBAREC_LOG_PATH', str)
DEBUG = env('UBAREC_DEBUG', bool, False)


def get_s3_connection():
    return {
        'service_name'         : SERVICE_NAME,
        'endpoint_url'         : ENDPOINT_URL,
        'region_name'          : REGION_NAME,
        'aws_access_key_id'    : ACCESS_KEY,
        'aws_secret_access_key': SECRET_KEY
    }
