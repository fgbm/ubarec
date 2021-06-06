import os
import subprocess
from abc import ABC, abstractmethod

import pyodbc

from ._defaults import *


class DriverMixin(ABC):

    @abstractmethod
    def get_backup_data(self):
        ...

    @abstractmethod
    def restore_data(self):
        ...

    @abstractmethod
    def get_backup_filename(self):
        ...

    @abstractmethod
    def get_backup_name(self):
        ...

    @property
    def backup_name(self):
        return self.get_backup_name()

    @property
    def backup_filename(self):
        return self.get_backup_filename()


class DatabaseBase(DriverMixin, ABC):
    def __init__(self, database: str):
        super().__init__()
        self.database = database

    def get_backup_filename(self):
        return os.path.join(TEMP_PATH, f'{self.database}.bak')

    def get_backup_name(self):
        return self.database

    def get_cursor(self):
        ...


class DatabasePostgres(DatabaseBase):
    def get_backup_data(self):
        pg_environ = os.environ.copy()
        pg_environ['PGPASSWORD'] = DB_PASS

        process = subprocess.Popen([
            'pg_dump', '--format=custom',
            f'--host={DB_HOST}', f'--port={DB_PORT}', f'--username={DB_USER}',
            f'--file={self.backup_filename}', f'{self.database}'
        ], stdout=subprocess.DEVNULL, env=pg_environ)
        if process.wait() != 0:
            raise ValueError("Errors occurred during the backup")

    def restore_data(self):
        pg_environ = os.environ.copy()
        pg_environ['PGPASSWORD'] = DB_PASS

        process = subprocess.Popen([
            'pg_restore', '--clean', '--format=custom',
            f'--host={DB_HOST}', f'--port={DB_PORT}', f'--username={DB_USER}',
            f'--dbname={self.database}', self.backup_filename
        ], stdout=subprocess.DEVNULL, env=pg_environ)
        if process.wait() != 0:
            raise ValueError("Errors occurred during the restore")


class DatabaseMsSql(DatabaseBase):
    @property
    def mssql_connection_string(self):
        return ';'.join([
            f'SERVER={DB_HOST}',
            f'PORT={DB_PORT}',
            f'UID={DB_USER}',
            f'PWD={DB_PASS}',
            f'DRIVER={DB_DRIVER}'
        ])

    def get_cursor(self):
        connection = pyodbc.connect(self.mssql_connection_string, autocommit=True)
        return connection.cursor()

    def get_backup_data(self):
        cursor = self.get_cursor()
        query = f"BACKUP DATABASE [{self.database}] TO DISK='{self.backup_filename}' WITH NOFORMAT, NOINIT, SKIP, NOREWIND;"
        cursor.execute(query)
        while cursor.nextset():
            pass

    def restore_data(self):
        cursor = self.get_cursor()
        query = f"RESTORE DATABASE [{self.database}] FROM DISK='{self.backup_filename}' WITH REPLACE;"
        cursor.execute(query)
        while cursor.nextset():
            pass
