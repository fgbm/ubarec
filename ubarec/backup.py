import os
import socket
import subprocess

import boto3
from loguru import logger

from .config import Config
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
        self.cfg: Config = Config.read()
        self.driver = driver
        self.hostname = hostname
        self.s3_filename = self._get_s3_filename()

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

    @step_function('Garbage cleaning')
    def _clean(self):
        self.clean()

    # endregion

    def _get_s3_filename(self):
        return f'{self.hostname}__{self.driver.backup_name}__{get_now_timestamp()}.7z'.lower()

    @property
    def zip_filename(self) -> str:
        return f'{self.driver.backup_filename}.7z'

    @logger.catch
    def compress(self):
        process = subprocess.Popen([
            get_7zip(), 'a',
            self.zip_filename,
            self.driver.backup_filename,
            f'-p{self.cfg.zip_password}' if len(self.cfg.zip_password) > 0 else ''
        ], stdout=subprocess.DEVNULL)
        process.wait()

    @logger.catch
    def clean(self):
        os.remove(self.zip_filename)
        os.remove(self.driver.backup_filename)

    @logger.catch
    def upload(self):
        session = boto3.session.Session()
        s3 = session.client(**self.cfg.s3_connection)
        s3.upload_file(
            self.zip_filename,
            self.cfg.bucket_name,
            self.s3_filename
        )
