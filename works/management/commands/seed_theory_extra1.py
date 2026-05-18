"""python manage.py seed_theory_extra1

Расширяет модули 1-4: добавляет 2 новых урока в каждый.
Добавляет новые модули 19 (Тестирование) и 20 (Алгоритмическое мышление).
"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson


def tip(t):  return f'<div class="tip">💡 {t}</div>'
def warn(t): return f'<div class="warning">⚠️ {t}</div>'
def info(t): return f'<div class="tip" style="background:#e0f2fe;border-color:#0284c7">ℹ️ {t}</div>'


def table(headers, rows):
    th = ''.join(f'<th>{c}</th>' for c in headers)
    trs = ''.join(
        '<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
        for r in rows
    )
    return f'<table class="theory-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


# Уроки, добавляемые в существующие модули.
# Ключ — точное название модуля из БД.
EXTRA_LESSONS = {

    # ═══════════════════════════════════════════════════════════════
    # МОДУЛЬ 1 — ВВЕДЕНИЕ В ПРОГРАММИРОВАНИЕ
    # ═══════════════════════════════════════════════════════════════
    'Введение в программирование': [
        {
            'title': 'Ввод данных: input() и преобразование типов',
            'order': 3,
            'estimated_minutes': 65,
            'content': '''
<h2>Функция input()</h2>
<p>Большинство реальных программ читают данные от пользователя, из файла или сети. В Python простейший способ получить данные от пользователя — функция <code>input()</code>.</p>

<pre><code>значение = input(подсказка)</code></pre>

<ul>
  <li>Выводит <code>подсказку</code> (необязательна)</li>
  <li>Ждёт, пока пользователь нажмёт Enter</li>
  <li><strong>Всегда возвращает строку (str)</strong> — даже если ввели число!</li>
</ul>

<pre><code>name = input("Как тебя зовут? ")
print(f"Привет, {name}!")

age_str = input("Сколько тебе лет? ")
print(type(age_str))   # <class 'str'>
print(age_str + 1)     # TypeError: нельзя сложить str и int!</code></pre>

''' + warn('input() ВСЕГДА возвращает строку. Прежде чем выполнять числовые операции, преобразуй значение через int() или float().') + '''

<h2>Преобразование типов</h2>
''' + table(
    ['Функция', 'Из чего', 'Пример', 'Результат'],
    [
        ['int(x)', 'str, float, bool', 'int("42")', '42'],
        ['float(x)', 'str, int, bool', 'float("3.14")', '3.14'],
        ['str(x)', 'Любого типа', 'str(100)', '"100"'],
        ['bool(x)', 'Любого типа', 'bool(0)', 'False'],
        ['list(x)', 'Итерируемого', 'list("abc")', "['a','b','c']"],
        ['tuple(x)', 'Итерируемого', 'tuple([1,2])', '(1, 2)'],
    ]
) + '''

<h3>Распространённые ошибки при конвертации</h3>
<pre><code># ValueError — неверный формат
int("abc")       # ValueError
float("3,14")    # ValueError (нужна точка, не запятая!)
int("3.14")      # ValueError (int не понимает дроби)

# Правильно:
int(float("3.14"))   # 3  ← сначала в float, потом в int
int("3.14".replace(",", "."))  # если пришло "3,14"</code></pre>

<h2>Ввод нескольких значений</h2>
<pre><code># Способ 1: несколько input() подряд
a = int(input("Первое число: "))
b = int(input("Второе число: "))

# Способ 2: через split() (числа на одной строке через пробел)
a, b = map(int, input("Два числа через пробел: ").split())

# Способ 3: список из строки
numbers = list(map(int, input("Числа: ").split()))
print(f"Сумма: {sum(numbers)}")</code></pre>

''' + tip('<code>map(int, iterable)</code> — применяет функцию int() к каждому элементу. Это быстрее и короче, чем list comprehension в данном случае.') + '''

<h2>Валидация ввода</h2>
<p>Пользователи вводят что угодно. Программа должна это обрабатывать корректно:</p>

<pre><code># Простая проверка: isdigit()
value = input("Введи целое число: ")
if value.lstrip("-").isdigit():
    n = int(value)
    print(f"Квадрат: {n ** 2}")
else:
    print("Ошибка: введено не целое число")

# Паттерн «цикл до верного ввода»
while True:
    raw = input("Введи возраст (1-120): ")
    if raw.isdigit() and 1 <= int(raw) <= 120:
        age = int(raw)
        break
    print("Некорректный ввод. Попробуй снова.")
print(f"Твой возраст: {age}")</code></pre>

<h2>Строки и числа: форматирование вывода</h2>
<pre><code># f-строки с выравниванием
items = [("Яблоко", 15.50), ("Банан", 8.00), ("Вишня", 45.90)]
print(f"{'Товар':<15} {'Цена':>8}")
print("-" * 24)
for name, price in items:
    print(f"{name:<15} {price:>7.2f}₽")
total = sum(p for _, p in items)
print("-" * 24)
print(f"{'ИТОГО':<15} {total:>7.2f}₽")</code></pre>

''' + info('Форматирование: <code>&lt;</code> — выравнивание влево, <code>&gt;</code> — вправо, <code>^</code> — по центру. Число перед символом — ширина поля.') + '''
''',
            'code_example': '''# Калькулятор с вводом от пользователя

def get_number(prompt):
    """Безопасное считывание числа."""
    while True:
        raw = input(prompt)
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            print(f"  Ошибка: '{raw}' не является числом. Попробуй снова.")

def get_operator():
    """Считывание оператора."""
    valid = {"+", "-", "*", "/", "**", "//", "%"}
    while True:
        op = input("Оператор (+, -, *, /, **, //, %): ").strip()
        if op in valid:
            return op
        print(f"  Неверный оператор. Доступны: {', '.join(sorted(valid))}")

# Пример запуска (раскомментируй):
# a = get_number("Первое число: ")
# op = get_operator()
# b = get_number("Второе число: ")
# ...

# Демонстрация без ввода:
print("Таблица преобразований:")
samples = ["42", "3.14", "-7", "0", "True", "1e6"]
print(f"{'Строка':<10} {'int':>8} {'float':>10} {'bool':>6}")
print("-" * 36)
for s in samples:
    try:
        i = int(float(s))
    except ValueError:
        i = "—"
    try:
        f = float(s)
    except ValueError:
        f = "—"
    b = bool(float(s)) if s not in ("True", "False") else (s == "True")
    print(f"{s:<10} {str(i):>8} {str(f):>10} {str(b):>6}")

# Ввод нескольких чисел через split
data = "10 20 30 40 50"           # имитация ввода
numbers = list(map(int, data.split()))
print(f"\\nЧисла: {numbers}")
print(f"Сумма: {sum(numbers)}")
print(f"Среднее: {sum(numbers)/len(numbers):.1f}")
print(f"Мин: {min(numbers)}, Макс: {max(numbers)}")
'''
        },
        {
            'title': 'Синтаксические и логические ошибки. Чтение traceback',
            'order': 4,
            'estimated_minutes': 60,
            'content': '''
<h2>Три вида ошибок в программировании</h2>

''' + table(
    ['Вид ошибки', 'Когда возникает', 'Пример', 'Как найти'],
    [
        ['Синтаксическая (SyntaxError)', 'До запуска, при чтении кода', 'пропущена «:», лишняя скобка', 'Сразу при запуске, IDE подсвечивает'],
        ['Времени выполнения (RuntimeError)', 'Во время выполнения', 'деление на ноль, нет файла', 'Traceback при запуске'],
        ['Логическая', 'Всегда — программа работает, но неверно', 'неверная формула', 'Только тестирование'],
    ]
) + '''

<h2>Синтаксические ошибки</h2>
<p>Python обнаруживает их до старта. IDE подсвечивает красным:</p>

<pre><code># SyntaxError: Missing colon
if x > 0
    print(x)

# SyntaxError: Unmatched bracket
result = (1 + 2
print(result)

# IndentationError: неверный отступ
def func():
print("hello")  # не отступлен!</code></pre>

''' + warn('IndentationError — особая разновидность SyntaxError. В Python отступ — часть синтаксиса! Смешивать пробелы и табуляцию нельзя.') + '''

<h2>Как читать Traceback</h2>
<p>Traceback — трассировка стека вызовов. Читай <strong>снизу вверх</strong>:</p>

<pre><code>Traceback (most recent call last):
  File "main.py", line 12, in &lt;module&gt;    ← точка вызова
    result = process(data)
  File "main.py", line 8, in process       ← функция
    return data[10]
  File "main.py", line 8, in process
IndexError: list index out of range         ← ТИП и СООБЩЕНИЕ ← читать первым</code></pre>

<ol>
  <li>Смотри на <strong>последнюю строку</strong>: тип ошибки и её описание</li>
  <li>Смотри на <strong>File, line N</strong> рядом с ошибкой: где именно</li>
  <li>Если нужно — читай цепочку вызовов выше</li>
</ol>

<h2>Частые ошибки начинающих</h2>

''' + table(
    ['Ошибка', 'Причина', 'Исправление'],
    [
        ['NameError: name \'x\' is not defined', 'Переменная не создана или опечатка', 'Проверь имена, порядок определений'],
        ['TypeError: can only concatenate str...', 'Попытка сложить str и int', 'Явно преобразуй: str(n) или int(s)'],
        ['IndexError: list index out of range', 'Индекс вне диапазона', 'Проверь len(lst), используй lst[-1]'],
        ['ZeroDivisionError', 'Деление на ноль', 'Добавь проверку: if b != 0'],
        ['IndentationError', 'Неверный отступ', '4 пробела, без табуляции'],
        ['SyntaxError: invalid syntax', 'Нарушение синтаксиса', 'Проверь двоеточия, скобки, кавычки'],
        ['AttributeError: NoneType has no ...', 'Функция вернула None', 'Проверь return в функции'],
        ['RecursionError', 'Нет базового случая в рекурсии', 'Добавь условие остановки'],
    ]
) + '''

<h2>Логические ошибки — самые опасные</h2>
<p>Программа запускается без ошибок, но даёт неверный результат:</p>

<pre><code># Ошибка: периметр вместо площади
def area_of_rectangle(a, b):
    return 2 * (a + b)  # это ПЕРИМЕТР!

# Ошибка: off-by-one
for i in range(1, n):   # должно быть range(1, n+1)
    total += i

# Ошибка: целочисленное деление вместо вещественного
average = total / len(items)  # в Python 3 правильно, но в 2 была бы ошибка
# Если total и len() оба int — всё равно float (/ всегда float в Python 3)

# Ошибка: изменение списка во время итерации
for item in items:
    if some_condition(item):
        items.remove(item)   # ОПАСНО! Пропустит элементы
# Правильно: итерируй по копии
for item in items[:]:
    if some_condition(item):
        items.remove(item)</code></pre>

<h2>Отладка: техники</h2>

<h3>1. print-отладка</h3>
<pre><code>def calculate(data):
    print(f"DEBUG: data = {data}")      # добавляем print
    result = process(data)
    print(f"DEBUG: result = {result}")  # смотрим промежуточный результат
    return result</code></pre>

<h3>2. assert — утверждения</h3>
<pre><code>def factorial(n):
    assert n >= 0, f"factorial требует n >= 0, получено {n}"
    if n == 0:
        return 1
    return n * factorial(n - 1)

factorial(-1)  # AssertionError: factorial требует n >= 0, получено -1</code></pre>

<h3>3. Встроенный отладчик pdb</h3>
<pre><code>import pdb
pdb.set_trace()   # программа остановится здесь, можно смотреть переменные
# В Python 3.7+: просто breakpoint()</code></pre>

''' + tip('Используй print-отладку для простых случаев. Для сложных — breakpoint() или отладчик в IDE (F9 в VS Code/PyCharm).') + '''
''',
            'code_example': '''# Демонстрация чтения ошибок и отладки

# 1. Находим и исправляем ошибки
def buggy_average(numbers):
    """Содержит логическую ошибку."""
    total = 0
    for n in numbers:
        total = total + n   # OK
    # Ошибка: делим на фиксированное 10, а не на длину списка
    return total / 10       # НЕВЕРНО

def correct_average(numbers):
    """Правильная версия."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [80, 90, 70, 85, 95]
