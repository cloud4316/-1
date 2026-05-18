#!/usr/bin/env bash
# Запуск: bash setup.sh
set -e
echo "============================================================"
echo " Установка сайта ОАИП"
echo "============================================================"

echo ""
echo "[1/5] Проверка Python..."
python --version 2>/dev/null || python3 --version
PYTHON=python
python --version 2>/dev/null || PYTHON=python3

echo ""
echo "[2/5] Установка зависимостей..."
$PYTHON -m pip install -r requirements.txt --quiet
echo "OK: зависимости установлены"

echo ""
echo "[3/5] Миграции базы данных..."
$PYTHON manage.py migrate --run-syncdb
echo "OK: база данных готова"

echo ""
echo "[4/5] Заполнение данными..."
$PYTHON manage.py seed_works   && echo "OK: практические работы"
$PYTHON manage.py seed_theory  && echo "OK: теория"
$PYTHON manage.py seed_quizzes
$PYTHON manage.py create_default_admin 2>/dev/null | grep -v DEBUG && echo "OK: тесты"

echo ""
echo "[5/5] Сбор статики..."
$PYTHON manage.py collectstatic --noinput --clear
echo "OK: статика собрана"

echo ""
echo "============================================================"
echo " Готово! Теперь запусти:  bash start.sh"
echo "============================================================"
