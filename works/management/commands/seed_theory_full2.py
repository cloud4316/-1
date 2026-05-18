"""python manage.py seed_theory_full2  — модули 5-10"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson


def tip(t):  return f'<div class="tip">💡 {t}</div>'
def warn(t): return f'<div class="warning">⚠️ {t}</div>'
def info(t): return f'<div class="tip" style="background:#e0f2fe;border-color:#0284c7">ℹ️ {t}</div>'


def table(headers, rows):
    th = ''.join(f'<th>{c}</th>' for c in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="theory-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


MODULES = [

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 5 — ЦИКЛ FOR И RANGE
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Цикл for и range()',
'icon': 'fas fa-list-ol',
'order': 5,
'description': 'Итерация по последовательностям. range(), enumerate(), zip(), list comprehension.',
'lessons': [
{
'title': 'Цикл for: итерация по последовательностям',
'order': 1,
'estimated_minutes': 85,
'content': '''
<h2>Концепция итерации</h2>
<p><strong>Итерация</strong> — последовательный обход элементов коллекции. Цикл <code>for</code> в Python принципиально отличается от аналогов в C/Java: он не считает от 0 до N, а обходит <em>любой итерируемый объект</em>.</p>

<h2>Синтаксис for</h2>
<pre><code>for переменная in итерируемый_объект:
    тело_цикла</code></pre>
<p>При каждой итерации переменная получает очередной элемент. После последнего элемента цикл завершается.</p>

<h2>Итерируемые объекты в Python</h2>
''' + table(
    ['Тип','Пример','Что перебираем'],
    [
        ['str','for c in "python"','Символы'],
        ['list','for x in [1,2,3]','Элементы'],
        ['tuple','for x in (1,2,3)','Элементы'],
        ['dict','for k in {"a":1}','Ключи'],
        ['set','for x in {1,2,3}','Элементы (в произв. порядке)'],
        ['range','for i in range(10)','Числа'],
        ['файл','for line in file','Строки файла'],
        ['enumerate','for i,x in enumerate(lst)','Индексы + элементы'],
        ['zip','for a,b in zip(l1,l2)','Пары элементов'],
    ]
) + '''

<h2>Функция range()</h2>
<p><code>range()</code> генерирует последовательность чисел <strong>не создавая список</strong> в памяти. Это делает её эффективной для больших диапазонов.</p>
<pre><code>range(stop)           # 0, 1, ..., stop-1
range(start, stop)    # start, ..., stop-1
range(start, stop, step)  # с шагом</code></pre>
''' + table(
    ['Вызов','Результат'],
    [
        ['range(5)','0, 1, 2, 3, 4'],
        ['range(1, 6)','1, 2, 3, 4, 5'],
        ['range(0, 10, 2)','0, 2, 4, 6, 8'],
        ['range(10, 0, -1)','10, 9, 8, 7, 6, 5, 4, 3, 2, 1'],
        ['range(5, 0, -1)','5, 4, 3, 2, 1'],
    ]
) + '''
''' + tip('range(100_000_000) занимает ~56 байт памяти, а список из 100 млн чисел — ~800 МБ. range — объект-генератор!') + '''

<h2>enumerate() — индекс + значение</h2>
<p>Часто нужен и элемент, и его порядковый номер:</p>
<pre><code># Плохо:
for i in range(len(fruits)):
    print(i, fruits[i])

# Хорошо:
for i, fruit in enumerate(fruits):
    print(i, fruit)

# С нестандартным стартом:
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")</code></pre>
''' + warn('Никогда не пиши <code>for i in range(len(lst)): ... lst[i]</code>. Используй <code>enumerate</code> или прямую итерацию.') + '''

<h2>zip() — параллельная итерация</h2>
<p>Обход нескольких последовательностей одновременно:</p>
<pre><code>names = ["Иван", "Мария", "Пётр"]
scores = [95, 87, 72]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip останавливается по КОРОТКОЙ последовательности
a = [1, 2, 3, 4, 5]
b = [10, 20, 30]
print(list(zip(a, b)))  # [(1,10),(2,20),(3,30)] — 4,5 потеряны!

# Если нужно по длинной:
from itertools import zip_longest
print(list(zip_longest(a, b, fillvalue=0)))</code></pre>

<h2>for / else</h2>
<p>Как и у while, у for есть блок else — выполняется если цикл не прервался break:</p>
<pre><code>def find_prime(nums):
    for n in nums:
        for d in range(2, int(n**0.5) + 1):
            if n % d == 0:
                break
        else:
            print(f"{n} — простое")

find_prime([2, 3, 4, 5, 6, 7, 8, 9, 10])</code></pre>

<h2>List Comprehension — генератор списков</h2>
<p>Мощный и питонический способ создавать списки:</p>
<pre><code># Обычный цикл:
squares = []
for i in range(10):
    squares.append(i ** 2)

# List comprehension:
squares = [i ** 2 for i in range(10)]

# С условием:
evens = [x for x in range(20) if x % 2 == 0]

# Вложенный:
matrix = [[i*j for j in range(1,4)] for i in range(1,4)]

# Со строками:
words = ["hello", "world", "python"]
upper = [w.upper() for w in words if len(w) > 4]</code></pre>
''' + info('List comprehension работает быстрее обычного цикла — примерно в 1.5-2 раза. Но читаемость важнее скорости для сложных случаев.') + '''

<h2>Dictionary и Set Comprehension</h2>
<pre><code># Dict comprehension
squares_dict = {n: n**2 for n in range(1, 11)}
# {1: 1, 2: 4, 3: 9, ...}

# Инвертировать словарь
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}

# Set comprehension
unique_lengths = {len(word) for word in words}</code></pre>
''',
'code_example': '''# Таблица умножения
print("Таблица умножения:")
print("   ", end="")
for j in range(1, 11):
    print(f"{j:4}", end="")
print()
for i in range(1, 11):
    print(f"{i:2}|", end="")
    for j in range(1, 11):
        print(f"{i*j:4}", end="")
    print()

# Работа с enumerate
fruits = ["яблоко", "банан", "вишня", "апельсин"]
print("\\nМоё меню:")
for i, fruit in enumerate(fruits, 1):
    print(f"  {i}. {fruit}")

# zip — соединить два списка
students = ["Иван", "Мария", "Пётр", "Анна"]
grades = [4, 5, 3, 5]
print("\\nОценки:")
for name, grade in zip(students, grades):
    stars = "★" * grade + "☆" * (5 - grade)
    print(f"  {name:<10} {stars}")

# List comprehension — примеры
squares = [x**2 for x in range(1, 11)]
print(f"\\nКвадраты: {squares}")

# Числа Фибоначчи с comprehension
def fib(n):
    a, b = 0, 1
    result = []
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result

fibs = fib(200)
print(f"Фибоначчи до 200: {fibs}")

# Матрица — список списков
n = 5
identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
print("\\nЕдиничная матрица 5x5:")
for row in identity:
    print(" ".join(map(str, row)))

# Поиск простых чисел (Решето Эратосфена)
def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit+1, i):
                is_prime[j] = False
    return [i for i in range(2, limit+1) if is_prime[i]]

primes = sieve(50)
print(f"\\nПростые до 50: {primes}")'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 6 — ФУНКЦИИ
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Функции',
'icon': 'fas fa-function',
'order': 6,
'description': 'Создание и вызов функций. Аргументы, возврат значений, область видимости, lambda.',
'lessons': [
{
'title': 'Функции: определение, аргументы, возврат',
'order': 1,
'estimated_minutes': 90,
'content': '''
<h2>Зачем нужны функции?</h2>
<p>Представь, что ты трижды в программе считаешь площадь треугольника. Без функции — копируешь формулу трижды. Если нашёл ошибку — исправляешь в трёх местах. Функции решают это:</p>
<ul>
  <li><strong>DRY</strong> — Don't Repeat Yourself (не повторяй себя)</li>
  <li><strong>Декомпозиция</strong> — разбивка задачи на мелкие подзадачи</li>
  <li><strong>Читаемость</strong> — код с функциями читается как текст</li>
  <li><strong>Тестируемость</strong> — функцию легко протестировать отдельно</li>
  <li><strong>Переиспользование</strong> — одна функция, много мест вызова</li>
</ul>

<h2>Синтаксис определения функции</h2>
<pre><code>def имя_функции(параметры):
    """Docstring — описание функции."""
    тело_функции
    return значение  # необязательно</code></pre>
''' + tip('Хорошая функция делает одну вещь и делает её хорошо. Это принцип единственной ответственности (SRP).') + '''

<h2>Параметры и аргументы</h2>
''' + table(
    ['Термин','Определение','Пример'],
    [
        ['Параметр','Переменная в определении функции','def f(x): — x это параметр'],
        ['Аргумент','Значение при вызове функции','f(42) — 42 это аргумент'],
    ]
) + '''

<h3>Виды аргументов:</h3>
<pre><code># 1. Позиционные (обязательные)
def power(base, exp):
    return base ** exp

power(2, 10)    # base=2, exp=10

# 2. Именованные (keyword)
power(exp=10, base=2)  # порядок не важен

# 3. Аргументы по умолчанию
def greet(name, greeting="Привет"):
    return f"{greeting}, {name}!"

greet("Иван")              # "Привет, Иван!"
greet("Мария", "Здравствуй")  # "Здравствуй, Мария!"

# 4. *args — переменное число позиционных
def total(*numbers):
    return sum(numbers)

total(1, 2, 3)       # 6
total(1, 2, 3, 4, 5) # 15

# 5. **kwargs — переменное число именованных
def describe(**info):
    for key, val in info.items():
        print(f"{key}: {val}")

describe(name="Иван", age=21, city="Москва")</code></pre>

''' + warn('Аргументы по умолчанию вычисляются ОДИН РАЗ при определении функции! Никогда не используй изменяемые объекты (списки, словари) как дефолты.') + '''
<pre><code># ПЛОХО:
def add(item, lst=[]):     # lst создаётся один раз!
    lst.append(item)
    return lst

# ХОРОШО:
def add(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst</code></pre>

<h2>Оператор return</h2>
<p>Функция может вернуть любое значение. Без return (или с пустым return) возвращает None.</p>
<pre><code># Возврат одного значения
def square(n):
    return n ** 2

# Возврат нескольких (кортеж)
def min_max(lst):
    return min(lst), max(lst)

low, high = min_max([3, 1, 4, 1, 5, 9])

# Ранний возврат (guard clause)
def safe_divide(a, b):
    if b == 0:
        return None  # или raise ValueError
    return a / b</code></pre>

<h2>Область видимости (Scope)</h2>
<p>Python использует правило <strong>LEGB</strong>:</p>
''' + table(
    ['Уровень','Буква','Описание'],
    [
        ['Local','L','Внутри текущей функции'],
        ['Enclosing','E','Внешняя функция (для вложенных)'],
        ['Global','G','Уровень модуля'],
        ['Built-in','B','Встроенные имена Python (print, len...)'],
    ]
) + '''
<pre><code>x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)  # "local"
    inner()
    print(x)      # "enclosing"

outer()
print(x)          # "global"</code></pre>

<h3>global и nonlocal</h3>
<pre><code>counter = 0

def increment():
    global counter    # изменяем глобальную переменную
    counter += 1

def make_counter():
    count = 0
    def inc():
        nonlocal count  # изменяем переменную внешней функции
        count += 1
        return count
    return inc</code></pre>
''' + warn('Злоупотребление global — признак плохого дизайна. Предпочитай передавать данные через аргументы и return.') + '''

<h2>Docstrings — документирование функций</h2>
<pre><code>def calculate_bmi(weight_kg, height_m):
    """
    Вычисляет индекс массы тела (ИМТ).

    Args:
        weight_kg (float): Масса в килограммах.
        height_m (float): Рост в метрах.

    Returns:
        float: ИМТ, округлённый до 1 знака.

    Raises:
        ValueError: Если рост или масса <= 0.
    """
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("Масса и рост должны быть положительными")
    return round(weight_kg / height_m ** 2, 1)

help(calculate_bmi)  # вывод документации</code></pre>

<h2>Lambda-функции</h2>
<p>Анонимные однострочные функции:</p>
<pre><code>square = lambda x: x ** 2
add = lambda a, b: a + b

# Чаще используют как аргументы других функций:
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort(key=lambda x: -x)  # сортировка по убыванию

students = [("Иван", 85), ("Мария", 92), ("Пётр", 78)]
students.sort(key=lambda s: s[1], reverse=True)  # по оценке</code></pre>
''',
'code_example': '''# Практические примеры функций

def celsius_to_fahrenheit(c):
    """Перевод из Цельсия в Фаренгейт."""
    return c * 9/5 + 32

def fahrenheit_to_celsius(f):
    """Перевод из Фаренгейта в Цельсий."""
    return (f - 32) * 5/9

for temp in [-40, 0, 20, 37, 100]:
    f = celsius_to_fahrenheit(temp)
    print(f"{temp:>4}°C = {f:>7.1f}°F")

# Функция с *args и **kwargs
def format_student(*subjects, name="Студент", **scores):
    print(f"\\n{name}:")
    print(f"  Предметы: {', '.join(subjects)}")
    for subj, score in scores.items():
        grade = "✓" if score >= 60 else "✗"
        print(f"  {grade} {subj}: {score}")

format_student("Математика", "Физика", "Python",
               name="Иван Петров",
               Математика=85, Физика=72, Python=95)

# Рекурсивная функция (забегаем вперёд)
def factorial(n):
    """n! через рекурсию."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print("\\nФакториалы:")
