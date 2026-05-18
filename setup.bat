@echo off
chcp 65001 >nul
title Установка ОАИП-сайт

echo ============================================================
echo  Первоначальная установка сайта ОАИП
echo ============================================================
echo.

REM Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден. Установи Python 3.11+ с python.org
    pause & exit /b 1
)
echo [OK] Python найден

REM Устанавливаем зависимости
echo.
echo [1/4] Установка зависимостей...
pip install -r requirements.txt --quiet
if errorlevel 1 ( echo [ОШИБКА] pip install завершился с ошибкой & pause & exit /b 1 )
echo [OK] Зависимости установлены

REM Миграции
echo.
echo [2/4] Применение миграций базы данных...
python manage.py migrate --run-syncdb
if errorlevel 1 ( echo [ОШИБКА] migrate завершился с ошибкой & pause & exit /b 1 )
echo [OK] База данных готова

REM Заполнение тестовыми работами
echo.
echo [3/4] Заполнение базы практическими работами...
python manage.py seed_works
if errorlevel 1 ( echo [ПРЕДУПРЕЖДЕНИЕ] seed_works — данные уже есть или ошибка )
echo [OK] Практические работы добавлены

echo.
echo [3b/4] Заполнение теоретическими материалами...
python manage.py seed_theory
if errorlevel 1 ( echo [ПРЕДУПРЕЖДЕНИЕ] seed_theory — данные уже есть или ошибка )
echo [OK] Теория добавлена

echo.
echo [3c/4] Заполнение тестами...
python manage.py seed_quizzes
python manage.py create_default_admin
if errorlevel 1 ( echo [ПРЕДУПРЕЖДЕНИЕ] seed_quizzes — данные уже есть или ошибка )
echo [OK] Тесты добавлены

REM Сбор статики
echo.
echo [4/4] Сбор статических файлов...
python manage.py collectstatic --noinput --clear
if errorlevel 1 ( echo [ОШИБКА] collectstatic завершился с ошибкой & pause & exit /b 1 )
echo [OK] Статика собрана

echo.
echo ============================================================
echo  Установка завершена!
echo  Теперь запусти start.bat для запуска сервера.
echo ============================================================
echo.
pause
