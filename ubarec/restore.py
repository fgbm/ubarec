import os
import socket
import subprocess

import boto3
import typer

from ._defaults import settings
from .drivers import DatabaseBase
from .handlers import step_function, get_7zip


class Restore:
    def __init__(
            self,
            driver: DatabaseBase,
            *,
            s3_filename: str = None,
            do_restore: bool = False,
            hostname: str = socket.gethostname()
    ):
        """Data recovery base class

        The class implements the general logic of data backup recovery:
        searching for the last backup copy in the S3 storage, unzipping and,
        if necessary, restoring instead of the current database

        :param driver: database driver
        :param s3_filename: using a specified file name in the repository for recovery
        :param hostname: override system hostname
        """
        self.driver = driver
        self.specified_s3_filename = s3_filename
        self.hostname = hostname
        self.do_restore = do_restore
        self.s3_filename = self.find_latest_backup() if s3_filename is None else s3_filename

        self._download()
        self._decompress()
        self._restore()
        self._clean()

    # region Hidden "step-by-step" functions

    @step_function('Download archive from repository')
    def _download(self):
        self.download()

    @step_function('Unzipping')
    def _decompress(self):
        self.decompress()

    @step_function('Restore database')
    def _restore(self):
        if self.do_restore:
            self.driver.restore_data()

    @step_function('Garbage collect')
    def _clean(self):
        self.clean()

    # endregion

    @property
    def zip_filename(self):
        return f'{self.driver.backup_filename}.7z'

    def find_latest_backup(self) -> str:
        prefix = self.driver.get_filename_prefix(self.hostname)
        session = boto3.session.Session()
        s3 = session.client(**settings.s3_connection)

        objects = s3.list_objects_v2(Bucket=settings.bucket_name, Prefix=prefix).get('Contents', [])
        if len(objects) == 0:
            raise ValueError(f"No backups found in the repository by prefix: '{prefix}'")

        latest = sorted(objects, key=lambda obj: obj['LastModified'], reverse=True)[0]
        return latest['Key']

    def download(self):
        session = boto3.session.Session()
        s3 = session.client(**settings.s3_connection)
        s3.download_file(
            settings.bucket_name,
            self.s3_filename,
            self.zip_filename
        )

    def decompress(self):
        process = subprocess.Popen([
            get_7zip(),
            'e', '-y',
            f'-p{settings.zip_password}' if settings.zip_password is not None and len(settings.zip_password) > 0 else '',
            f'-o{settings.temp_path}',
            self.zip_filename
        ], stdout=subprocess.DEVNULL)
        process.wait()

    def clean(self):
        os.remove(self.zip_filename)
        if self.do_restore:
            os.remove(self.driver.backup_filename)
        else:
            typer.echo(f'Database backup file restored in {self.driver.backup_filename}')