print(f"Неверное среднее: {buggy_average(data):.1f}")     # 84.0 (совпало!)
data2 = [80, 90, 70]
print(f"Неверное среднее: {buggy_average(data2):.1f}")    # 24.0 (неверно!)
print(f"Верное среднее:   {correct_average(data2):.1f}")  # 80.0

# 2. Защита от ошибок через assert
def safe_sqrt(x):
    assert x >= 0, f"Корень из отрицательного числа: {x}"
    return x ** 0.5

try:
    print(safe_sqrt(16))    # 4.0
    print(safe_sqrt(-4))    # AssertionError
except AssertionError as e:
    print(f"Ошибка утверждения: {e}")

# 3. Типичные ошибки и их исправления
print("\\n--- Типичные ошибки ---")

# TypeError: конкатенация str + int
year = 2026
# print("Год: " + year)  ← TypeError
print("Год: " + str(year))   # исправлено
print(f"Год: {year}")        # лучший способ

# IndexError: защита
lst = [10, 20, 30]
idx = 5
if 0 <= idx < len(lst):
    print(lst[idx])
else:
    print(f"Индекс {idx} вне диапазона [0, {len(lst)-1}]")

# ZeroDivisionError: защита
def safe_divide(a, b):
    if b == 0:
        return None
    return a / b

result = safe_divide(10, 0)
if result is None:
    print("Деление на ноль невозможно")
else:
    print(f"Результат: {result}")

# 4. Off-by-one — классическая логическая ошибка
print("\\n--- Сумма 1..10 ---")
# Ошибка:
total = sum(range(1, 10))     # 1+2+...+9 = 45, пропустили 10!
print(f"Неверно (range(1,10)):  {total}")

# Правильно:
total = sum(range(1, 11))     # 1+2+...+10 = 55
print(f"Верно   (range(1,11)): {total}")
'''
        },
    ],

    # ═══════════════════════════════════════════════════════════════
    # МОДУЛЬ 2 — ПЕРЕМЕННЫЕ И ТИПЫ ДАННЫХ
    # ═══════════════════════════════════════════════════════════════
    'Переменные и типы данных': [
        {
            'title': 'bool и None: логический тип и отсутствие значения',
            'order': 4,
            'estimated_minutes': 65,
            'content': '''
<h2>Логический тип bool</h2>
<p><code>bool</code> — подтип <code>int</code>. Имеет только два значения: <code>True</code> и <code>False</code>. В числовых выражениях <code>True == 1</code>, <code>False == 0</code>.</p>

<pre><code>print(True + True)      # 2
print(True * 5)         # 5
print(False * 100)      # 0
print(int(True))        # 1
print(int(False))       # 0
print(type(True))       # <class 'bool'></code></pre>

''' + info('bool — подкласс int. Это позволяет считать «количество True» через sum(): sum([True, False, True, True]) == 3') + '''

<h2>Операторы сравнения возвращают bool</h2>
<pre><code>result = 5 > 3          # True
check = "abc" == "abc"  # True
test  = 10 in [1,2,3]   # False

# Все операторы: ==  !=  >  <  >=  <=  is  is not  in  not in</code></pre>

<h2>Truthy и Falsy — детально</h2>
<p>В Python любое значение неявно конвертируется в bool в логических выражениях:</p>

''' + table(
    ['Значение', 'bool(значение)', 'Тип'],
    [
        ['0', 'False', 'int'],
        ['0.0', 'False', 'float'],
        ['0j', 'False', 'complex'],
        ['""', 'False', 'str'],
        ['[]', 'False', 'list'],
        ['()', 'False', 'tuple'],
        ['{}', 'False', 'dict'],
        ['set()', 'False', 'set'],
        ['None', 'False', 'NoneType'],
        ['False', 'False', 'bool'],
        ['Всё остальное', 'True', 'любой'],
    ]
) + '''

<pre><code># Практические применения:
users = []
if users:                    # вместо if len(users) > 0
    print("Есть пользователи")

name = input("Имя: ")
if name:                     # вместо if name != ""
    print(f"Привет, {name}")

result = get_data()
if result is not None:       # правильная проверка на None
    process(result)</code></pre>

<h2>Функции any() и all()</h2>

''' + table(
    ['Функция', 'Возвращает True если', 'Пример'],
    [
        ['any(iterable)', 'Хотя бы один элемент правдив', 'any([0, 0, 1, 0]) → True'],
        ['all(iterable)', 'Все элементы правдивы', 'all([1, 2, 3]) → True'],
        ['any([])', 'Всегда False для пустого', 'any([]) → False'],
        ['all([])', 'Всегда True для пустого!', 'all([]) → True'],
    ]
) + '''

<pre><code># any — хотя бы один прошёл
scores = [45, 72, 88, 61, 39]
has_excellent = any(s >= 90 for s in scores)
print(f"Есть отличники: {has_excellent}")  # False

# all — все прошли минимум
passed_all = all(s >= 60 for s in scores)
print(f"Все сдали: {passed_all}")          # False

