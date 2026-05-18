@echo off
echo ========================================
echo    Запуск Django сервера в локальной сети
echo ========================================
echo.

REM Получаем IP адрес компьютера
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set "ip=%%a"
    goto :found
)
:found
set ip=%ip: =%

echo Ваш IP адрес: %ip%
echo.
echo Сервер будет доступен по адресам:
echo   - Локально: http://127.0.0.1:8000
echo   - В сети:   http://%ip%:8000
echo.
echo ========================================
echo Для остановки сервера нажмите Ctrl+C
echo ========================================
echo.

REM Запускаем Django сервер на всех интерфейсах
python manage.py runserver 0.0.0.0:8000

pause