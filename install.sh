#!/usr/bin/env bash
# Установщик AlgorithmMaster для Git Bash / Linux / macOS
# Запуск: bash install.sh

set -e

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       AlgorithmMaster — Установщик (Git Bash / Linux)       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ── Определяем команду python ───────────────────────────────────────────────
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        VER=$("$cmd" -c "import sys; print(sys.version_info.major, sys.version_info.minor)")
        MAJOR=$(echo $VER | cut -d' ' -f1)
        MINOR=$(echo $VER | cut -d' ' -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

# ── ШАГ 1: Python ───────────────────────────────────────────────────────────
echo "[1/6] Проверка Python 3.10+..."

if [ -z "$PYTHON" ]; then
    echo "    Python 3.10+ не найден. Попытка установки..."
    
    # Windows Git Bash — предлагаем скачать
    if [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]]; then
        echo ""
        echo "    [ОШИБКА] Установи Python вручную:"
        echo "    1. Перейди на https://python.org/downloads"
        echo "    2. Скачай Python 3.12"
        echo "    3. При установке отметь 'Add Python to PATH'"
        echo "    4. Перезапусти Git Bash и запусти install.sh снова"
        exit 1
    
    # Ubuntu / Debian
    elif command -v apt-get &>/dev/null; then
        echo "    Устанавливаем через apt..."
        sudo apt-get update -q && sudo apt-get install -y python3 python3-pip
        PYTHON=python3
    
    # macOS
    elif command -v brew &>/dev/null; then
        echo "    Устанавливаем через Homebrew..."
        brew install python@3.12
        PYTHON=python3
    
    else
        echo "    [ОШИБКА] Не могу установить Python автоматически."
        echo "    Установи Python 3.10+ вручную: https://python.org"
        exit 1
    fi
fi

echo "    OK: $($PYTHON --version)"

# ── ШАГ 2: pip ──────────────────────────────────────────────────────────────
echo ""
echo "[2/6] Проверка pip..."
if ! $PYTHON -m pip --version &>/dev/null; then
    echo "    Устанавливаем pip..."
    $PYTHON -m ensurepip --upgrade 2>/dev/null || \
    curl https://bootstrap.pypa.io/get-pip.py | $PYTHON
fi
echo "    OK"

# ── ШАГ 3: Зависимости (только недостающие) ─────────────────────────────────
echo ""
echo "[3/6] Проверка и установка зависимостей..."

install_if_missing() {
    local module="$1"
    local package="$2"
    if ! $PYTHON -c "import $module" 2>/dev/null; then
        echo "    Устанавливаем $package..."
        $PYTHON -m pip install "$package" --quiet --break-system-packages 2>/dev/null || \
        $PYTHON -m pip install "$package" --quiet
    else
        echo "    OK: $package (уже установлен)"
    fi
}

install_if_missing "django"    "django==5.2.6"
install_if_missing "waitress"  "waitress==3.0.1"
install_if_missing "whitenoise" "whitenoise==6.8.2 openpyxl==3.1.5"
install_if_missing    
install_if_missing "PIL"       
install_if_missing   

echo "    Все зависимости установлены"

# ── ШАГ 4: Миграции ─────────────────────────────────────────────────────────
echo ""
echo "[4/6] Создание базы данных..."
$PYTHON manage.py migrate --run-syncdb 2>/dev/null | grep -E "OK|Apply|Error" || true
echo "    OK"

# ── ШАГ 5: Данные ───────────────────────────────────────────────────────────
echo ""
echo "[5/6] Заполнение данными..."
$PYTHON manage.py seed_works   2>/dev/null | grep -v DEBUG || true
$PYTHON manage.py seed_theory  2>/dev/null | grep -v DEBUG || true
$PYTHON manage.py seed_quizzes 2>/dev/null | grep -v DEBUG || true
$PYTHON manage.py create_default_admin 2>/dev/null | grep -v DEBUG

# ── ШАГ 6: Статика ──────────────────────────────────────────────────────────
echo ""
echo "[6/6] Сбор статических файлов..."
$PYTHON manage.py collectstatic --noinput --clear 2>/dev/null | tail -1 || true
echo "    OK"

# ── Итог ────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  Установка завершена!                        ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Логин преподавателя:  admin                                 ║"
echo "║  Пароль:               admin                                 ║"
echo "║                                                              ║"
echo "║  ВАЖНО: смените пароль после первого входа!                  ║"
echo "║  Перейди: http://127.0.0.1:8000/admin/                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
read -rp "Запустить сервер прямо сейчас? (y/n): " START
if [[ "$START" =~ ^[Yy]$ ]]; then
    bash start.sh
fi