# Практический пример
def is_valid_student(s):
    return (
        all([s.get("name"), s.get("group")])   # оба поля заполнены
        and s.get("age", 0) >= 16              # возраст допустимый
    )</code></pre>

<h2>None — отсутствие значения</h2>
<p><code>None</code> — единственный объект типа <code>NoneType</code>. Используется для обозначения «нет значения», «ещё не задано», «функция ничего не вернула».</p>

<pre><code># Когда функция ничего не возвращает
def greet(name):
    print(f"Привет, {name}")

result = greet("Иван")
print(result)    # None

# Значение по умолчанию до инициализации
winner = None
for player in players:
    if player.score > best_score:
        winner = player          # присваивается когда найдено

if winner is not None:
    print(f"Победитель: {winner.name}")

# Аргумент по умолчанию (лучше None, чем [])
def add_tag(item, tags=None):
    if tags is None:
        tags = []
    tags.append(item)
    return tags</code></pre>

''' + warn('Никогда не сравнивай с None через ==. Правильно: <code>x is None</code> или <code>x is not None</code>. Причина: некоторые объекты переопределяют оператор ==.') + '''
''',
            'code_example': '''# bool, None и логические функции

# 1. Подсчёт через sum(bool)
scores = [72, 88, 55, 93, 67, 81, 49, 95, 78, 60]
n = len(scores)

passed = sum(1 for s in scores if s >= 60)
excellent = sum(s >= 90 for s in scores)   # True считается как 1
failed = sum(s < 60 for s in scores)

print(f"Всего: {n}")
print(f"Сдали:     {passed}/{n} ({passed/n*100:.0f}%)")
print(f"Отличники: {excellent}/{n}")
print(f"Не сдали:  {failed}/{n}")

# 2. any() и all() для проверки данных
students = [
    {"name": "Иван",   "group": "А1", "age": 20, "gpa": 4.5},
    {"name": "",       "group": "А1", "age": 21, "gpa": 4.0},   # пустое имя
    {"name": "Пётр",   "group": "",   "age": 19, "gpa": 3.8},   # нет группы
    {"name": "Анна",   "group": "Б2", "age": 15, "gpa": 4.9},   # слишком молодой
    {"name": "Дмитрий","group": "В3", "age": 22, "gpa": 4.2},
]

def validate(s):
    errors = []
    if not s.get("name"):        errors.append("нет имени")
    if not s.get("group"):       errors.append("нет группы")
    if s.get("age", 0) < 16:    errors.append("возраст < 16")
    return errors

print("\\nВалидация студентов:")
for s in students:
    errors = validate(s)
    name = s["name"] or "(пусто)"
    status = "✓" if not errors else "✗ " + ", ".join(errors)
    print(f"  {name:<12} {status}")

# 3. None как сигнал «не найдено»
database = {
    "u001": {"name": "Иван",  "score": 85},
    "u002": {"name": "Мария", "score": 92},
}

def get_user(uid):
    return database.get(uid)   # None если нет

for uid in ["u001", "u999", "u002"]:
    user = get_user(uid)
    if user is not None:
        print(f"  {uid}: {user['name']} — {user['score']} баллов")
    else:
        print(f"  {uid}: пользователь не найден")

# 4. Истинность разных значений
print("\\nТаблица истинности:")
values = [0, 1, -1, 0.0, 0.1, "", "a", [], [0], {}, {"k": 0}, None, False, True]
for v in values:
    print(f"  bool({str(v):<10}) = {bool(v)}")
'''
        },
        {
            'title': 'Явное и неявное преобразование типов',
            'order': 5,
            'estimated_minutes': 70,
            'content': '''
<h2>Два вида преобразований</h2>

''' + table(
    ['Вид', 'Описание', 'Пример'],
    [
        ['Явное (explicit)', 'Программист явно вызывает функцию конвертации', 'int("42"), str(3.14)'],
        ['Неявное (implicit)', 'Python автоматически при смешении типов', '1 + 1.0 → 2.0 (int→float)'],
    ]
) + '''

<h2>Неявное преобразование</h2>
<p>Python делает неявную конвертацию только «безопасную» — от меньшего к большему:</p>

<pre><code>print(1 + 1.0)      # 2.0 (int → float, нет потери точности)
print(True + 1)     # 2   (bool → int, нет потери)
print(True + 1.5)   # 2.5 (bool → float)

# Python НЕ делает неявно:
print("5" + 3)      # TypeError! Нет автоматического str→int</code></pre>

<h2>Иерархия числовых типов</h2>
<pre><code>bool → int → float → complex</code></pre>
<p>При смешении Python приводит к «большему» типу:</p>
<pre><code>True + 1       # bool + int  → int (2)
1 + 2.0        # int + float → float (3.0)
1.0 + (1+0j)   # float + complex → complex ((2+0j))</code></pre>

<h2>Явное преобразование: детали</h2>

<h3>int()</h3>
<pre><code>int("42")          # 42
int("-17")         # -17
int(3.99)          # 3 (обрезает, не округляет!)
int(True)          # 1
int("0b1010", 0)   # 10 (авто-определение системы счисления)
int("FF", 16)      # 255 (16-ричное)
int("101", 2)      # 5 (двоичное)</code></pre>

''' + warn('int(3.99) → 3, не 4! Это ОБРЕЗАНИЕ (truncation), не округление. Для округления используй round().') + '''

<h3>float()</h3>
<pre><code>float("3.14")       # 3.14
float("1e-5")       # 0.00001 (научная нотация)
float("inf")        # math.inf
float("nan")        # math.nan
float(True)         # 1.0
# float("3,14")     # ValueError — запятая, не точка!</code></pre>

<h3>str()</h3>
<pre><code>str(42)             # "42"
str(3.14)           # "3.14"
str(True)           # "True"
str([1, 2, 3])      # "[1, 2, 3]"
str(None)           # "None"

# repr() — «техническое» представление
repr("hello")       # "'hello'" (с кавычками!)
repr([1, "a"])      # "[1, 'a']"</code></pre>

<h3>bool()</h3>
<pre><code>bool(0)      # False
bool(42)     # True
bool("")     # False
bool("0")    # True! (непустая строка)
bool([])     # False
bool(None)   # False</code></pre>

''' + warn('"0" (строка) → True, хотя int("0") → 0 → False. Это частый источник ошибок при работе с пользовательским вводом.') + '''

<h2>Числовые системы</h2>
''' + table(
    ['Система', 'Префикс', 'Функция в/из', 'Пример'],
    [
        ['Двоичная (base 2)', '0b', 'bin(n) / int(s, 2)', 'bin(10) → "0b1010"'],
        ['Восьмеричная (base 8)', '0o', 'oct(n) / int(s, 8)', 'oct(255) → "0o377"'],
        ['Десятичная (base 10)', '—', 'str(n) / int(s)', 'str(42) → "42"'],
        ['Шестнадцатеричная (base 16)', '0x', 'hex(n) / int(s, 16)', 'hex(255) → "0xff"'],
    ]
) + '''

<h2>ord() и chr() — символы и коды</h2>
<pre><code>ord("A")     # 65  (код символа в Unicode)
ord("a")     # 97
ord("я")     # 1103

chr(65)      # "A"
chr(1072)    # "а"

