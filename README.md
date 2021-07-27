![Pypi version](https://img.shields.io/pypi/v/ubarec.svg)
![Python versions](https://img.shields.io/pypi/pyversions/ubarec)
![build](https://github.com/fgbm/ubarec/workflows/build/badge.svg)
![License](https://img.shields.io/github/license/fgbm/ubarec.svg)
![Downloads](https://img.shields.io/pypi/dm/ubarec)

# Ubarec

[Russian](https://github.com/fgbm/ubarec/blob/master/README.ru.md)

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

## Working principle

In backup mode Ubarec performs the following actions for each of the databases specified in the command line parameters
- forms database dump (either by executing SQL script or using standard utilities)
- archives the dump using 7zip; if the `UBAREC_ZIP_PASSWORD` environment variable is set, the archive is password-protected
- the created archive is copied to the S3-storage
- files created during the previous stages are deleted

The formed database archive has a file name by mask:

```The current hostname>__<DB name>__<Time Label>.zip```

In recovery mode Ubarec performs the following algorithm:
- searches for the last archive of the specified database in the S3 storage
- copies the found archive to a temporary folder
- unpacks the archive using the `UBAREC_ZIP_PASSWORD` password
- if the `do_restore` key is specified, restores the database in the DBMS either by executing an SQL script or using the standard utilities (depending on the DBMS type)
- deletes the files created during the previous steps; if the `do_restore` key is specified, the database dump remains

## Configure

According to the principles of the [12-factor application](https://12factor.net/), 
Ubarec takes settings from environment variables.

| Name                     | Required? | Default value                     | Description                                             |
| ------------------------ | --------- | --------------------------------- | ------------------------------------------------------- |
| `UBAREC_ENDPOINT_URL`    | No        | `https://storage.yandexcloud.net` | S3 object storage entry point                           |
| `UBAREC_REGION_NAME`     | No        | `ru-central1`                     | Region name                                             |
| `UBAREC_ACCESS_KEY`      | Yes       |                                   | Bucket access key ID                                    |
| `UBAREC_SECRET_KEY`      | Yes       |                                   | Bucket secret key                                       |
| `UBAREC_BUCKET_NAME`     | Yes       |                                   | Bucket name                                             |
| `UBAREC_ZIP_PASSWORD`    | No        |                                   | ZIP password                                            |
| `UBAREC_DB_TYPE`         | No        | `mssql`                           | Database type ('mssql' or 'postgres')                   |
| `UBAREC_DB_HOST`         | No        | `localhost`                       | Database server                                         |
| `UBAREC_DB_PORT`         | No        |                                   | Database connection port                                |
| `UBAREC_DB_USERNAME`     | Yes       |                                   | User name to connect to the database                    |
| `UBAREC_DB_PASSWORD`     | Yes       |                                   | Password to connect to the database                     |
| `UBAREC_DB_DRIVER`       | No        |                                   | ODBC driver to connect to the database (used for MSSQL) |
| `UBAREC_TEMP_PATH`       | No        | User temporary files storage      | Path for storing temporary files                        |
| `UBAREC_LOG_PATH`        | No        |                                   | Log storage path                                        |
| `UBAREC_DEBUG`           | No        | `False`                           | Debug mode                                              |
| `UBAREC_FILENAME_PREFIX` | Нет       | `{hostname}__{backup_name}__`     | Prefix of file name uploaded to S3 storage              |

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
