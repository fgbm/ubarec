import os
import subprocess

import pyodbc

from .config import Config


class DriverMixin:
    def __init__(self):
        self.cfg: Config = Config.read()

    def get_backup_data(self):
        raise NotImplementedError

    def restore_data(self):
        raise NotImplementedError

    def get_backup_filename(self):
        raise NotImplementedError

    def get_backup_name(self):
        raise NotImplementedError

    @property
    def backup_name(self):
        return self.get_backup_name()

    @property
    def backup_filename(self):
        return self.get_backup_filename()


class DatabaseBase(DriverMixin):
    def __init__(self, database: str):
        super().__init__()
        self.database = database

    def get_backup_filename(self):
        return os.path.join(self.cfg.temp_path, f'{self.database}.bak')

    def get_backup_name(self):
        return self.database

    def get_cursor(self):
        raise NotImplementedError


class DatabasePostgres(DatabaseBase):
    def get_backup_data(self):
        pg_environ = os.environ.copy()
        pg_environ['PGPASSWORD'] = self.cfg.db_password

        process = subprocess.Popen([
            'pg_dump', '--format=custom',
            f'--host={self.cfg.db_host}', f'--port={self.cfg.db_port}', f'--username={self.cfg.db_username}',
            f'--file={self.backup_filename}', f'{self.database}'
        ], stdout=subprocess.DEVNULL, env=pg_environ)
        process.wait()

    def restore_data(self):
        pg_environ = os.environ.copy()
        pg_environ['PGPASSWORD'] = self.cfg.db_password

        process = subprocess.Popen([
            'pg_restore', '--clean', '--format=custom',
            f'--host={self.cfg.db_host}', f'--port={self.cfg.db_port}', f'--username={self.cfg.db_username}',
            f'--dbname={self.database}', self.backup_filename
        ], stdout=subprocess.DEVNULL, env=pg_environ)
        process.wait()


class DatabaseMsSql(DatabaseBase):
    def get_cursor(self):
        connection = pyodbc.connect(self.cfg.mssql_connection_string, autocommit=True)
        return connection.cursor()

    def get_backup_data(self):
        cursor = self.get_cursor()
        query = f"BACKUP DATABASE [{self.database}] TO DISK='{self.backup_filename}' WITH NOFORMAT, NOINIT, SKIP, NOREWIND;"
        cursor.execute(query)
        while cursor.nextset():
            pass

    def restore_data(self):
        cursor = self.get_cursor()
        query = f"""
            RESTORE DATABASE [{self.database}] FROM DISK='{self.backup_filename}' WITH REPLACE;
        """
        cursor.execute(query)
        while cursor.nextset():
            pass