# Практика: шифр Цезаря
def caesar(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result

print(caesar("Hello, World!", 3))  # "Khoor, Zruog!"</code></pre>
''',
            'code_example': '''# Преобразования типов: практика

import math

# 1. Таблица конвертации
print("Явные преобразования:")
print(f"{'Значение':<12} {'int':>6} {'float':>8} {'str':>10} {'bool':>6}")
print("-" * 44)
tests = [42, 3.14, True, False, 0, "7", 1e3]
for v in tests:
    try: i = int(v)
    except: i = "err"
    try: f = float(v)
    except: f = "err"
    s = str(v)
    b = bool(v)
    print(f"{str(v):<12} {str(i):>6} {str(f):>8} {s:>10} {str(b):>6}")

# 2. Числовые системы
print("\\nЧисловые системы:")
for n in [0, 1, 10, 42, 127, 255]:
    print(f"  {n:>4} | bin={bin(n):<12} | oct={oct(n):<8} | hex={hex(n):<6}")

# 3. Работа с ASCII/Unicode
print("\\nASCII таблица (32-126):")
for row_start in range(32, 127, 16):
    row = ""
    for code in range(row_start, min(row_start + 16, 127)):
        ch = chr(code)
        row += f"{code:3}:{ch} "
    print(f"  {row}")

# 4. Шифр Цезаря
def caesar(text, shift):
    result = []
    for ch in text:
        if "A" <= ch <= "Z":
            result.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        elif "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        else:
            result.append(ch)
    return "".join(result)

msg = "Python is Fun!"
enc = caesar(msg, 13)  # ROT13
dec = caesar(enc, 13)  # ROT13 дважды = оригинал
print(f"\\nШифр Цезаря (ROT13):")
print(f"  Оригинал:  {msg}")
print(f"  Зашифровано: {enc}")
print(f"  Расшифровано: {dec}")

# 5. Ловушка: int(float) обрезает
values = [1.1, 1.5, 1.9, 2.0, -1.1, -1.9]
print("\\nОкругление vs Обрезание:")
for v in values:
    print(f"  {v:>5}: int={int(v):>3}, round={round(v):>3}, "
          f"floor={math.floor(v):>3}, ceil={math.ceil(v):>3}")
'''
        },
    ],

    # ═══════════════════════════════════════════════════════════════
    # МОДУЛЬ 3 — УСЛОВНЫЕ ОПЕРАТОРЫ
    # ═══════════════════════════════════════════════════════════════
    'Условные операторы': [
        {
            'title': 'Вложенные условия и упрощение логики',
            'order': 2,
            'estimated_minutes': 75,
            'content': '''
<h2>Вложенные условия</h2>
<p>Условие внутри условия — частая необходимость, но легко уходит в «pyramid of doom»:</p>

<pre><code># Плохо: глубокая вложенность (pyramid of doom)
if user:
    if user.is_active:
        if user.has_permission("admin"):
            if data:
                process(data)

# Хорошо: guard clauses (ранние выходы)
if not user:
    return "Нет пользователя"
if not user.is_active:
    return "Пользователь неактивен"
if not user.has_permission("admin"):
    return "Нет прав"
if not data:
    return "Нет данных"
process(data)</code></pre>

''' + tip('Паттерн «guard clause»: проверяй ошибочные случаи первыми и делай ранний return. Это уменьшает вложенность и улучшает читаемость.') + '''

<h2>Законы де Моргана</h2>
<p>Математические законы, которые позволяют упростить сложные логические выражения:</p>

<ul>
  <li><code>not (A and B)</code> ≡ <code>not A or not B</code></li>
  <li><code>not (A or B)</code> ≡ <code>not A and not B</code></li>
</ul>

<pre><code># Пример: «не (взрослый и активный)»
# Вместо:
if not (age >= 18 and is_active):
    ...
# Эквивалентно (де Морган):
if age < 18 or not is_active:
    ...

# Пример: «не студент и не преподаватель»
# Вместо:
if not (role == "student" or role == "teacher"):
    ...
# Эквивалентно:
if role != "student" and role != "teacher":
    ...
# Ещё лучше:
if role not in ("student", "teacher"):
    ...</code></pre>

<h2>Приоритет логических операторов</h2>
''' + table(
    ['Приоритет', 'Оператор', 'Пример'],
    [
        ['Высший', 'not', 'not x > 0 → (not x) > 0 — осторожно!'],
        ['Средний', 'and', 'a and b and c'],
        ['Низший', 'or', 'a or b or c'],
    ]
) + '''

<pre><code># Частая ошибка: приоритет not
x = 5
print(not x > 3)        # False: (not 5) > 3 → 0 > 3 → False? НЕТ!
# Правильно: not (x > 3) → not True → False
# Фактически: not (5 > 3) == not True == False ← всё равно False, но логика разная

# Явные скобки убирают путаницу:
if (a > 0) and (b > 0) or (c == 0):
    ...  # читается: (a>0 and b>0) or c==0

# Без скобок тот же приоритет:
if a > 0 and b > 0 or c == 0:  # and выполняется раньше or
    ...</code></pre>

''' + warn('Всегда добавляй скобки в сложных логических выражениях. Приоритет <code>and/or</code> неочевиден многим читателям.') + '''

<h2>Цепочки сравнений</h2>
<pre><code># Python позволяет математические неравенства
if 0 < x < 100:    # x строго между 0 и 100
    ...

if 1 <= age <= 120:  # допустимый возраст
    ...

# Внимательно с цепочками — они эквивалентны and:
# a < b < c  ≡  a < b and b < c

# Не работает так, как кажется:
x = 5
print(1 < x < 10)    # True (правильно)
print(1 < x and x < 10)   # True (то же самое)</code></pre>

<h2>Оператор in для диапазонов значений</h2>
<pre><code># Вместо длинной цепочки or:
if day == "Сб" or day == "Вс":
    print("Выходной")

# Лаконично через in:
if day in ("Сб", "Вс"):
    print("Выходной")

# Числовые диапазоны:
FORBIDDEN = {403, 404, 500, 503}
if status_code in FORBIDDEN:
    handle_error(status_code)</code></pre>

<h2>Условное выражение vs if/else</h2>
<pre><code># Тернарный — только для простых случаев
label = "чётное" if n % 2 == 0 else "нечётное"

# if/else — когда нужна логика
if n % 2 == 0:
    label = "чётное"
    count_even += 1
else:
    label = "нечётное"
    count_odd += 1

# Никогда не злоупотребляй вложенным тернарным:
# result = a if x > 0 else (b if x < 0 else c)  ← плохо читается</code></pre>
''',
            'code_example': '''# Вложенные условия и упрощение логики

# 1. Классификация треугольников
def classify_triangle(a, b, c):
    # Guard clause: проверка корректности
    if a <= 0 or b <= 0 or c <= 0:
        return "Ошибка: стороны должны быть положительными"
    if a + b <= c or a + c <= b or b + c <= a:
        return "Не треугольник (нарушено неравенство треугольника)"

    # Классификация по сторонам
    if a == b == c:
        side_type = "равносторонний"
    elif a == b or b == c or a == c:
        side_type = "равнобедренный"
    else:
        side_type = "разносторонний"

    # Классификация по углам
    sides = sorted([a, b, c])
    a2, b2, c2 = sides[0]**2, sides[1]**2, sides[2]**2
    if a2 + b2 == c2:
        angle_type = "прямоугольный"
    elif a2 + b2 > c2:
        angle_type = "остроугольный"
    else:
        angle_type = "тупоугольный"

    return f"{side_type}, {angle_type}"

tests = [(3,4,5), (5,5,5), (5,5,3), (1,2,10), (0,3,4)]
for sides in tests:
    print(f"  {sides}: {classify_triangle(*sides)}")

# 2. Система скидок (упрощение через guard clauses)
def calculate_discount(price, quantity, is_premium):
    """Вычисляет скидку по правилам."""
    if price <= 0 or quantity <= 0:
        return 0.0

    discount = 0.0

    # Скидка за объём
    if quantity >= 100:
        discount = 0.20
    elif quantity >= 50:
        discount = 0.15
    elif quantity >= 10:
        discount = 0.10

    # Дополнительная скидка для премиум
    if is_premium:
        discount += 0.05

    # Максимальная скидка — 30%
    discount = min(discount, 0.30)

    return round(price * quantity * (1 - discount), 2)

cases = [
    (100, 5, False),
    (100, 15, False),
    (100, 60, True),
    (100, 120, True),
    (0, 10, True),
]
print("\\nСистема скидок:")
for price, qty, premium in cases:
    total = calculate_discount(price, qty, premium)
    label = "премиум" if premium else "обычный"
    print(f"  {price}₽ × {qty:>3} ({label:<8}) = {total:>9.2f}₽")

# 3. Законы де Моргана в действии
def check_access(user, resource):
    """Проверка доступа к ресурсу."""
    is_admin = user.get("role") == "admin"
    is_owner = user.get("id") == resource.get("owner_id")
    is_public = resource.get("public", False)
    is_banned = user.get("banned", False)

    # Явно запрещено
    if is_banned:
        return "Доступ запрещён: бан"

    # Полный доступ: администратор или владелец
    if is_admin or is_owner:
        return "Доступ разрешён"

    # Публичный ресурс — доступен всем незабаненным
    if is_public:
        return "Доступ разрешён (публичный)"

    return "Доступ запрещён"

admin = {"id": 1, "role": "admin"}
owner = {"id": 2, "role": "user"}
guest = {"id": 3, "role": "user"}
banned = {"id": 4, "role": "user", "banned": True}
res_priv = {"owner_id": 2, "public": False}
res_pub = {"owner_id": 2, "public": True}

for user, res, label in [
    (admin, res_priv, "admin/private"),
    (owner, res_priv, "owner/private"),
    (guest, res_priv, "guest/private"),
    (guest, res_pub, "guest/public"),
    (banned, res_pub, "banned/public"),
]:
    print(f"  {label:<20}: {check_access(user, res)}")
'''
        },
        {
            'title': 'Практические задачи на условные операторы',
            'order': 3,
            'estimated_minutes': 70,
            'content': '''
<h2>Задача 1: Игра «Камень, ножницы, бумага»</h2>
<p>Один из классических примеров разветвляющегося алгоритма. Три игрока, три пары сравнений:</p>
<ul>
  <li>Камень бьёт ножницы</li>
  <li>Ножницы режут бумагу</li>
  <li>Бумага накрывает камень</li>
</ul>

<pre><code>def play_rps(player, computer):
    if player == computer:
        return "Ничья"
    wins = {("камень", "ножницы"), ("ножницы", "бумага"), ("бумага", "камень")}
    return "Победа" if (player, computer) in wins else "Поражение"

# Альтернатива через словарь
BEATS = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}
def play(player, computer):
    if player == computer: return "Ничья"
    return "Победа" if BEATS[player] == computer else "Поражение"</code></pre>

