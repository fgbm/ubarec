import os
import socket
import subprocess

import boto3
import pyodbc

from .config import Config
from .handlers import step_function, get_7zip, get_now_timestamp


class BaseBackup:
    def __init__(
            self,
            database: str,
            *,
            hostname: str = socket.gethostname()
    ):
        """Backup data base class

        :param database: database name
        :param hostname: override system hostname
        """
        self.cfg: Config = Config.read()
        self.database = database
        self.hostname = hostname
        self.s3_filename = self._get_s3_filename()

        self._backup()
        self._compress()
        self._upload()
        self._clean()

    # region Hidden "step-by-step" functions

    @step_function(f'\U0001F47D Dump database')
    def _backup(self):
        self.backup()

    @step_function(f'\U0001F510 Compress dump')
    def _compress(self):
        self.compress()

    @step_function('\U0001F4BE Upload data to S3')
    def _upload(self):
        self.upload()

    @step_function(f'\U0001F4A5 Garbage cleaning')
    def _clean(self):
        self.clean()

    # endregion

    def _get_s3_filename(self):
        return f'{self.hostname}__{self.database}__{get_now_timestamp()}.7z'.lower()

    @property
    def bak_filename(self) -> str:
        return os.path.join(self.cfg.temp_path, f'{self.database}.bak')

    @property
    def zip_filename(self) -> str:
        return os.path.join(self.cfg.temp_path, f'{self.database}.bak.7z')

    def get_cursor(self):
        raise NotImplemented

    def backup(self):
        raise NotImplemented

    def compress(self):
        process = subprocess.Popen([
            get_7zip(), 'a',
            self.zip_filename,
            self.bak_filename,
            f'-p{self.cfg.zip_password}' if len(self.cfg.zip_password) > 0 else ''
        ], stdout=subprocess.DEVNULL)
        process.wait()

    def clean(self):
        os.remove(self.zip_filename)
        os.remove(self.bak_filename)

    def upload(self):
        session = boto3.session.Session()
        s3 = session.client(**self.cfg.s3_connection)
        s3.upload_file(
            self.zip_filename,
            self.cfg.bucket_name,
            self.s3_filename
        )


class BackupMSSql(BaseBackup):
    def get_cursor(self):
        connection = pyodbc.connect(self.cfg.mssql_connection_string, autocommit=True)
        return connection.cursor()

    def backup(self):
        cursor = self.get_cursor()
        query = f"BACKUP DATABASE [{self.database}] TO DISK='{self.bak_filename}' WITH NOFORMAT, NOINIT, SKIP, NOREWIND;"
        cursor.execute(query)
        while cursor.nextset():
            pass


class BackupPostgres(BaseBackup):
    def backup(self):
        pg_environ = os.environ.copy()
        pg_environ['PGPASSWORD'] = self.cfg.db_password

        process = subprocess.Popen([
            'pg_dump', '--format=custom',
            f'--host={self.cfg.db_host}', f'--port={self.cfg.db_port}', f'--username={self.cfg.db_username}',
            f'--file={self.bak_filename}', f'{self.database}'
        ], stdout=subprocess.DEVNULL, env=pg_environ)
        process.wait()
