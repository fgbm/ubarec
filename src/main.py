from typing import Dict, Type
from typing import List

import typer

from .backup import BaseBackup, BackupMSSql, BackupPostgres
from .config import Config
from .restore import BaseRestore, RestoreMSSql, RestorePostres

app = typer.Typer()

BACKUP_DISPATCHER: Dict[str, Type[BaseBackup]] = {
    'mssql'   : BackupMSSql,
    'postgres': BackupPostgres
}

RESTORE_DISPATCHER: Dict[str, Type[BaseRestore]] = {
    'mssql'   : RestoreMSSql,
    'postgres': RestorePostres
}


@app.command()
def backup(
        databases: List[str] = typer.Argument(..., help='Database list')
):
    for database in databases:
        config = Config.read()
        typer.echo(f'\U000026A1 Process backup {database}')
        BACKUP_DISPATCHER[config.db_type](database)
        typer.echo('')

    typer.echo(f'\U0001F389 That\'s all, folks!')


@app.command()
def restore(
        database: str = typer.Argument(..., help='Database name'),
        do_restore: bool = typer.Option(False, help='Restore database from backup')
):
    config = Config.read()

    if do_restore:
        typer.confirm('Are you sure about recovery? The current data will be changed!', abort=True)

    typer.echo(f'\U000026A1 Process restore {database}')
    RESTORE_DISPATCHER[config.db_type](database, do_restore=do_restore)

    typer.echo(f'\U0001F389 That\'s all, folks!')


@app.command()
def configure():
    config = Config.read(False) or Config()
    config.initialize()
    config.save()


if __name__ == "__main__":
    app()
