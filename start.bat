@echo off
chcp 65001 >nul 2>&1
title AlgorithmMaster — ОАИП

REM ── Проверяем что БД проинициализирована ────────────────────────────────────
python manage.py migrate --check >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] База данных не настроена. Запускаем первоначальную установку...
    echo.
    python manage.py migrate --run-syncdb
    python manage.py seed_works   >nul 2>&1
    python manage.py seed_theory  >nul 2>&1
    python manage.py seed_quizzes >nul 2>&1
    python manage.py create_default_admin
    python manage.py collectstatic --noinput --clear >nul 2>&1
    echo [OK] Установка завершена.
    echo.
)

REM ── Определяем IP ───────────────────────────────────────────────────────────
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set RAW_IP=%%a
)
set LOCAL_IP=%RAW_IP: =%

set PORT=8000

echo ============================================================
echo  AlgorithmMaster — Сервер запускается
echo ============================================================
echo.
echo  На этом компьютере : http://127.0.0.1:%PORT%/
echo  В локальной сети   : http://%LOCAL_IP%:%PORT%/
echo  Панель препод.     : http://127.0.0.1:%PORT%/teacher/
echo  Django Admin       : http://127.0.0.1:%PORT%/admin/
echo.
echo  Для остановки: Ctrl+C
echo ============================================================
echo.

python -m waitress --host=0.0.0.0 --port=%PORT% --threads=8 algorithm_site.wsgi:application

if %errorlevel% neq 0 (
    echo.
    echo [ОШИБКА] Сервер завершился с ошибкой.
    echo Возможная причина: порт %PORT% занят другой программой.
    echo Попробуй: python manage.py runserver 0.0.0.0:8001
    pause
)
