import os
import socket
import subprocess

import boto3

from ._defaults import settings
from .drivers import DatabaseBase
from .handlers import step_function, get_7zip, get_now_timestamp


class Backup:
    def __init__(
            self,
            driver: DatabaseBase,
            *,
            hostname: str = socket.gethostname()
    ):
        """Backup data base class

        :param driver: database driver
        :param hostname: override system hostname
        """
        self.driver = driver
        self.hostname = hostname

        self._backup()
        self._compress()
        self._upload()
        self._clean()

    # region Hidden "step-by-step" functions

    @step_function('Dump database')
    def _backup(self):
        self.driver.get_backup_data()

    @step_function('Compress dump')
    def _compress(self):
        self.compress()

    @step_function('Upload data to S3')
    def _upload(self):
        self.upload()

    @step_function('Garbage collect')
    def _clean(self):
        self.clean()

    # endregion

    @property
    def s3_filename(self):
        prefix = self.driver.get_filename_prefix(self.hostname)
        return f'{prefix}{get_now_timestamp()}.7z'.lower()

    @property
    def zip_filename(self) -> str:
        return f'{self.driver.backup_filename}.7z'

    def compress(self):
        process = subprocess.Popen([
            get_7zip(), 'a',
            self.zip_filename,
            self.driver.backup_filename,
            f'-p{settings.zip_password}' if settings.zip_password is not None and len(settings.zip_password) > 0 else ''
        ], stdout=subprocess.DEVNULL)
        process.wait()

    def clean(self):
        os.remove(self.zip_filename)
        os.remove(self.driver.backup_filename)

    def upload(self):
        session = boto3.session.Session()
        s3 = session.client(**settings.s3_connection)
        s3.upload_file(
            self.zip_filename,
            settings.bucket_name,
            self.s3_filename
        )
