@echo off
chcp 65001 >nul 2>&1
title AlgorithmMaster — DEV (авто-перезагрузка)

REM Создаём DEBUG.lock если нет
if not exist DEBUG.lock (
    echo. > DEBUG.lock
    echo [OK] DEBUG.lock создан — режим отладки включён
)

REM Применяем миграции если нужно
python manage.py migrate --check >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Применяем миграции...
    python manage.py migrate --run-syncdb
)

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set RAW_IP=%%a
set LOCAL_IP=%RAW_IP: =%
set PORT=8000

echo ============================================================
echo  AlgorithmMaster — DEV-сервер (авто-перезагрузка браузера)
echo ============================================================
echo.
echo  Локально : http://127.0.0.1:%PORT%/
echo  Сеть     : http://%LOCAL_IP%:%PORT%/
echo.
echo  Браузер обновляется автоматически при изменении файлов!
echo  Python-файлы: сервер перезапускается сам
echo  CSS/HTML/JS:  браузер обновляется через 1-2 сек
echo.
echo  Для остановки: Ctrl+C
echo ============================================================
echo.

python manage.py runserver 0.0.0.0:%PORT%
