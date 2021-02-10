![Pypi version](https://img.shields.io/pypi/v/ubarec.svg)
![Python versions](https://img.shields.io/pypi/pyversions/ubarec)
![License](https://img.shields.io/github/license/fgbm/ubarec.svg)
![Downloads](https://img.shields.io/pypi/dm/ubarec)

# Ubarec

[Russian](README.ru.md)

The utility is designed for backup and restore databases to S3 storage. 
So far, PostgreSQL and MS SQL databases are supported.

## Install

### Ubuntu

The basic dependencies and package are easy to install:
```bash
sudo apt install -y p7zip-full unixodbc-dev python3.8 python3-pip && python3.8 -m pip install ubarec
```

When working with MS SQL, you must install the appropriate [ODBC driver](https://docs.microsoft.com/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server).

### Windows

The program uses the console archiver [7-Zip](https://www.7-zip.org/download.html), 
which should be pre-installed in any convenient way, for example, with the
[chocolatey](https://chocolatey.org/):
```powershell
choco install 7zip 
```

The module is installed from the environment with administrator privileges:
```powershell
py -m pip install ubarec
```

## Config

To configure the application for the first time or edit an existing configuration, start the application
with the key ```configure```:
```powershell
ubarec configure
```

## Backup

```powershell
ubarec backup --help
```
TODO: Describe the backup algorithm, startup keys

## Restore from backup

```powershell
ubarec restore --help
```
TODO: Describe the restore algorithm, startup keys
