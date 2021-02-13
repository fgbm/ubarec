from pathlib import Path
from typing import Dict, Type, List

import typer
from appdirs import user_log_dir
from loguru import logger

from .__init__ import __version__
from .backup import Backup
from .config import Config
from .drivers import DatabaseBase, DatabaseMsSql, DatabasePostgres
from .restore import Restore

DATABASE_DRIVER: Dict[str, Type[DatabaseBase]] = {
    'mssql'   : DatabaseMsSql,
    'postgres': DatabasePostgres
}

LOG_FILENAME = Path(user_log_dir('ubarec', False)) / 'errors.log'
LOG_FILENAME.parent.mkdir(parents=True, exist_ok=True)
logger.add(LOG_FILENAME, level='ERROR', rotation="5 MB", diagnose=False)

app = typer.Typer()


@app.command()
@logger.catch
def backup(
        databases: List[str] = typer.Argument(..., help='Database list')
):
    for database in databases:
        config = Config.read()
        typer.echo(f'\U000026A1 Process backup {database}')
        driver = DATABASE_DRIVER[config.db_type](database)
        Backup(driver)
        typer.echo('')

    typer.echo(f'\U0001F389 That\'s all, folks!')


@app.command()
@logger.catch
def restore(
        database: str = typer.Argument(..., help='Database name'),
        do_restore: bool = typer.Option(False, help='Restore database from backup')
):
    config = Config.read()

    if do_restore:
        typer.confirm('Are you sure about recovery? The current data will be changed!', abort=True)

    typer.echo(f'\U000026A1 Process restore {database}')
    driver = DATABASE_DRIVER[config.db_type](database)
    Restore(driver, do_restore=do_restore)

    typer.echo(f'\U0001F389 That\'s all, folks!')


@app.command()
@logger.catch
def configure():
    config = Config.read(False) or Config()
    config.initialize()
    config.save()


@app.command()
def version():
    typer.echo(__version__)
