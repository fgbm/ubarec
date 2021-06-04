from os import environ
from enum import Enum
import tempfile


class DatabaseType(str, Enum):
    mssql = 'mssql'
    postgres = 'postgres'


def env(key, type_, default=None):
    if key not in environ:
        return default

    val = environ[key]

    if type_ == str:
        return val
    elif type_ == bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        raise ValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val)
        )
    elif type_ == int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(
                "Invalid environment variable '%s' (expected an integer): '%s'" % (key, val)
            ) from None
    else:
        return type_(val)


SERVICE_NAME = env('UBAREC_SERVICE_NAME', str, 's3')
ENDPOINT_URL = env('UBAREC_ENDPOINT_URL', str, 'https://storage.yandexcloud.net')
REGION_NAME = env('UBAREC_REGION_NAME', str, 'ru-central1')
ACCESS_KEY = env('UBAREC_ACCESS_KEY', str)
SECRET_KEY = env('UBAREC_SECRET_KEY', str)
BUCKET_NAME = env('UBAREC_BUCKET_NAME', str)
ZIP_PASSWORD = env('UBAREC_ZIP_PASSWORD', str)
DB_TYPE = env('UBAREC_DB_TYPE', DatabaseType, DatabaseType.mssql.name)
DB_HOST = env('UBAREC_DB_HOST', str, 'localhost')
DB_PORT = env('UBAREC_DB_PORT', int, 1433)
DB_USER = env('UBAREC_DB_USERNAME', str)
DB_PASS = env('UBAREC_DB_PASSWORD', str)
DB_DRIVER = env('UBAREC_DB_DRIVER', str, '')
TEMP_PATH = env('UBAREC_TEMP_PATH', str, tempfile.gettempdir())


def get_s3_connection():
    return {
        'service_name'         : SERVICE_NAME,
        'endpoint_url'         : ENDPOINT_URL,
        'region_name'          : REGION_NAME,
        'aws_access_key_id'    : ACCESS_KEY,
        'aws_secret_access_key': SECRET_KEY
    }