<h2>Задача 2: FizzBuzz и обобщения</h2>
<p>Классическая задача: числа от 1 до N. Кратные 3 → Fizz, кратные 5 → Buzz, кратные 15 → FizzBuzz.</p>

<pre><code>def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:      # 15 ДОЛЖНО БЫТЬ ПЕРВЫМ!
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result</code></pre>

''' + warn('Порядок проверок важен! Если сначала проверить % 3, то числа кратные 15 выведут только "Fizz", а не "FizzBuzz".') + '''

<h2>Задача 3: Определение сезона по месяцу</h2>
<pre><code>SEASONS = {
    "Зима":  {12, 1, 2},
    "Весна": {3, 4, 5},
    "Лето":  {6, 7, 8},
    "Осень": {9, 10, 11},
}
MONTH_NAMES = {1:"Январь",2:"Февраль",3:"Март",4:"Апрель",
               5:"Май",6:"Июнь",7:"Июль",8:"Август",
               9:"Сентябрь",10:"Октябрь",11:"Ноябрь",12:"Декабрь"}

def get_season(month):
    if not 1 <= month <= 12:
        return "Некорректный месяц"
    for season, months in SEASONS.items():
        if month in months:
            return season</code></pre>

<h2>Задача 4: Система оценок с несколькими критериями</h2>
<pre><code>def final_grade(written, oral, attendance):
    """
    written: 0-100
    oral: 0-100
    attendance: 0-100 (процент посещаемости)
    """
    # Штраф за посещаемость
    if attendance < 50:
        return "Не допущен (посещаемость < 50%)"

    avg = written * 0.6 + oral * 0.4

    # Посещаемость влияет на финальную оценку
    if attendance < 70:
        avg *= 0.9   # штраф 10%

    if avg >= 90:   return "Отлично"
    if avg >= 75:   return "Хорошо"
    if avg >= 60:   return "Удовлетворительно"
    return "Неудовлетворительно"</code></pre>

<h2>Задача 5: Простой интерпретатор команд</h2>
<pre><code>def execute_command(cmd, state):
    match cmd.lower().strip():
        case "старт" | "start":
            state["running"] = True
            return "Запущено"
        case "стоп" | "stop":
            state["running"] = False
            return "Остановлено"
        case "статус" | "status":
            s = "работает" if state["running"] else "остановлено"
            return f"Состояние: {s}"
        case cmd if cmd.startswith("скорость "):
            try:
                speed = int(cmd.split()[1])
                state["speed"] = speed
                return f"Скорость: {speed}"
            except (ValueError, IndexError):
                return "Неверный формат: скорость N"
        case _:
            return f"Неизвестная команда: {cmd}"</code></pre>
''',
            'code_example': '''# Практические задачи на условия

import random

# 1. Полная игра «Камень, ножницы, бумага»
CHOICES = ["камень", "ножницы", "бумага"]
BEATS = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}

def play_rps(player, computer):
    if player not in CHOICES:
        return None, "Неверный выбор"
    if player == computer:
        return 0, "Ничья"
    if BEATS[player] == computer:
        return 1, f"{player} бьёт {computer}"
    return -1, f"{computer} бьёт {player}"

# Симуляция игры
wins = draws = losses = 0
for _ in range(100):
    p = random.choice(CHOICES)
    c = random.choice(CHOICES)
    result, _ = play_rps(p, c)
    if result == 1:   wins += 1
    elif result == 0: draws += 1
    else:             losses += 1

print("Симуляция 100 игр (случайный выбор):")
print(f"  Победы: {wins}, Ничьи: {draws}, Поражения: {losses}")
print(f"  Теоретически ~33% каждого исхода")

# 2. FizzBuzz расширенный
def fizzbuzz_generalized(n, rules):
    """Обобщённый FizzBuzz с произвольными правилами.
    rules: список (делитель, слово), напр. [(3,"Fizz"),(5,"Buzz")]
    """
    results = []
    for i in range(1, n + 1):
        label = ""
        for divisor, word in rules:
            if i % divisor == 0:
                label += word
        results.append(label if label else str(i))
    return results

rules = [(3, "Fizz"), (5, "Buzz"), (7, "Jazz")]
output = fizzbuzz_generalized(30, rules)
print("\\nFizzBuzzJazz (1-30):")
for i, v in enumerate(output, 1):
    suffix = "  ←" if v != str(i) else ""
    print(f"  {i:2}: {v}{suffix}")

# 3. Система оценок с несколькими критериями
def evaluate_student(name, written, oral, attendance):
    """Комплексная оценка студента."""
    issues = []
    if attendance < 50:
        return name, "Не допущен", f"посещаемость {attendance}% < 50%"

    base = written * 0.6 + oral * 0.4

    if attendance < 70:
        base *= 0.9
        issues.append(f"штраф за посещаемость {attendance}%")

    if written < 40:
        issues.append("письменная < 40")
    if oral < 40:
        issues.append("устная < 40")

    if issues and base >= 60:
        base = min(base, 59)  # нельзя сдать если есть критические проблемы

    if base >= 90:   grade = "Отлично"
    elif base >= 75: grade = "Хорошо"
    elif base >= 60: grade = "Удовл."
    else:            grade = "Неудовл."

    note = "; ".join(issues) if issues else ""
    return name, grade, note

students = [
    ("Иван",    80, 75, 95),
    ("Мария",   95, 90, 100),
    ("Пётр",    50, 45, 65),
    ("Анна",    70, 80, 45),
    ("Дмитрий", 35, 70, 80),
]

print("\\nИтоговые оценки:")
print(f"{'Студент':<12} {'Оценка':<10} {'Примечание'}")
print("-" * 50)
for args in students:
    name, grade, note = evaluate_student(*args)
    print(f"{name:<12} {grade:<10} {note}")
'''
        },
    ],

    # ═══════════════════════════════════════════════════════════════
    # МОДУЛЬ 4 — ЦИКЛ WHILE
    # ═══════════════════════════════════════════════════════════════
    'Цикл while': [
        {
            'title': 'Вложенные циклы: паттерны, матрицы, перебор',
            'order': 2,
            'estimated_minutes': 80,
            'content': '''
<h2>Вложенные циклы</h2>
<p>Цикл внутри цикла. Внутренний цикл выполняется <strong>полностью</strong> на каждой итерации внешнего.</p>

<pre><code>for i in range(3):         # внешний: 3 итерации
    for j in range(4):     # внутренний: 4 итерации (для каждого i)
        print(i, j)
# Всего 3 × 4 = 12 строк вывода</code></pre>

<p>Для вложенного while то же самое:</p>
<pre><code>i = 1
while i <= 3:
    j = 1
    while j <= 4:          # ВАЖНО: j переинициализируется каждый раз!
        print(f"({i},{j})", end=" ")
        j += 1
    print()
    i += 1</code></pre>

''' + warn('При вложенных while обязательно переинициализируй счётчик внутреннего цикла внутри внешнего. Иначе внутренний цикл выполнится только один раз.') + '''

<h2>Паттерны звёздочками</h2>
<p>Классические учебные задачи — вывод геометрических фигур через вложенные циклы:</p>

<pre><code>n = 5

# Прямоугольник n×n
for i in range(n):
    print("* " * n)

# Правый треугольник
for i in range(1, n+1):
    print("* " * i)

# Перевёрнутый треугольник
for i in range(n, 0, -1):
    print("* " * i)

# Пирамида (по центру)
for i in range(1, n+1):
    spaces = " " * (n - i)
    stars = "* " * i
    print(spaces + stars)

# Ромб
for i in range(1, n+1):
    print(" " * (n-i) + "* " * i)
for i in range(n-1, 0, -1):
    print(" " * (n-i) + "* " * i)</code></pre>

<h2>Перебор комбинаций</h2>
<p>Вложенные циклы — самый простой способ перебрать все пары, тройки и т.д.:</p>

