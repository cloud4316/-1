#!/usr/bin/env bash
PYTHON=python; python --version &>/dev/null || PYTHON=python3
PORT=8000

# Включаем DEBUG
touch DEBUG.lock

# Миграции
if ! $PYTHON manage.py migrate --check &>/dev/null; then
    echo "[!] Применяем миграции..."
    $PYTHON manage.py migrate --run-syncdb
fi

LOCAL_IP=$($PYTHON -c "import socket; s=socket.socket(); s.connect(('8.8.8.8',80)); print(s.getsockname()[0]); s.close()" 2>/dev/null || echo "127.0.0.1")

echo "============================================================"
echo " AlgorithmMaster — DEV-сервер (авто-перезагрузка браузера)"
echo ""
echo "  Локально : http://127.0.0.1:$PORT/"
echo "  Сеть     : http://$LOCAL_IP:$PORT/"
echo ""
echo "  Браузер обновляется автоматически при изменении файлов!"
echo "  Для остановки: Ctrl+C"
echo "============================================================"
echo ""

$PYTHON manage.py runserver 0.0.0.0:$PORT
