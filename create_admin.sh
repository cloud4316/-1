#!/usr/bin/env bash
# Запуск: bash create_admin.sh
PYTHON=python
python --version 2>/dev/null || PYTHON=python3
echo "============================================================"
echo " Создание учётной записи преподавателя"
echo "============================================================"
echo ""
echo "Преподаватель входит через /admin/ или /login/ по логину."
echo "После создания он получит доступ к панели /teacher/"
echo ""
$PYTHON manage.py createsuperuser
echo ""
echo "Готово! Войдите как преподаватель через /login/"
echo "используя логин (username), который вы только что задали."
echo "Или войдите в Django Admin: /admin/"