<pre><code># Все пары чисел от 1 до n
n = 4
pairs = []
for i in range(1, n+1):
    for j in range(i+1, n+1):   # j > i — избегаем дубликатов
        pairs.append((i, j))
print(pairs)
# C(4,2) = 6 пар: (1,2),(1,3),(1,4),(2,3),(2,4),(3,4)

# Таблица умножения
for i in range(1, 11):
    row = [f"{i*j:4}" for j in range(1, 11)]
    print("".join(row))</code></pre>

<h2>Двумерный обход (матрица)</h2>
<p>Матрица — список списков. Для обхода нужны два индекса: строка и столбец.</p>

<pre><code>matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
rows = len(matrix)
cols = len(matrix[0])

# Обход всех элементов
for i in range(rows):
    for j in range(cols):
        print(matrix[i][j], end=" ")
    print()

# Сумма каждой строки
for i, row in enumerate(matrix):
    print(f"Строка {i}: сумма = {sum(row)}")

# Главная диагональ (i == j)
diagonal = [matrix[i][i] for i in range(min(rows, cols))]
print(f"Диагональ: {diagonal}")  # [1, 5, 9]</code></pre>

<h2>break и continue во вложенных циклах</h2>
<p>break и continue действуют только на <strong>ближайший</strong> (внутренний) цикл:</p>

<pre><code># Поиск пары в матрице
found = False
for i in range(rows):
    for j in range(cols):
        if matrix[i][j] == target:
            found = True
            break      # только внутренний цикл
    if found:
        break          # прерываем и внешний

# Флаг — стандартный способ прервать оба цикла
# В Python 3.12+ есть target labels в beta, но пока — флаг</code></pre>

''' + tip('Для поиска по матрице удобнее использовать функцию с return — ранний return прерывает оба цикла сразу.') + '''
''',
            'code_example': '''# Вложенные циклы: практика

# 1. Паттерны фигур
def print_shape(shape, n=5):
    print(f"--- {shape} ---")
    if shape == "rectangle":
        for _ in range(n):
            print("█" * n)
    elif shape == "triangle":
        for i in range(1, n+1):
            print("█" * i)
    elif shape == "pyramid":
        for i in range(1, n+1):
            print(" " * (n-i) + "█" * (2*i-1))
    elif shape == "diamond":
        for i in range(1, n+1):
            print(" "*(n-i) + "█"*(2*i-1))
        for i in range(n-1, 0, -1):
            print(" "*(n-i) + "█"*(2*i-1))

for shape in ["rectangle", "triangle", "pyramid", "diamond"]:
    print_shape(shape, 5)
    print()

# 2. Таблица умножения
print("Таблица умножения (1-10):")
print("   ", end="")
for j in range(1, 11):
    print(f"{j:4}", end="")
print()
print("   " + "----" * 10)
for i in range(1, 11):
    print(f"{i:2}|", end="")
    for j in range(1, 11):
        print(f"{i*j:4}", end="")
    print()

# 3. Магический квадрат 3x3 (сумма строк/столбцов/диагоналей = 15)
magic = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
n = 3
print("\\nМагический квадрат:")
for row in magic:
    print("  " + " ".join(f"{x:2}" for x in row))

# Проверка
row_sums = [sum(magic[i]) for i in range(n)]
col_sums = [sum(magic[i][j] for i in range(n)) for j in range(n)]
diag1 = sum(magic[i][i] for i in range(n))
diag2 = sum(magic[i][n-1-i] for i in range(n))
print(f"  Суммы строк: {row_sums}")
print(f"  Суммы столбцов: {col_sums}")
print(f"  Главная диагональ: {diag1}")
print(f"  Побочная диагональ: {diag2}")
print(f"  Магический: {all(s == 15 for s in row_sums+col_sums+[diag1,diag2])}")

# 4. Решето Эратосфена через while
def sieve_while(limit):
    """Простые числа через вложенные while."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    i = 2
    while i * i <= limit:
        if is_prime[i]:
            j = i * i
            while j <= limit:
                is_prime[j] = False
                j += i
        i += 1
    return [n for n in range(2, limit+1) if is_prime[n]]

primes = sieve_while(100)
print(f"\\nПростые до 100 ({len(primes)} штук):")
for i, p in enumerate(primes):
    print(f"{p:3}", end=("\\n" if (i+1) % 10 == 0 else " "))
'''
        },
        {
            'title': 'Числовые алгоритмы с while: поиск, итерации, приближения',
            'order': 3,
            'estimated_minutes': 75,
            'content': '''
<h2>Двоичный поиск — O(log n)</h2>
<p>Самый эффективный алгоритм поиска в отсортированном массиве. На каждом шаге отбрасывает половину оставшихся вариантов.</p>

<pre><code>def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2   # середина

        if arr[mid] == target:
            return mid              # нашли!
        elif arr[mid] < target:
            left = mid + 1          # ищем в правой половине
        else:
            right = mid - 1         # ищем в левой половине

    return -1   # не нашли</code></pre>

''' + info('Для нахождения числа в диапазоне 1..1 000 000 двоичный поиск делает максимум log₂(1000000) ≈ 20 шагов. Линейный поиск — до 1 000 000.') + '''

<h2>Алгоритм Евклида — НОД</h2>
<p>Нахождение наибольшего общего делителя (НОД). Один из старейших алгоритмов (300 до н.э.).</p>

<pre><code>def gcd(a, b):
    """Алгоритм Евклида через вычитание (оригинальный)."""
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a

def gcd_fast(a, b):
    """Алгоритм Евклида через остаток (быстрый)."""
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Наименьшее общее кратное через НОД."""
    return abs(a * b) // gcd_fast(a, b)</code></pre>

<h2>Метод Ньютона (итерационный квадратный корень)</h2>
<p>Численный метод нахождения корня функции через последовательное приближение. Для √N:</p>
<p>Формула итерации: x_new = (x + N/x) / 2</p>

<pre><code>def sqrt_newton(n, precision=1e-10):
    if n < 0:
        raise ValueError("Корень из отрицательного числа")
    if n == 0:
        return 0

    x = n                   # начальное приближение
    iterations = 0

    while True:
        x_new = (x + n / x) / 2
        iterations += 1
        if abs(x_new - x) < precision:
            break
        x = x_new

    return x_new, iterations</code></pre>

''' + tip('Метод Ньютона сходится квадратично: на каждом шаге число правильных знаков удваивается. Обычно 20-30 итераций дают точность double precision.') + '''

<h2>Прогрессии и суммы</h2>
<pre><code># Сумма арифметической прогрессии: a, a+d, a+2d, ...
def arithmetic_sum(a, d, n):
    """Первые n членов арифм. прогрессии начиная с a с шагом d."""
    total = 0
    current = a
    for _ in range(n):
        total += current
        current += d
    return total

# Формула Гаусса: n*(a1+an)/2
n = 100
direct = sum(range(1, n+1))
formula = n * (1 + n) // 2
print(f"Сумма 1..{n}: цикл={direct}, формула={formula}")

# Геометрическая прогрессия с условием остановки
def geometric_partial_sum(a, r, epsilon=1e-6):
    """Сумма членов геом. прогрессии пока член > epsilon."""
    total = 0
    current = a
    terms = 0
    while abs(current) > epsilon:
        total += current
        current *= r
        terms += 1
    return total, terms</code></pre>

<h2>Угадай число с оптимальной стратегией</h2>
<pre><code>def optimal_guess(low, high, secret):
    """Двоичный поиск для угадывания числа."""
    steps = 0
    while low <= high:
        guess = (low + high) // 2
        steps += 1
        if guess == secret:
            return steps
        elif guess < secret:
            low = guess + 1
        else:
            high = guess - 1
    return -1   # не нашли (не должно случиться)</code></pre>
''',
            'code_example': '''import math

# 1. Двоичный поиск с детализацией
def binary_search_verbose(arr, target):
    left, right = 0, len(arr) - 1
    step = 0
    print(f"Ищем {target} в массиве из {len(arr)} элементов")
    while left <= right:
        step += 1
        mid = (left + right) // 2
        print(f"  Шаг {step}: [{left}..{right}] → проверяем arr[{mid}]={arr[mid]}", end="")
        if arr[mid] == target:
            print(f" — НАЙДЕНО!")
            return mid
        elif arr[mid] < target:
            print(f" < {target}, ищем правее")
            left = mid + 1
        else:
            print(f" > {target}, ищем левее")
            right = mid - 1
    print(f"  Не найдено за {step} шагов")
    return -1

arr = list(range(0, 100, 2))   # чётные числа 0..98
binary_search_verbose(arr, 72)
binary_search_verbose(arr, 55)

