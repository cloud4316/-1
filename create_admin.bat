@echo off
chcp 65001 >nul
title Создание администратора

echo Создание администратора сайта
echo.
python manage.py createsuperuser
pause
