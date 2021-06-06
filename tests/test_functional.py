import os

from ubarec.main import backup, restore, version

DATABASE = os.environ.get('TEST_DATABASE')


def test_backup():
    backup(databases=[DATABASE])


def test_restore():
    restore(database=DATABASE, do_restore=False)


def test_version():
    version()