# 2. НОД и НОК
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

pairs = [(48, 18), (100, 75), (17, 13), (360, 100)]
print("\\nНОД и НОК:")
for a, b in pairs:
    g, l = gcd(a, b), lcm(a, b)
    print(f"  НОД({a},{b})={g}, НОК({a},{b})={l}")

# 3. Метод Ньютона для квадратного корня
def sqrt_newton(n, precision=1e-12):
    if n < 0: raise ValueError
    if n == 0: return 0.0, 0
    x = float(n)
    for i in range(1000):
        x_new = (x + n / x) / 2
        if abs(x_new - x) < precision:
            return x_new, i + 1
        x = x_new
    return x, 1000

print("\\nКвадратный корень (метод Ньютона):")
for n in [2, 3, 9, 144, 10000, 1234567]:
    root, iters = sqrt_newton(n)
    exact = math.sqrt(n)
    error = abs(root - exact)
    print(f"  √{n:<8} = {root:.10f}  (итераций: {iters:2}, погрешность: {error:.2e})")

# 4. Коллатц: исследование последовательностей
def collatz_length(n):
    length = 1
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        length += 1
    return length

# Найти число до 1000 с максимальной длиной
print("\\nКоллатц — топ-5 самых длинных:")
lengths = [(collatz_length(n), n) for n in range(1, 1001)]
lengths.sort(reverse=True)
for length, n in lengths[:5]:
    print(f"  n={n}: длина={length}")
'''
        },
    ],
}


# Новые модули целиком
NEW_MODULES = [
    # ═══════════════════════════════════════════════════════════════
    # МОДУЛЬ 19 — ТЕСТИРОВАНИЕ КОДА
    # ═══════════════════════════════════════════════════════════════
    {
        'title': 'Тестирование кода',
        'icon': 'fas fa-check-double',
        'order': 19,
        'description': 'doctest, assert, unittest. Почему тесты важны и как их писать правильно.',
        'lessons': [
            {
                'title': 'Зачем тестировать. doctest, assert и unittest',
                'order': 1,
                'estimated_minutes': 85,
                'content': '''
<h2>Зачем тестировать код?</h2>
<p>«У меня всё работает» — самая опасная фраза в программировании. Код без тестов:</p>
<ul>
  <li>Может работать «в целом», но ломаться на граничных случаях</li>
  <li>При изменении одной части ломает другую (регрессия)</li>
  <li>Трудно поддерживать — страшно что-то менять</li>
</ul>
<p>Тесты — это автоматические проверки, которые запускаются мгновенно и говорят «всё OK» или «вот что сломалось».</p>

<h2>Три вида тестирования</h2>
''' + table(
    ['Вид', 'Что проверяет', 'Инструмент'],
    [
        ['Unit тест', 'Одну функцию/метод в изоляции', 'unittest, pytest'],
        ['Интеграционный', 'Взаимодействие нескольких компонентов', 'pytest, Django TestCase'],
        ['End-to-End (E2E)', 'Весь поток от пользователя до результата', 'Selenium, Playwright'],
    ]
) + '''

<h2>assert — простейшие проверки</h2>
<pre><code>def add(a, b):
    return a + b

# Проверки после функции (в коде или тестовом файле)
assert add(2, 3) == 5
assert add(-1, 1) == 0
assert add(0, 0) == 0

# С сообщением об ошибке
assert add(2, 3) == 5, f"Ожидалось 5, получено {add(2,3)}"</code></pre>

''' + warn('assert отключается при запуске с флагом -O (optimize). Не используй assert для пользовательского ввода и критичной бизнес-логики — только в тестах.') + '''

<h2>doctest — тесты прямо в документации</h2>
<p>doctest читает docstring функции и выполняет примеры, начинающиеся с >>>:</p>

<pre><code>def factorial(n):
    """
    Вычисляет n! (факториал).

    >>> factorial(0)
    1
    >>> factorial(5)
    120
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n должен быть неотрицательным
    """
    if n < 0:
        raise ValueError("n должен быть неотрицательным")
    if n == 0:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)</code></pre>

''' + tip('doctest удобен для небольших функций. Преимущество: документация и тест в одном месте. Недостаток: сложные сценарии неудобно писать.') + '''

<h2>unittest — полноценное тестирование</h2>
<pre><code>import unittest

