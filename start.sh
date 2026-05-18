#!/usr/bin/env bash
PYTHON=python; python --version &>/dev/null || PYTHON=python3
PORT=8000

# Проверяем БД
if ! $PYTHON manage.py migrate --check &>/dev/null; then
    echo "[!] БД не настроена. Запускаем установку..."
    $PYTHON manage.py migrate --run-syncdb
    $PYTHON manage.py seed_works   2>/dev/null | grep -v DEBUG
    $PYTHON manage.py seed_theory  2>/dev/null | grep -v DEBUG
    $PYTHON manage.py seed_quizzes 2>/dev/null | grep -v DEBUG
    $PYTHON manage.py create_default_admin 2>/dev/null | grep -v DEBUG
    $PYTHON manage.py collectstatic --noinput --clear 2>/dev/null | tail -1
    echo "[OK] Установка завершена."
fi

LOCAL_IP=$($PYTHON -c "import socket; s=socket.socket(); s.connect(('8.8.8.8',80)); print(s.getsockname()[0]); s.close()" 2>/dev/null || echo "127.0.0.1")

echo "============================================================"
echo " AlgorithmMaster — Сервер запускается"
echo ""
echo "  На этом компьютере : http://127.0.0.1:$PORT/"
echo "  В локальной сети   : http://$LOCAL_IP:$PORT/"
echo "  Панель препод.     : http://127.0.0.1:$PORT/teacher/"
echo ""
echo "  Для остановки: Ctrl+C"
echo "============================================================"
echo ""
$PYTHON -m waitress --host=0.0.0.0 --port=$PORT --threads=8 algorithm_site.wsgi:application
