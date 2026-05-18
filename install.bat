@echo off
chcp 65001 >nul 2>&1
title Установщик AlgorithmMaster — ОАИП

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         AlgorithmMaster — Установщик (Windows)              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM ── ШАГ 1: Проверяем Python ─────────────────────────────────────────────────
echo [1/6] Проверка Python...
python --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo     Найден: %%v
    goto :PYTHON_OK
)

REM Python не найден — скачиваем
echo     Python не найден. Скачиваем Python 3.12...
echo.

REM Пробуем через winget (Windows 11 / обновлённый Win10)
winget --version >nul 2>&1
if %errorlevel% == 0 (
    echo     Устанавливаем через winget...
    winget install --id Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
    goto :REFRESH_PATH
)

REM Fallback — скачиваем через PowerShell
echo     Скачиваем установщик Python через браузер...
powershell -Command "& { $url='https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe'; $out='%TEMP%\python_installer.exe'; Write-Host '    Загрузка...'; (New-Object Net.WebClient).DownloadFile($url,$out); Write-Host '    Установка...'; Start-Process -FilePath $out -Args '/quiet InstallAllUsers=0 PrependPath=1' -Wait; Write-Host '    Готово.' }"
if %errorlevel% neq 0 (
    echo.
    echo [ОШИБКА] Не удалось установить Python автоматически.
    echo Скачай вручную: https://python.org/downloads
    echo При установке отметь "Add Python to PATH"
    echo.
    pause & exit /b 1
)

:REFRESH_PATH
REM Обновляем PATH в текущей сессии
for /f "tokens=*" %%p in ('powershell -Command "[Environment]::GetEnvironmentVariable(\"PATH\",\"User\")"') do set PATH=%%p;%PATH%

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ВНИМАНИЕ] Python установлен, но требуется ПЕРЕЗАПУСК командной строки.
    echo Закрой это окно, открой новую командную строку в этой папке и запусти install.bat снова.
    pause & exit /b 1
)

:PYTHON_OK
echo     OK

REM ── ШАГ 2: Проверяем pip ────────────────────────────────────────────────────
echo.
echo [2/6] Проверка pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo     Устанавливаем pip...
    python -m ensurepip --upgrade >nul 2>&1
)
echo     OK

REM ── ШАГ 3: Устанавливаем зависимости ────────────────────────────────────────
echo.
echo [3/6] Установка зависимостей (Django, Waitress, WhiteNoise...)

REM Проверяем каждый пакет и ставим только если нет
python -c "import django" >nul 2>&1
if %errorlevel% neq 0 (
    echo     Устанавливаем Django...
    python -m pip install django==5.2.6 --quiet
)

python -c "import waitress" >nul 2>&1
if %errorlevel% neq 0 (
    echo     Устанавливаем Waitress...
    python -m pip install waitress==3.0.1 --quiet
)

python -c "import whitenoise" >nul 2>&1
if %errorlevel% neq 0 (
    echo     Устанавливаем WhiteNoise...
    python -m pip install whitenoise==6.8.2 openpyxl==3.1.5 --quiet
)

python -c "import chardet" >nul 2>&1
if %errorlevel% neq 0 (
    echo     Устанавливаем chardet...
    python -m pip install chardet==5.2.0 --quiet
)

python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo     Устанавливаем Pillow...
    python -m pip install Pillow==10.4.0 --quiet
)

echo     OK — все зависимости установлены

REM ── ШАГ 4: Миграции базы данных ─────────────────────────────────────────────
echo.
echo [4/6] Создание базы данных...
python manage.py migrate --run-syncdb
if %errorlevel% neq 0 (
    echo [ОШИБКА] migrate завершился с ошибкой
    pause & exit /b 1
)
echo     OK

REM ── ШАГ 5: Заполнение данными ───────────────────────────────────────────────
echo.
echo [5/6] Заполнение данными...
python manage.py seed_works   >nul 2>&1
python manage.py seed_theory  >nul 2>&1
python manage.py seed_quizzes >nul 2>&1
python manage.py create_default_admin
echo     OK

REM ── ШАГ 6: Статика ──────────────────────────────────────────────────────────
echo.
echo [6/6] Сбор статических файлов...
python manage.py collectstatic --noinput --clear
echo     OK

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                  Установка завершена!                        ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  Логин преподавателя:  admin                                 ║
echo ║  Пароль:               admin                                 ║
echo ║                                                              ║
echo ║  ВАЖНО: смените пароль после первого входа!                  ║
echo ║  Перейди: http://127.0.0.1:8000/admin/                      ║
echo ║           Пользователи → admin → Изменить пароль             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
set /p START="Запустить сервер прямо сейчас? (y/n): "
if /i "%START%"=="y" goto :RUNSERVER
if /i "%START%"=="д" goto :RUNSERVER
goto :END

:RUNSERVER
echo.
call start.bat
goto :EOF

:END
echo.
echo Для запуска сервера используй: start.bat
echo.
pause