class TestCalculator(unittest.TestCase):

    def setUp(self):
        """Выполняется перед каждым тестом."""
        self.calc = Calculator()

    def test_add_positive(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(self.calc.add(-1, -1), -2)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_sqrt_negative(self):
        with self.assertRaises(ValueError):
            self.calc.sqrt(-1)

if __name__ == "__main__":
    unittest.main()</code></pre>

<h2>Методы assert в unittest</h2>
''' + table(
    ['Метод', 'Проверяет', 'Пример'],
    [
        ['assertEqual(a, b)', 'a == b', 'assertEqual(func(5), 25)'],
        ['assertNotEqual(a, b)', 'a != b', '—'],
        ['assertTrue(x)', 'bool(x) is True', 'assertTrue(lst)'],
        ['assertFalse(x)', 'bool(x) is False', 'assertFalse([])'],
        ['assertIsNone(x)', 'x is None', '—'],
        ['assertIsNotNone(x)', 'x is not None', '—'],
        ['assertIn(a, b)', 'a in b', 'assertIn(3, [1,2,3])'],
        ['assertRaises(Exc)', 'Исключение брошено', 'см. выше'],
        ['assertAlmostEqual(a, b)', '|a-b| < delta', 'для float'],
    ]
) + '''

<h2>Принципы хорошего теста (FIRST)</h2>
<ul>
  <li><strong>F</strong>ast — тест должен выполняться быстро (< 100мс)</li>
  <li><strong>I</strong>solated — тесты не зависят друг от друга</li>
  <li><strong>R</strong>epeatable — результат одинаков при каждом запуске</li>
  <li><strong>S</strong>elf-validating — тест сам определяет успех/неудачу</li>
  <li><strong>T</strong>imely — тест пишется вместе с кодом (или до)</li>
</ul>

<h2>TDD — разработка через тесты</h2>
<p>Test-Driven Development: сначала пишем тест, затем код:</p>
<ol>
  <li>Написать тест (он падает — RED)</li>
  <li>Написать минимальный код, чтобы тест прошёл (GREEN)</li>
  <li>Улучшить код без изменения поведения (REFACTOR)</li>
</ol>
''',
                'code_example': '''# Тестирование: демонстрация

import unittest
import math

# --- Тестируемый код ---

def is_prime(n):
    """
    Проверяет, является ли n простым числом.

    >>> is_prime(2)
    True
    >>> is_prime(1)
    False
    >>> is_prime(17)
    True
    >>> is_prime(4)
    False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def find_primes(limit):
    """Простые числа до limit включительно."""
    return [n for n in range(2, limit + 1) if is_prime(n)]


class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount
        return self._balance

    @property
    def balance(self):
        return self._balance


# --- Тесты ---

class TestIsPrime(unittest.TestCase):

    def test_small_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
            self.assertTrue(is_prime(p), f"{p} должно быть простым")

    def test_not_prime(self):
        for n in [0, 1, 4, 6, 8, 9, 10, 15, 100]:
            self.assertFalse(is_prime(n), f"{n} не должно быть простым")

    def test_large_prime(self):
        self.assertTrue(is_prime(997))   # простое
        self.assertFalse(is_prime(1001)) # 7 × 11 × 13


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount(1000)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000)

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_withdraw(self):
        self.account.withdraw(300)
        self.assertEqual(self.account.balance, 700)

    def test_deposit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_overdraft_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(9999)

    def test_sequence_of_operations(self):
        self.account.deposit(200)   # 1200
        self.account.withdraw(400)  # 800
        self.account.deposit(50)    # 850
        self.assertEqual(self.account.balance, 850)


# Запуск тестов
loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromTestCase(TestIsPrime))
suite.addTests(loader.loadTestsFromTestCase(TestBankAccount))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

print(f"\\nРезультат: {'PASSED' if result.wasSuccessful() else 'FAILED'}")
print(f"Тестов: {result.testsRun}, Ошибок: {len(result.errors)}, Провалов: {len(result.failures)}")

# doctest
import doctest
print("\\nЗапуск doctest:")
results = doctest.testmod(verbose=False)
print(f"doctest: {results.attempted} тестов, {results.failed} провалов")
'''
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # МОДУЛЬ 20 — АЛГОРИТМИЧЕСКОЕ МЫШЛЕНИЕ
    # ═══════════════════════════════════════════════════════════════
    {
        'title': 'Алгоритмическое мышление',
        'icon': 'fas fa-brain',
        'order': 20,
        'description': 'Как думать алгоритмически. Декомпозиция, сложность, жадные алгоритмы, динамическое программирование.',
        'lessons': [
            {
                'title': 'Декомпозиция задач и анализ сложности',
                'order': 1,
                'estimated_minutes': 85,
                'content': '''
<h2>Что такое алгоритмическое мышление?</h2>
<p>Алгоритмическое мышление — способность:</p>
<ul>
  <li>Разбить сложную задачу на простые подзадачи (декомпозиция)</li>
  <li>Найти закономерность (паттерн)</li>
  <li>Абстрагироваться от деталей (абстракция)</li>
  <li>Записать решение как последовательность шагов (алгоритм)</li>
</ul>

<h2>Шаги решения задачи</h2>
<ol>
  <li><strong>Понять задачу</strong> — перефрази своими словами, найди примеры входа/выхода</li>
  <li><strong>Граничные случаи</strong> — пустой ввод, нули, максимальные значения, отрицательные числа</li>
  <li><strong>Набросок решения</strong> — псевдокод, схема</li>
  <li><strong>Оценить сложность</strong> — O(n), O(n²) и т.д.</li>
  <li><strong>Реализовать</strong> — код</li>
  <li><strong>Протестировать</strong> — граничные случаи + общий случай</li>
</ol>

<h2>Нотация O-большое — быстрое введение</h2>
<p>Описывает, как растёт время работы при увеличении размера входа n:</p>

''' + table(
    ['Сложность', 'Класс', 'При n=1000', 'Пример'],
    [
        ['O(1)', 'Константная', '1 операция', 'Доступ по индексу'],
        ['O(log n)', 'Логарифмическая', '~10 операций', 'Двоичный поиск'],
        ['O(n)', 'Линейная', '1 000', 'Линейный поиск'],
        ['O(n log n)', 'Линейно-логарифмическая', '~10 000', 'Быстрая сортировка'],
        ['O(n²)', 'Квадратичная', '1 000 000', 'Пузырьковая сортировка'],
        ['O(2ⁿ)', 'Экспоненциальная', '10³⁰⁰ операций', 'Перебор всех подмножеств'],
    ]
) + '''

<h2>Паттерны алгоритмов</h2>

<h3>1. Два указателя (Two Pointers)</h3>
<p>Два индекса движутся навстречу или в одном направлении:</p>
<pre><code>def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

def two_sum_sorted(arr, target):
    """Найти пару с заданной суммой в отсортированном массиве."""
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return (left, right)
        elif s < target:
            left += 1
        else:
            right -= 1
    return None</code></pre>

<h3>2. Скользящее окно (Sliding Window)</h3>
<pre><code>def max_sum_subarray(arr, k):
    """Максимальная сумма подмассива длины k."""
    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]   # добавляем новый, убираем старый
        max_sum = max(max_sum, window_sum)

    return max_sum</code></pre>

<h3>3. Жадный алгоритм (Greedy)</h3>
<p>На каждом шаге выбирать локально оптимальный вариант:</p>
<pre><code>def coin_change_greedy(amount, coins):
    """Минимальное количество монет (только если монеты «удобные»)."""
    coins.sort(reverse=True)    # от крупных к мелким
    result = []
    for coin in coins:
        while amount >= coin:
            result.append(coin)
            amount -= coin
    return result if amount == 0 else None

# Работает для [1, 5, 10, 25]:
print(coin_change_greedy(41, [1, 5, 10, 25]))  # [25, 10, 5, 1]
# НЕ работает для [1, 3, 4]:
# Нужно 6 = 3+3, жадный даёт 4+1+1 = 3 монеты вместо 2!</code></pre>

<h3>4. Динамическое программирование (DP)</h3>
<p>Сохраняем результаты подзадач чтобы не пересчитывать:</p>
<pre><code>def coin_change_dp(amount, coins):
    """Точное минимальное количество монет (DP)."""
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1

    return dp[amount] if dp[amount] != float("inf") else -1</code></pre>
''',
                'code_example': '''# Алгоритмическое мышление: практика

import time

# 1. Сравнение: линейный vs двоичный поиск
def linear_search(arr, target):
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Бенчмарк
import random
sizes = [1000, 10000, 100000]
print("Линейный vs Двоичный поиск:")
print(f"{'N':>8} {'Линейный':>12} {'Двоичный':>12}")
print("-" * 35)
for n in sizes:
    arr = sorted(random.sample(range(n * 10), n))
    target = random.choice(arr)

    reps = 1000
    t1 = time.perf_counter()
    for _ in range(reps): linear_search(arr, target)
    t1 = (time.perf_counter() - t1) / reps * 1e6

    t2 = time.perf_counter()
    for _ in range(reps): binary_search(arr, target)
    t2 = (time.perf_counter() - t2) / reps * 1e6

    print(f"{n:>8} {t1:>10.1f}μs {t2:>10.1f}μs")

# 2. Два указателя: палиндромы
def is_palindrome(s):
    s = "".join(c.lower() for c in s if c.isalnum())
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

tests = ["racecar", "A man a plan a canal Panama", "hello", "Was it a car or a cat I saw"]
print("\\nПалиндромы:")
for t in tests:
    print(f"  '{t[:30]}{'...' if len(t)>30 else ''}': {is_palindrome(t)}")

# 3. Жадный vs DP: размен монет
def greedy_coins(amount, coins):
    coins_sorted = sorted(coins, reverse=True)
    result = []
    for c in coins_sorted:
        while amount >= c:
            result.append(c)
            amount -= c
    return result if amount == 0 else None

def dp_coins(amount, coins):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    parent = [-1] * (amount + 1)
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i and dp[i-c] + 1 < dp[i]:
                dp[i] = dp[i-c] + 1
                parent[i] = c
    if dp[amount] == float("inf"):
        return None
    result = []
    while amount > 0:
        result.append(parent[amount])
        amount -= parent[amount]
    return result

print("\\nРазмен монет:")
test_cases = [
    (41, [1, 5, 10, 25]),
    (6, [1, 3, 4]),
    (11, [1, 5, 6, 9]),
]
for amount, coins in test_cases:
    g = greedy_coins(amount, coins[:])
    d = dp_coins(amount, coins)
    print(f"  {amount}₽ из {coins}:")
    print(f"    Жадный: {g} ({len(g) if g else '∞'} монет)")
    print(f"    DP:     {d} ({len(d) if d else '∞'} монет)")

# 4. Скользящее окно
def max_sum_window(arr, k):
    if len(arr) < k:
        return None, None
    window = sum(arr[:k])
    max_sum = window
    max_pos = 0
    for i in range(k, len(arr)):
        window += arr[i] - arr[i-k]
        if window > max_sum:
            max_sum = window
            max_pos = i - k + 1
    return max_sum, arr[max_pos:max_pos+k]

data = [2, 1, 5, 1, 3, 2, 1, 4, 6, 3]
for k in [2, 3, 4]:
    total, sub = max_sum_window(data, k)
    print(f"\\nОкно {k}: макс сумма = {total}, подмассив = {sub}")
'''
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Расширяет модули 1-4 (по 2 урока), добавляет модули 19-20'

    def handle(self, *args, **options):
        added_lessons = 0

        # Добавляем уроки в существующие модули
        for module_title, lessons in EXTRA_LESSONS.items():
            try:
                module = TheoryModule.objects.get(title=module_title)
            except TheoryModule.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Модуль не найден: {module_title}')
                )
                continue

            for les in lessons:
                _, created = TheoryLesson.objects.update_or_create(
                    module=module,
                    title=les['title'],
                    defaults=les,
                )
                if created:
                    added_lessons += 1
                    self.stdout.write(f'  + урок: {les["title"][:60]}')

        # Добавляем новые модули
        for mod_data in NEW_MODULES:
            lessons = mod_data.pop('lessons')
            module, mc = TheoryModule.objects.update_or_create(
                title=mod_data['title'],
                defaults=mod_data,
            )
            for les in lessons:
                _, lc = TheoryLesson.objects.update_or_create(
                    module=module,
                    title=les['title'],
                    defaults=les,
                )
                if lc:
                    added_lessons += 1
                    self.stdout.write(f'  + урок: {les["title"][:60]}')

        from django.db.models import Sum
        total_min = TheoryLesson.objects.aggregate(t=Sum('estimated_minutes'))['t'] or 0
        self.stdout.write(self.style.SUCCESS(
            f'\nГотово! Добавлено уроков: {added_lessons}\n'
            f'Всего в БД: {TheoryModule.objects.count()} модулей, '
            f'{TheoryLesson.objects.count()} уроков '
            f'(~{total_min // 60}ч {total_min % 60}мин)'
        ))