for i in range(1, 11):
    print(f"{i:2}! = {factorial(i):>10}")

# Функции высшего порядка
def apply_twice(func, x):
    """Применить функцию дважды."""
    return func(func(x))

double = lambda x: x * 2
print(apply_twice(double, 3))   # 12 (3→6→12)

# Замыкание (closure)
def make_multiplier(factor):
    """Создаёт функцию-умножитель."""
    def multiplier(x):
        return x * factor
    return multiplier

triple = make_multiplier(3)
times10 = make_multiplier(10)
print(triple(7))    # 21
print(times10(7))   # 70

# Декоратор (введение)
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} выполнилась за {elapsed:.6f} сек")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(1_000_000)'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 7 — СПИСКИ И КОРТЕЖИ
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Списки и кортежи',
'icon': 'fas fa-list',
'order': 7,
'description': 'Хранение коллекций данных. Методы списков, срезы, сортировка, кортежи.',
'lessons': [
{
'title': 'Списки: создание, индексация, методы',
'order': 1,
'estimated_minutes': 85,
'content': '''
<h2>Список (list) — основная коллекция Python</h2>
<p>Список — <strong>упорядоченная изменяемая</strong> коллекция. Может содержать элементы любых типов, в том числе смешанных и вложенных списков.</p>

<h3>Способы создания</h3>
<pre><code>lst1 = [1, 2, 3, 4, 5]
lst2 = list("Python")          # ['P', 'y', 't', 'h', 'o', 'n']
lst3 = list(range(10))         # [0, 1, 2, ..., 9]
lst4 = [0] * 5                 # [0, 0, 0, 0, 0]
lst5 = [x**2 for x in range(5)] # [0, 1, 4, 9, 16]
empty = []                     # пустой список</code></pre>

<h2>Индексация и срезы</h2>
<p>Работают аналогично строкам, но можно изменять элементы:</p>
<pre><code>lst = [10, 20, 30, 40, 50]
print(lst[0])     # 10
print(lst[-1])    # 50
print(lst[1:3])   # [20, 30]
print(lst[::-1])  # [50, 40, 30, 20, 10]

# Изменение через индекс
lst[2] = 99
print(lst)        # [10, 20, 99, 40, 50]

# Срез можно присваивать
lst[1:3] = [200, 300, 400]  # замена среза</code></pre>

<h2>Методы списков</h2>
<h3>Добавление элементов</h3>
''' + table(
    ['Метод','Описание','Пример','Результат'],
    [
        ['.append(x)','Добавить в конец','[1,2].append(3)','[1,2,3]'],
        ['.insert(i,x)','Вставить на позицию i','[1,3].insert(1,2)','[1,2,3]'],
        ['.extend(iter)','Добавить все элементы','[1,2].extend([3,4])','[1,2,3,4]'],
        ['+=','То же что extend','lst += [5,6]','lst с добавленными 5,6'],
    ]
) + '''
<h3>Удаление элементов</h3>
''' + table(
    ['Метод','Описание','Примечание'],
    [
        ['.remove(x)','Удалить первое вхождение x','ValueError если нет'],
        ['.pop()','Удалить и вернуть последний','O(1)'],
        ['.pop(i)','Удалить и вернуть элемент по индексу','O(n) для середины'],
        ['.clear()','Очистить список','—'],
        ['del lst[i]','Удалить элемент (нет возврата)','—'],
        ['del lst[i:j]','Удалить срез','—'],
    ]
) + '''
<h3>Поиск и информация</h3>
''' + table(
    ['Метод/Функция','Описание','Пример'],
    [
        ['.index(x)','Индекс первого вхождения','[3,1,4].index(4) → 2'],
        ['.count(x)','Количество вхождений','[1,2,1].count(1) → 2'],
        ['len(lst)','Количество элементов','len([1,2,3]) → 3'],
        ['x in lst','Проверка принадлежности','3 in [1,2,3] → True'],
        ['min/max(lst)','Минимум/максимум','min([3,1,4]) → 1'],
        ['sum(lst)','Сумма','sum([1,2,3]) → 6'],
        ['sorted(lst)','Новый отсортированный','—'],
        ['.sort()','Сортировка на месте','—'],
        ['.reverse()','Реверс на месте','—'],
    ]
) + '''

<h2>Копирование списков — важно!</h2>
''' + warn('Присваивание lst2 = lst1 НЕ создаёт копию. Оба имени указывают на ОДИН объект.') + '''
<pre><code>lst1 = [1, 2, 3]
lst2 = lst1      # не копия, а второй ярлык!
lst2.append(4)
print(lst1)      # [1, 2, 3, 4] — изменился!

# Поверхностная копия (shallow):
lst2 = lst1.copy()
lst2 = lst1[:]
lst2 = list(lst1)

# Глубокая копия (для вложенных):
import copy
lst2 = copy.deepcopy(lst1)</code></pre>

<h2>Сортировка</h2>
<pre><code>numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()               # сортировка на месте, по возрастанию
numbers.sort(reverse=True)   # по убыванию

# sorted() — возвращает новый список, оригинал неизменён
sorted_nums = sorted(numbers)

# Сортировка по ключу
words = ["python", "java", "c++", "javascript"]
words.sort(key=len)               # по длине слова
words.sort(key=lambda w: w[-1])   # по последней букве

students = [{"name": "Иван", "gpa": 4.5},
            {"name": "Мария", "gpa": 4.8}]
students.sort(key=lambda s: s["gpa"], reverse=True)</code></pre>

<h2>Вложенные списки (матрицы)</h2>
<pre><code># Матрица 3x3
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix[1][2])  # 6 (строка 1, столбец 2)

# Транспонирование
transposed = [[matrix[j][i] for j in range(3)] for i in range(3)]</code></pre>
''',
'code_example': '''# Практика со списками

# 1. Статистика оценок
grades = [78, 92, 65, 88, 72, 95, 60, 84, 77, 90]

print(f"Оценок: {len(grades)}")
print(f"Средняя: {sum(grades)/len(grades):.1f}")
print(f"Лучшая: {max(grades)}")
print(f"Худшая: {min(grades)}")
print(f"Медиана: {sorted(grades)[len(grades)//2]}")

above_80 = [g for g in grades if g >= 80]
print(f"Выше 80: {len(above_80)} ({len(above_80)/len(grades)*100:.0f}%)")

# 2. Стек (LIFO) — последний вошёл, первый вышел
stack = []
for op in ["push A", "push B", "push C", "pop", "push D", "pop"]:
    if op.startswith("push"):
        item = op.split()[1]
        stack.append(item)
        print(f"push {item} → стек: {stack}")
    else:
        item = stack.pop()
        print(f"pop → взяли {item}, стек: {stack}")

# 3. Очередь (FIFO) — первый вошёл, первый вышел
from collections import deque
queue = deque()
for name in ["Иван", "Мария", "Пётр"]:
    queue.append(name)
    print(f"Пришёл {name}: {list(queue)}")

while queue:
    name = queue.popleft()
    print(f"Обслужен {name}: осталось {list(queue)}")

# 4. Матрица — перемножение
def matrix_multiply(A, B):
    n = len(A)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
C = matrix_multiply(A, B)
print("\\nПроизведение матриц:")
for row in C:
    print(row)'''
},

{
'title': 'Кортежи, множества и их применение',
'order': 2,
'estimated_minutes': 75,
'content': '''
<h2>Кортеж (tuple) — неизменяемый список</h2>
<p>Кортеж похож на список, но после создания его нельзя изменить. Это делает его:</p>
<ul>
  <li>Быстрее списка (нет накладных расходов на изменяемость)</li>
  <li>Безопаснее — защита данных от случайного изменения</li>
  <li>Хешируемым — можно использовать как ключ словаря</li>
  <li>Семантически чётким — «эти данные не должны меняться»</li>
</ul>
<pre><code>t1 = (1, 2, 3)
t2 = 1, 2, 3          # скобки необязательны!
t3 = (42,)             # кортеж из ОДНОГО элемента — нужна запятая!
t4 = ()                # пустой кортеж
t5 = tuple([1,2,3])    # из списка</code></pre>
''' + warn('(42) — это НЕ кортеж, это просто число 42 в скобках. Для кортежа из одного элемента нужна запятая: (42,)') + '''

<h3>Распаковка кортежей</h3>
<pre><code># Функция возвращает несколько значений через кортеж
def divide(a, b):
    return a // b, a % b   # возвращает кортеж

quotient, remainder = divide(17, 5)  # распаковка
print(f"{quotient} остаток {remainder}")

# Обмен переменных
x, y = y, x  # через кортеж — питонично!

# Расширенная распаковка
first, *middle, last = (1, 2, 3, 4, 5)</code></pre>

<h3>Именованные кортежи (namedtuple)</h3>
<pre><code>from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)         # 3 4
print(p[0], p[1])       # 3 4 — доступ по индексу тоже работает
print(p)                # Point(x=3, y=4)

Student = namedtuple("Student", ["name", "age", "gpa"])
ivan = Student("Иван", 21, 4.5)
print(ivan.name, ivan.gpa)</code></pre>

<h2>Множество (set) — уникальные элементы</h2>
<p>Неупорядоченная коллекция уникальных хешируемых объектов. Реализована на хеш-таблице.</p>
<pre><code>s1 = {1, 2, 3, 4, 5}
s2 = set([1, 2, 2, 3, 3])  # {1, 2, 3} — дубликаты удалены
s3 = set("hello")          # {'h', 'e', 'l', 'o'}
empty_set = set()          # НЕЛЬЗЯ {} — это пустой словарь!</code></pre>

<h3>Операции над множествами</h3>
''' + table(
    ['Операция','Оператор','Метод','Описание'],
    [
        ['Объединение','|','s1.union(s2)','Все элементы обоих'],
        ['Пересечение','&','s1.intersection(s2)','Общие элементы'],
        ['Разность','-','s1.difference(s2)','Есть в s1, нет в s2'],
        ['Симм. разность','^','s1.symmetric_difference(s2)','Только в одном из двух'],
        ['Подмножество','<=','s1.issubset(s2)','s1 ⊆ s2'],
        ['Надмножество','>=','s1.issuperset(s2)','s1 ⊇ s2'],
        ['Несвязанные','—','s1.isdisjoint(s2)','Нет общих элементов'],
    ]
) + '''
''' + info('Проверка принадлежности к множеству O(1) — мгновенно, к списку O(n) — медленнее при больших данных.') + '''

<h3>Применение множеств</h3>
<pre><code># Удаление дубликатов из списка
data = [1, 3, 2, 3, 1, 4, 2, 5]
unique = list(set(data))  # порядок не сохраняется!

# Если нужен порядок — dict.fromkeys():
unique_ordered = list(dict.fromkeys(data))  # [1, 3, 2, 4, 5]

# Нахождение общих элементов
group_a = {"Иван", "Мария", "Пётр", "Анна"}
group_b = {"Пётр", "Дмитрий", "Анна", "Елена"}
both = group_a & group_b   # {'Пётр', 'Анна'}
only_a = group_a - group_b # {'Иван', 'Мария'}
all_students = group_a | group_b</code></pre>
''',
'code_example': '''# Кортежи и множества: практика

from collections import namedtuple, Counter

# Именованные кортежи для структурированных данных
Product = namedtuple("Product", ["name", "price", "category"])
catalog = [
    Product("Ноутбук", 45000, "Электроника"),
    Product("Мышь", 800, "Электроника"),
    Product("Стол", 15000, "Мебель"),
    Product("Стул", 5000, "Мебель"),
    Product("Монитор", 20000, "Электроника"),
]

# Фильтрация по категории
electronics = [p for p in catalog if p.category == "Электроника"]
total = sum(p.price for p in electronics)
print(f"Электроника: {len(electronics)} товаров на {total:,} руб.")

# Самый дорогой
most_expensive = max(catalog, key=lambda p: p.price)
print(f"Самый дорогой: {most_expensive.name} ({most_expensive.price:,} руб.)")

# Множества: анализ посещаемости
mon = {"Иван", "Мария", "Пётр", "Анна", "Дмитрий"}
tue = {"Мария", "Анна", "Елена", "Дмитрий"}
wed = {"Иван", "Пётр", "Елена", "Николай"}

print("\\nАнализ посещаемости:")
print(f"Все студенты: {mon | tue | wed}")
print(f"Были все 3 дня: {mon & tue & wed}")
print(f"Только в понедельник: {mon - tue - wed}")
print(f"Прогуляли хоть раз: {(mon | tue | wed) - (mon & tue & wed)}")

# Counter — специальное множество с подсчётом
text = "программирование это искусство создания программ"
word_count = Counter(text.split())
print("\\nТоп-5 слов:")
for word, count in word_count.most_common(5):
    print(f"  '{word}': {count}")

letter_count = Counter(text.replace(" ", ""))
print(f"\\nБуква 'а' встречается {letter_count['а']} раз")'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 8 — СЛОВАРИ И МНОЖЕСТВА (ПРОДВИНУТЫЙ)
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Словари',
'icon': 'fas fa-book-open',
'order': 8,
'description': 'Словари — ключ-значение. Методы, вложенные словари, defaultdict, Counter.',
'lessons': [
{
'title': 'Словари: хранение данных по ключу',
'order': 1,
'estimated_minutes': 85,
'content': '''
<h2>Что такое словарь?</h2>
<p>Словарь (<code>dict</code>) — неупорядоченная* коллекция пар «ключ: значение». Реализован на хеш-таблице, что обеспечивает O(1) доступ, вставку и удаление.</p>
<p>* С Python 3.7+ словари <em>сохраняют порядок вставки</em>.</p>

<h3>Аналогия</h3>
<p>Словарь — как настоящий словарь (книга): по слову (ключу) мгновенно находишь определение (значение). В отличие от списка, где поиск идёт перебором.</p>

<h2>Создание словарей</h2>
<pre><code># Литерал
student = {"name": "Иван", "age": 21, "gpa": 4.5}

# Конструктор dict()
d = dict(name="Иван", age=21)
d = dict([("name", "Иван"), ("age", 21)])

# Из двух списков (zip)
keys = ["a", "b", "c"]
vals = [1, 2, 3]
d = dict(zip(keys, vals))

# Dict comprehension
squares = {n: n**2 for n in range(1, 11)}

# Заполнить одним значением
empty = dict.fromkeys(["x", "y", "z"], 0)
# {"x": 0, "y": 0, "z": 0}</code></pre>

<h2>Требования к ключам</h2>
''' + table(
    ['Тип','Можно ключом','Пример'],
    [
        ['int','Да','d[42] = "answer"'],
        ['str','Да','d["name"] = "Иван"'],
        ['tuple','Да (если неизменяемый)','d[(1,2)] = "точка"'],
        ['float','Да (осторожно!)','d[3.14] = "pi"'],
        ['list','НЕТ — изменяемый','d[[1,2]] → TypeError'],
        ['dict','НЕТ — изменяемый','d[{}] → TypeError'],
        ['set','НЕТ — изменяемый','d[{1,2}] → TypeError'],
    ]
) + '''

<h2>Доступ к данным</h2>
<pre><code>d = {"name": "Иван", "age": 21, "city": "Москва"}

# Обычный доступ (KeyError если нет)
print(d["name"])    # "Иван"
print(d["grade"])   # KeyError!

# Безопасный доступ
print(d.get("grade"))          # None
print(d.get("grade", "N/A"))   # "N/A" — значение по умолчанию

# Проверка ключа
print("name" in d)    # True
print("grade" in d)   # False</code></pre>

<h2>Методы словаря</h2>
''' + table(
    ['Метод','Описание','Пример'],
    [
        ['.keys()','Все ключи','for k in d.keys()'],
        ['.values()','Все значения','for v in d.values()'],
        ['.items()','Пары (ключ, значение)','for k,v in d.items()'],
        ['.get(k, def)','Значение или default','d.get("x", 0)'],
        ['.pop(k)','Удалить и вернуть','d.pop("age")'],
        ['.popitem()','Удалить последний','k, v = d.popitem()'],
        ['.update(d2)','Обновить из другого','d.update({"x": 1})'],
        ['.setdefault(k,v)','Установить если нет','d.setdefault("n", 0)'],
        ['.copy()','Поверхностная копия','d2 = d.copy()'],
        ['.clear()','Очистить','d.clear()'],
    ]
) + '''

<h2>Итерация по словарю</h2>
<pre><code>scores = {"Иван": 85, "Мария": 92, "Пётр": 78}

# По ключам (по умолчанию)
for name in scores:
    print(name)

# По значениям
for score in scores.values():
    print(score)

# По парам (самый частый случай)
for name, score in scores.items():
    print(f"{name}: {score}")

# Сортировка по значению
for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: {score}")</code></pre>

<h2>Вложенные словари</h2>
<pre><code>database = {
    "users": {
        "u001": {"name": "Иван", "role": "student", "gpa": 4.5},
        "u002": {"name": "Мария", "role": "teacher"},
    },
    "courses": {
        "python101": {"title": "Python для начинающих", "students": 25},
    }
}

# Доступ к вложенным данным
print(database["users"]["u001"]["name"])      # "Иван"

# Безопасный доступ к вложенным
user = database.get("users", {}).get("u999", {}).get("name", "Неизвестен")</code></pre>

<h2>defaultdict и Counter</h2>
<pre><code>from collections import defaultdict, Counter

# defaultdict — автоматически создаёт значение по умолчанию
groups = defaultdict(list)
students = [("Иван", "А1"), ("Мария", "Б2"), ("Пётр", "А1"), ("Анна", "Б2")]
for name, group in students:
    groups[group].append(name)
# {"А1": ["Иван", "Пётр"], "Б2": ["Мария", "Анна"]}

# Counter — подсчёт элементов
text = "banana"
freq = Counter(text)
# {'a': 3, 'n': 2, 'b': 1}
print(freq.most_common(2))   # [('a', 3), ('n', 2)]</code></pre>
''',
'code_example': '''from collections import defaultdict, Counter

# 1. Телефонная книга
contacts = {}

def add_contact(name, phone):
    contacts[name] = phone

def find_contact(name):
    return contacts.get(name, "Не найден")

add_contact("Иван", "+7-999-123-45-67")
add_contact("Мария", "+7-999-234-56-78")
add_contact("Пётр", "+7-999-345-67-89")

print(find_contact("Мария"))
print(find_contact("Николай"))

# 2. Подсчёт частоты слов
text = """python это мощный язык программирования
python используется в веб разработке и науке о данных
программирование на python это интересно"""

words = text.split()
freq = Counter(words)
print("\\nТоп-5 слов:")
for word, count in freq.most_common(5):
    bar = "█" * count
    print(f"  {word:<20} {bar} ({count})")

# 3. Группировка данных
students_data = [
    ("Иван", "А1", 85), ("Мария", "Б2", 92),
    ("Пётр", "А1", 78), ("Анна", "Б2", 88),
    ("Дмитрий", "В3", 71), ("Елена", "А1", 95),
]

groups = defaultdict(list)
for name, group, score in students_data:
    groups[group].append((name, score))

print("\\nСредние баллы по группам:")
for group, members in sorted(groups.items()):
    avg = sum(s for _, s in members) / len(members)
    best = max(members, key=lambda x: x[1])
    print(f"  {group}: средний {avg:.1f}, лучший — {best[0]} ({best[1]})")

# 4. Кеш результатов (мемоизация)
cache = {}
def fib(n):
    if n in cache:
        return cache[n]
    if n <= 1:
        result = n
    else:
        result = fib(n-1) + fib(n-2)
    cache[n] = result
    return result

print("\\nФибоначчи с кешем:")
for i in range(0, 15):
    print(f"  fib({i:2}) = {fib(i):5}")'''
},
]
},

]  # конец MODULES


class Command(BaseCommand):
    help = 'Модули 5-8: циклы, функции, списки, словари'

    def handle(self, *args, **options):
        created_l = 0
        for mod_data in MODULES:
            lessons = mod_data.pop('lessons')
            module, _ = TheoryModule.objects.update_or_create(
                title=mod_data['title'], defaults=mod_data)
            for les in lessons:
                _, lc = TheoryLesson.objects.update_or_create(
                    module=module, title=les['title'], defaults=les)
                if lc:
                    created_l += 1

        from django.db.models import Sum
        total = TheoryLesson.objects.aggregate(t=Sum('estimated_minutes'))['t'] or 0
        self.stdout.write(self.style.SUCCESS(
            f'OK  Уроков всего: {TheoryLesson.objects.count()} '
            f'(~{total//60}ч {total%60}мин)'
        ))
