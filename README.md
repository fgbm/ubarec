# Ubarec

[Russian](README.ru.md)

The utility is designed for backup and restore databases to S3 storage. 
So far, PostgreSQL and MS SQL databases are supported.

## Install

### Ubuntu

The basic dependencies and package are easy to install:
```bash
sudo apt install -y p7zip-full unixodbc-dev python3.8 python3-pip && pip3 install ubarec
```

When working with MS SQL, you must install the appropriate [ODBC driver](https://docs.microsoft.com/ru-ru/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server).

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

Для первичной настроки приложения или редактирования существующей конфигурации следует запустить приложение
с ключом ```configure```:
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
