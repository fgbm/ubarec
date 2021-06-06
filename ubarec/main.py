from pathlib import Path
from typing import Dict, Type, List

import typer

from .__init__ import __version__
from ._defaults import *
from .backup import Backup
from .drivers import DatabaseBase, DatabaseMsSql, DatabasePostgres
from .restore import Restore

DATABASE_DRIVER: Dict[DatabaseType, Type[DatabaseBase]] = {
    DatabaseType.mssql   : DatabaseMsSql,
    DatabaseType.postgres: DatabasePostgres
}

if LOG_PATH is not None:
    logger.add(Path(LOG_PATH) / 'errors.log', level='ERROR', rotation="5 MB", diagnose=False, backtrace=False)
    if DEBUG:
        logger.add(Path(LOG_PATH) / 'debug.log', level='DEBUG', rotation="5 MB", diagnose=True)

app = typer.Typer()


@app.command()
@logger.catch(onerror=lambda _: sys.exit(1))
def backup(
        databases: List[str] = typer.Argument(..., help='Database list')
):
    for database in databases:
        typer.echo(f'Process backup {database}')
        driver = DATABASE_DRIVER[DB_TYPE](database)
        Backup(driver)
        typer.echo('')

    typer.echo('That\'s all, folks!')


@app.command()
@logger.catch(onerror=lambda _: sys.exit(1))
def restore(
        database: str = typer.Argument(..., help='Database name'),
        do_restore: bool = typer.Option(False, help='Restore database from backup')
):
    if do_restore:
        typer.confirm('Are you sure about recovery? The current data will be changed!', abort=True)

    typer.echo(f'Process restore {database}')
    driver = DATABASE_DRIVER[DB_TYPE](database)
    Restore(driver, do_restore=do_restore)

    typer.echo('That\'s all, folks!')


@app.command()
def version():
    typer.echo(__version__)
