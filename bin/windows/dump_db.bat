@echo off

set BACKUP_DIR=..\..\database_backup\%date:~10,4%-%date:~4,2%-%date:~7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%

set BACKUP_DIR=%BACKUP_DIR: =0%
mkdir "%BACKUP_DIR%"

mongodump --uri="mongodb://admin:xxxxx@xxxxx:27017/app?authSource=admin" --out="%BACKUP_DIR%"

if %ERRORLEVEL% EQU 0 (
    echo Backup completed successfully to %BACKUP_DIR%
) else (
    echo Backup failed
    exit /b 1
)