# Ubarec

[English](README.md)

Утилита предназначена для резервного копирования и восстановления баз данных на S3 хранилища. 
Пока что поддерживаются базы данных PostgreSQL и MS SQL.

## Установка

### Ubuntu

Основные зависимости и пакет устанавливаются легко:
```bash
sudo apt install -y p7zip-full unixodbc-dev python3.8 python3-pip && pip3 install ubarec
```

При работе с MS SQL необходимо установить соответствующий [драйвер ODBC](https://docs.microsoft.com/ru-ru/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server).

### Windows

В программе используется консольный архиватор [7-Zip](https://www.7-zip.org/download.html), 
который необходимо предварительно установить любым удобным способом, например, при помощи
пакетного менеджера [chocolatey](https://chocolatey.org/):
```powershell
choco install 7zip 
```

Установка модуля производится из окружения с правами администратора:
```powershell
py -m pip install ubarec
```

## Настройка

Для первичной настроки приложения или редактирования существующей конфигурации следует запустить приложение
с ключом ```configure```:
```powershell
ubarec configure
```

## Резервное копирование

```powershell
ubarec backup --help
```
TODO: Описать алгоритм бекапа, ключи запуска

## Восстановление из резервной копии

```powershell
ubarec restore --help
```
TODO: Описать алгоритм восстановления, ключи запуска
