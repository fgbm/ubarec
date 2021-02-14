import datetime
import os
import platform
from pathlib import Path

import typer
from loguru import logger


def type_done():
    typer.secho('DONE', fg=typer.colors.GREEN)


def type_error():
    typer.secho('ERROR', fg=typer.colors.RED)


def step_function(message: str):
    def upper_wrapper(func):
        def wrapper(*args, **kwargs):
            typer.echo(message + ' ... ', nl=False)
            try:
                result = func(*args, **kwargs)
                type_done()
                return result
            except Exception:
                type_error()
                raise

        return wrapper

    return upper_wrapper


def get_7zip():
    if platform.system() == 'Windows':
        pf_environment_variables = ('ProgramFiles', 'ProgramFiles(x86)', 'ProgramW6432', 'PROGRAMDATA')
        pf_path_list = [Path(os.environ.get(var, '')) for var in pf_environment_variables]
        try:
            pf_path = next(filter(lambda x: x != '', pf_path_list))
            return str(pf_path / '7-Zip' / '7z.exe')
        except StopIteration:
            msg = 'Could not find path to 7-Zip executable file. Is the archiver really installed?'
            logger.error(msg)
            typer.echo(msg)
            raise typer.Abort()

    else:
        return '7z'


def get_now_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
