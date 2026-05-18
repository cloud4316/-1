"""python manage.py seed_theory_full3  — модули 9-14"""
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
# МОДУЛЬ 9 — ОБРАБОТКА ОШИБОК
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Обработка ошибок и исключений',
'icon': 'fas fa-exclamation-triangle',
'order': 9,
'description': 'Исключения в Python: try/except/finally, создание собственных ошибок, отладка.',
'lessons': [
{
'title': 'Исключения: try, except, finally, raise',
'order': 1,
'estimated_minutes': 80,
'content': '''
<h2>Что такое исключение?</h2>
<p>Исключение — сигнал об ошибке во время выполнения программы. В отличие от синтаксических ошибок (выявляются до запуска), исключения возникают в процессе работы.</p>

<h3>Два подхода к ошибкам</h3>
''' + table(
    ['Подход','Название','Пример'],
    [
        ['Проверить перед действием','LBYL (Look Before You Leap)','if key in d: x = d[key]'],
        ['Попробовать и обработать','EAFP (Easier to Ask Forgiveness)','try: x = d[key] except KeyError: ...'],
    ]
) + '''
''' + info('Python предпочитает стиль EAFP — попробовать и обработать исключение. Это питонично и зачастую быстрее.') + '''

<h2>Синтаксис try/except</h2>
<pre><code>try:
    # код, который может вызвать исключение
    результат = опасная_операция()
except ТипОшибки as e:
    # обработка конкретной ошибки
    print(f"Ошибка: {e}")
except (TypeError, ValueError) as e:
    # несколько типов в одном блоке
    print(f"Ошибка типа: {e}")
except Exception as e:
    # любая ошибка (широкий перехват)
    print(f"Неизвестная ошибка: {e}")
else:
    # выполняется ТОЛЬКО если не было исключений
    print("Всё прошло успешно!")
finally:
    # выполняется ВСЕГДА (cleanup)
    print("Завершение, освобождение ресурсов")</code></pre>
''' + warn('Не перехватывай слишком широко (except Exception) без веской причины — это скрывает настоящие ошибки.') + '''

<h2>Встроенные исключения</h2>
''' + table(
    ['Исключение','Когда возникает','Пример'],
    [
        ['ValueError','Неверное значение при верном типе','int("abc")'],
        ['TypeError','Неверный тип операнда','1 + "a"'],
        ['ZeroDivisionError','Деление на ноль','1 / 0'],
        ['IndexError','Индекс за пределами','[1,2][5]'],
        ['KeyError','Ключ не найден','{}["x"]'],
        ['AttributeError','Атрибут/метод не существует','None.upper()'],
        ['NameError','Имя не определено','print(undefined_var)'],
        ['FileNotFoundError','Файл не существует','open("nope.txt")'],
        ['ImportError','Модуль не найден','import nonexistent'],
        ['RecursionError','Превышена глубина рекурсии','бесконечная рекурсия'],
        ['StopIteration','Итератор исчерпан','next(iter([]))'],
        ['OverflowError','Число слишком велико для float','float overflow'],
        ['MemoryError','Не хватает памяти','[0]*10**12'],
        ['OSError','Ошибка операции ОС','disk full, permission'],
    ]
) + '''

<h2>Иерархия исключений</h2>
<pre><code>BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 └── Exception
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── TypeError
      ├── ValueError
      ├── AttributeError
      ├── NameError
      ├── IOError / OSError
      └── RuntimeError
           └── RecursionError</code></pre>
''' + tip('Перехватывай конкретный тип исключения, а не базовый. <code>except ZeroDivisionError</code> лучше чем <code>except Exception</code>.') + '''

<h2>Создание собственных исключений</h2>
<pre><code>class ValidationError(ValueError):
    """Ошибка валидации данных."""
    def __init__(self, field, message):
        self.field = field
        super().__init__(f"Поле '{field}': {message}")

class AgeError(ValidationError):
    pass

def validate_age(age):
    if not isinstance(age, int):
        raise TypeError(f"Возраст должен быть целым числом, получен {type(age).__name__}")
    if age < 0:
        raise AgeError("age", "не может быть отрицательным")
    if age > 150:
        raise AgeError("age", f"значение {age} нереалистично")
    return True

try:
    validate_age(-5)
except AgeError as e:
    print(f"Ошибка валидации: {e}")
    print(f"Поле: {e.field}")</code></pre>

<h2>Оператор raise</h2>
<pre><code># Вызвать новое исключение
raise ValueError("Некорректное значение")

# Повторно вызвать текущее исключение
try:
    risky()
except ValueError:
    log_error()
    raise  # то же исключение дальше

# Цепочка исключений (chaining)
try:
    process()
except IOError as e:
    raise RuntimeError("Ошибка обработки") from e</code></pre>

<h2>Контекстный менеджер (with)</h2>
<p>Автоматически освобождает ресурсы, даже при исключении:</p>
<pre><code># Без with (опасно):
f = open("file.txt")
data = f.read()    # если здесь ошибка — файл не закроется!
f.close()

# С with (правильно):
with open("file.txt") as f:
    data = f.read()
# f.close() вызывается автоматически

# Несколько ресурсов:
with open("input.txt") as fin, open("output.txt", "w") as fout:
    fout.write(fin.read())</code></pre>
''' + tip('Всегда открывай файлы через <code>with</code>. Это гарантирует закрытие даже при исключении.') + '''

<h2>Отладка: traceback</h2>
<p>Python выводит трассировку стека (traceback) при необработанном исключении. Читай снизу вверх:</p>
<ul>
  <li>Последняя строка — тип и сообщение ошибки</li>
  <li>Строки выше — цепочка вызовов (где именно произошло)</li>
  <li>Файл и номер строки — точное место</li>
</ul>
''',
'code_example': '''# Практика: обработка исключений

def safe_int(value, default=0):
    """Безопасное преобразование в int."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

print(safe_int("42"))     # 42
print(safe_int("abc"))    # 0
print(safe_int(None))     # 0
print(safe_int("3.14"))   # 0 (int("3.14") тоже ошибка!)

# Калькулятор с полной обработкой ошибок
def calculator(expression):
    """Безопасный калькулятор строкового выражения."""
    try:
        parts = expression.strip().split()
        if len(parts) != 3:
            raise ValueError(f"Формат: число оператор число, получено: {expression}")

        a = float(parts[0])
        op = parts[1]
        b = float(parts[2])

        match op:
            case "+": return a + b
            case "-": return a - b
            case "*": return a * b
            case "/":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                return a / b
            case "**": return a ** b
            case _:
                raise ValueError(f"Неизвестный оператор: {op}")

    except ValueError as e:
        return f"Ошибка значения: {e}"
    except ZeroDivisionError as e:
        return f"Математическая ошибка: {e}"
    except Exception as e:
        return f"Неожиданная ошибка: {e}"

tests = ["10 + 5", "10 / 0", "abc + 5", "2 ** 8", "10 / 3", "bad input"]
for expr in tests:
    result = calculator(expr)
    print(f"  {expr:<20} = {result}")

# Пользовательские исключения
class InventoryError(Exception):
    pass

class OutOfStockError(InventoryError):
    def __init__(self, item, requested, available):
        self.item = item
        self.requested = requested
        self.available = available
        super().__init__(
            f"Товар '{item}': запрошено {requested}, доступно {available}"
        )

inventory = {"яблоки": 10, "бананы": 5, "апельсины": 0}

def purchase(item, quantity):
    if item not in inventory:
        raise InventoryError(f"Товар '{item}' не существует")
    if inventory[item] < quantity:
        raise OutOfStockError(item, quantity, inventory[item])
    inventory[item] -= quantity
    return f"Куплено {quantity} шт. '{item}'"

test_purchases = [("яблоки", 3), ("бананы", 10), ("апельсины", 1), ("манго", 2)]
for item, qty in test_purchases:
    try:
        print(purchase(item, qty))
    except OutOfStockError as e:
        print(f"Нет в наличии: {e}")
    except InventoryError as e:
        print(f"Ошибка: {e}")'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 10 — АЛГОРИТМЫ СОРТИРОВКИ
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Алгоритмы сортировки',
'icon': 'fas fa-sort',
'order': 10,
'description': 'Пузырьковая, выборочная, вставками, быстрая, слиянием. Сложность O(n²) vs O(n log n).',
'lessons': [
{
'title': 'Квадратичные алгоритмы сортировки',
'order': 1,
'estimated_minutes': 90,
'content': '''
<h2>Зачем изучать алгоритмы сортировки?</h2>
<p>Сортировка — один из самых изученных алгоритмических классов. Причины:</p>
<ul>
  <li>Фундаментальная задача CS — встречается в каждом реальном приложении</li>
  <li>Прекрасно иллюстрирует анализ сложности алгоритмов</li>
  <li>Паттерны «сравни и переставь» используются в других алгоритмах</li>
  <li>На собеседованиях — обязательная тема</li>
</ul>

<h2>Нотация O-большое (Big-O)</h2>
<p>Описывает рост времени выполнения при увеличении размера входа n:</p>
''' + table(
    ['Сложность','Название','Пример при n=1000','Пример'],
    [
        ['O(1)','Константная','1 операция','Доступ к элементу по индексу'],
        ['O(log n)','Логарифмическая','≈10 операций','Двоичный поиск'],
        ['O(n)','Линейная','1 000 операций','Линейный поиск'],
        ['O(n log n)','Линейно-логарифмическая','≈10 000 операций','Быстрая, слияниями'],
        ['O(n²)','Квадратичная','1 000 000 операций','Пузырьковая, вставками'],
        ['O(2ⁿ)','Экспоненциальная','10³⁰⁰ операций','Перебор всех подмножеств'],
    ]
) + '''

<h2>Сортировка пузырьком (Bubble Sort)</h2>
<p>Принцип: сравниваем соседние элементы и меняем местами, если они стоят не в том порядке. После одного прохода максимальный элемент «всплывает» в конец.</p>
<ul>
  <li>Время: O(n²) в среднем и худшем, O(n) в лучшем (уже отсортированный)</li>
  <li>Память: O(1) — сортировка «на месте»</li>
  <li>Стабильная: одинаковые элементы не меняют порядка</li>
  <li>Практическое применение: только обучение</li>
</ul>
<pre><code>def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:     # оптимизация: уже отсортировано
            break
    return arr</code></pre>

<h3>Визуализация на [64, 34, 25, 12, 22]</h3>
<pre><code>Проход 1: [34, 25, 12, 22, 64]  ← 64 на месте
Проход 2: [25, 12, 22, 34, 64]  ← 34 на месте
Проход 3: [12, 22, 25, 34, 64]  ← 25 на месте
Проход 4: [12, 22, 25, 34, 64]  ← готово, нет перестановок</code></pre>

<h2>Сортировка выбором (Selection Sort)</h2>
<p>Принцип: найти минимальный элемент в неотсортированной части и поставить его на нужное место.</p>
<ul>
  <li>Время: O(n²) всегда — не улучшается даже для отсортированного массива</li>
  <li>Память: O(1)</li>
  <li>Нестабильная: одинаковые элементы могут менять порядок</li>
  <li>Плюс: минимальное количество перестановок (O(n))</li>
</ul>
<pre><code>def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr</code></pre>

<h2>Сортировка вставками (Insertion Sort)</h2>
<p>Принцип: берём элемент и вставляем его на нужное место в уже отсортированную левую часть. Аналог того, как люди сортируют карты в руке.</p>
<ul>
  <li>Время: O(n²) в среднем и худшем, O(n) для почти отсортированных данных</li>
  <li>Память: O(1)</li>
  <li>Стабильная</li>
  <li>Практическое применение: для малых массивов (n &lt; 50) эффективнее быстрой сортировки</li>
  <li>Использование: Python's timsort использует вставками для небольших блоков</li>
</ul>
<pre><code>def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr</code></pre>

<h2>Сравнение квадратичных алгоритмов</h2>
''' + table(
    ['Алгоритм','Лучший случай','Средний','Худший','Память','Стабильная'],
    [
        ['Пузырьковая','O(n)','O(n²)','O(n²)','O(1)','Да'],
        ['Выбором','O(n²)','O(n²)','O(n²)','O(1)','Нет'],
        ['Вставками','O(n)','O(n²)','O(n²)','O(1)','Да'],
    ]
) + '''
''' + info('При n=10000 квадратичные алгоритмы делают ≈100 000 000 операций. На современном ПК это ~1 секунда. При n=100000 — уже 100 секунд!'),
'code_example': '''import time
import random

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    comparisons = swaps = 0
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            comparisons += 1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return arr, comparisons, swaps

def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)
    comparisons = swaps = 0
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return arr, comparisons, swaps

def insertion_sort(arr):
    arr = arr.copy()
    n = len(arr)
    comparisons = swaps = 0
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j+1] = arr[j]
            j -= 1
            swaps += 1
        comparisons += 1 if j >= 0 else 0
        arr[j+1] = key
    return arr, comparisons, swaps

# Сравниваем алгоритмы
random.seed(42)
data = [random.randint(1, 100) for _ in range(50)]
print(f"Массив ({len(data)} элементов): {data[:10]}...")

print(f"\\n{'Алгоритм':<20} {'Сравнений':>12} {'Перестановок':>14} {'Время':>10}")
print("-" * 60)

for name, func in [("Пузырьковая", bubble_sort),
                   ("Выбором", selection_sort),
                   ("Вставками", insertion_sort)]:
    start = time.perf_counter()
    sorted_arr, comps, swaps = func(data)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{name:<20} {comps:>12} {swaps:>14} {elapsed:>9.3f}ms")

# Проверка на разных данных
print("\\nЛучший случай (уже отсортировано):")
sorted_data = list(range(50))
for name, func in [("Пузырьковая", bubble_sort), ("Вставками", insertion_sort)]:
    _, comps, _ = func(sorted_data)
    print(f"  {name}: {comps} сравнений")'''
},

{
'title': 'Быстрая сортировка и сортировка слиянием',
'order': 2,
'estimated_minutes': 90,
'content': '''
<h2>Принцип «разделяй и властвуй»</h2>
<p>Эффективные алгоритмы сортировки используют рекурсию и стратегию divide & conquer:</p>
<ol>
  <li><strong>Разделить</strong> — разбить задачу на подзадачи</li>
  <li><strong>Завоевать</strong> — решить каждую подзадачу рекурсивно</li>
  <li><strong>Объединить</strong> — собрать результаты</li>
</ol>

<h2>Сортировка слиянием (Merge Sort)</h2>
<p>Принцип: рекурсивно разделить массив пополам, отсортировать каждую половину, затем слить две отсортированные половины.</p>
<ul>
  <li>Время: O(n log n) всегда — гарантированно!</li>
  <li>Память: O(n) — нужен дополнительный массив для слияния</li>
  <li>Стабильная</li>
  <li>Применение: внешняя сортировка (файлы), Java Arrays.sort для объектов</li>
</ul>
<pre><code>def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result</code></pre>

<h3>Визуализация слияния</h3>
<pre><code>[38, 27, 43, 3, 9, 82, 10]
         ↓ split
[38, 27, 43]   [3, 9, 82, 10]
     ↓ split         ↓ split
[38] [27,43]  [3,9]  [82,10]
      ↓ merge   ↓ merge  ↓ merge
[38] [27,43]  [3,9]  [10,82]
     ↓ merge         ↓ merge
  [27,38,43]       [3,9,10,82]
         ↓ merge
  [3, 9, 10, 27, 38, 43, 82]</code></pre>

<h2>Быстрая сортировка (Quick Sort)</h2>
<p>Принцип: выбрать опорный элемент (pivot), разбить массив на «меньше опорного» и «больше опорного», рекурсивно отсортировать каждую часть.</p>
<ul>
  <li>Время: O(n log n) в среднем, O(n²) в худшем (уже отсортированный + плохой выбор pivot)</li>
  <li>Память: O(log n) — стек вызовов</li>
  <li>Нестабильная в классической реализации</li>
  <li>Применение: C++ std::sort, Python sorted() использует Timsort (гибрид)</li>
</ul>
<pre><code>def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]  # медиана — лучше, чем первый элемент
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)</code></pre>

<h2>Timsort — алгоритм Python</h2>
<p>Python (CPython) использует Timsort в <code>list.sort()</code> и <code>sorted()</code>:</p>
<ul>
  <li>Гибрид сортировки слиянием и сортировки вставками</li>
  <li>O(n log n) в худшем, O(n) для почти отсортированных данных</li>
  <li>Стабильная</li>
  <li>Разработан Тимом Петерсом специально для Python (2002)</li>
  <li>Сейчас используется в Java (Arrays.sort для объектов), Android, Swift</li>
</ul>
''' + tip('Встроенная <code>sorted()</code> и <code>list.sort()</code> в Python написаны на C и оптимизированы до предела. В реальных задачах используй их, а не собственные реализации.') + '''

<h2>Итоговое сравнение всех алгоритмов</h2>
''' + table(
    ['Алгоритм','Лучший','Средний','Худший','Память','Стабильная','Применение'],
    [
        ['Пузырьковая','O(n)','O(n²)','O(n²)','O(1)','Да','Обучение'],
        ['Выбором','O(n²)','O(n²)','O(n²)','O(1)','Нет','Редко'],
        ['Вставками','O(n)','O(n²)','O(n²)','O(1)','Да','Малые массивы, онлайн-сортировка'],
        ['Слиянием','O(n logn)','O(n logn)','O(n logn)','O(n)','Да','Внешняя сортировка, большие данные'],
        ['Быстрая','O(n logn)','O(n logn)','O(n²)','O(logn)','Нет','Массивы, реальные задачи'],
        ['Timsort','O(n)','O(n logn)','O(n logn)','O(n)','Да','Python, Java, Android'],
        ['Пирамидальная','O(n logn)','O(n logn)','O(n logn)','O(1)','Нет','Priority queue'],
    ]
),
'code_example': '''import random
import time

def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))

def merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result

def quick_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr)//2]
    return (quick_sort([x for x in arr if x < pivot]) +
            [x for x in arr if x == pivot] +
            quick_sort([x for x in arr if x > pivot]))

# Сравнение производительности
random.seed(42)
sizes = [100, 500, 1000, 5000]

print(f"{'N':>6} {'Слияние':>10} {'Быстрая':>10} {'sorted()':>10}")
print("-" * 42)
for n in sizes:
    data = [random.randint(1, 10000) for _ in range(n)]

    t1 = time.perf_counter()
    for _ in range(5): merge_sort(data)
    t1 = (time.perf_counter() - t1) / 5 * 1000

    t2 = time.perf_counter()
    for _ in range(5): quick_sort(data)
    t2 = (time.perf_counter() - t2) / 5 * 1000

    t3 = time.perf_counter()
    for _ in range(5): sorted(data)
    t3 = (time.perf_counter() - t3) / 5 * 1000

    print(f"{n:>6} {t1:>9.2f}ms {t2:>9.2f}ms {t3:>9.2f}ms")

# Сортировка по нескольким ключам
students = [
    ("Иван", 21, 4.5), ("Мария", 21, 4.8),
    ("Пётр", 20, 4.5), ("Анна", 22, 4.2),
    ("Дмитрий", 20, 4.9),
]

# Сначала по GPA убыванию, потом по имени
ranked = sorted(students, key=lambda s: (-s[2], s[0]))
print("\\nРейтинг студентов:")
for i, (name, age, gpa) in enumerate(ranked, 1):
    print(f"  {i}. {name:<12} GPA: {gpa:.1f}  Возраст: {age}")'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 11 — РЕКУРСИЯ
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Рекурсия',
'icon': 'fas fa-redo',
'order': 11,
'description': 'Функции, вызывающие сами себя. Базовый случай, стек вызовов, мемоизация.',
'lessons': [
{
'title': 'Рекурсия: суть, принципы, практика',
'order': 1,
'estimated_minutes': 85,
'content': '''
<h2>Что такое рекурсия?</h2>
<p>Рекурсия — это когда функция вызывает саму себя для решения подзадачи меньшего размера. Это не просто приём — это особый способ мышления.</p>

<blockquote style="border-left:4px solid #6366f1;padding-left:1rem;color:#64748b;font-style:italic">
«Чтобы понять рекурсию, нужно сначала понять рекурсию.» — старая программистская шутка
</blockquote>

<h2>Два обязательных компонента</h2>
<ul>
  <li><strong>Базовый случай</strong> (base case) — условие остановки. Без него рекурсия бесконечна → RecursionError.</li>
  <li><strong>Рекурсивный случай</strong> — вызов себя с упрощённой задачей, которая приближает к базовому случаю.</li>
</ul>

<h2>Стек вызовов</h2>
<p>Каждый вызов функции добавляет <strong>фрейм</strong> в стек вызовов (call stack). При рекурсии фреймы накапливаются:</p>
<pre><code>factorial(4)
  → factorial(3)
      → factorial(2)
          → factorial(1)
              → return 1
          ← return 2 * 1 = 2
      ← return 3 * 2 = 6
  ← return 4 * 6 = 24</code></pre>
''' + warn('Python ограничивает глубину рекурсии по умолчанию до 1000. Для глубоких рекурсий используй итеративный подход или sys.setrecursionlimit().') + '''

<h2>Классические примеры</h2>

<h3>1. Факториал</h3>
<pre><code>def factorial(n):
    if n <= 1:      # базовый случай
        return 1
    return n * factorial(n - 1)  # рекурсивный случай</code></pre>

<h3>2. Числа Фибоначчи</h3>
<pre><code># Наивная версия — очень медленно!
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n-1) + fib_naive(n-2)
# fib_naive(40) — ~2 минуты!

# С мемоизацией — быстро!
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
# fib(1000) — мгновенно</code></pre>

<h3>3. Двоичный поиск рекурсивно</h3>
<pre><code>def binary_search(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)</code></pre>

<h2>Рекурсия vs Итерация</h2>
''' + table(
    ['Критерий','Рекурсия','Итерация'],
    [
        ['Читаемость','Лучше для древовидных задач','Лучше для линейных'],
        ['Скорость','Медленнее (накладные расходы на стек)','Быстрее'],
        ['Память','O(n) для стека','O(1) обычно'],
        ['Ограничения','Лимит стека (1000 по умолчанию)','Нет ограничений'],
        ['Применение','Деревья, графы, разделяй и властвуй','Массивы, списки, простые циклы'],
    ]
) + '''

<h2>Мемоизация и @lru_cache</h2>
<p>Мемоизация — кеширование результатов функции для избежания повторных вычислений:</p>
<pre><code>from functools import lru_cache

@lru_cache(maxsize=None)   # кеш без ограничений
def expensive(n):
    ...

# Узнать размер кеша:
print(expensive.cache_info())</code></pre>
''' + tip('@lru_cache превращает экспоненциальный O(2ⁿ) алгоритм Фибоначчи в линейный O(n).') + '''

<h2>Рекурсия для работы с деревьями</h2>
<p>Деревья — самая естественная область применения рекурсии. Папка на диске — дерево. HTML-страница — дерево. Файловая система — дерево.</p>
<pre><code>def count_files(path):
    """Рекурсивно подсчитать файлы в директории."""
    import os
    total = 0
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path):
            total += 1
        elif os.path.isdir(full_path):
            total += count_files(full_path)  # рекурсия!
    return total</code></pre>

<h2>Ханойские башни</h2>
<p>Классическая задача: переставить n дисков с колышка A на колышек C через B, не кладя больший диск на меньший.</p>
<pre><code>def hanoi(n, source="A", target="C", auxiliary="B"):
    if n == 1:
        print(f"Переместить диск 1: {source} → {target}")
        return
    hanoi(n-1, source, auxiliary, target)
    print(f"Переместить диск {n}: {source} → {target}")
    hanoi(n-1, auxiliary, target, source)
# Для n дисков нужно 2ⁿ - 1 ходов!</code></pre>
''',
'code_example': '''from functools import lru_cache
import sys

# 1. Факториал с демонстрацией стека
def factorial_verbose(n, depth=0):
    indent = "  " * depth
    print(f"{indent}factorial({n}) вызван")
    if n <= 1:
        print(f"{indent}→ базовый случай, возврат 1")
        return 1
    result = n * factorial_verbose(n - 1, depth + 1)
    print(f"{indent}→ {n} * ... = {result}")
    return result

print("Трассировка factorial(4):")
print(f"Результат: {factorial_verbose(4)}")

# 2. Фибоначчи: сравнение наивного и с кешем
@lru_cache(maxsize=None)
def fib_cached(n):
    if n <= 1: return n
    return fib_cached(n-1) + fib_cached(n-2)

def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

import time
print("\\nФибоначчи (сравнение):")
for n in [10, 30, 50, 100]:
    t1 = time.perf_counter()
    r1 = fib_cached(n)
    t1 = (time.perf_counter() - t1) * 1e6

    t2 = time.perf_counter()
    r2 = fib_iterative(n)
    t2 = (time.perf_counter() - t2) * 1e6

    print(f"  fib({n:3}): кеш={t1:.1f}μs, итер={t2:.1f}μs, значение={r1}")

# 3. Рекурсивная структура: вложенные списки
def flatten(lst):
    """Разворачивает вложенные списки любой глубины."""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

nested = [1, [2, 3, [4, 5]], [6, [7, [8, 9]]], 10]
print(f"\\nВложенный: {nested}")
print(f"Плоский:   {flatten(nested)}")

# 4. Ханойские башни
def hanoi(n, source="A", target="C", via="B"):
    if n == 1:
        return [(source, target)]
    moves = []
    moves.extend(hanoi(n-1, source, via, target))
    moves.append((source, target))
    moves.extend(hanoi(n-1, via, target, source))
    return moves

for disks in [2, 3, 4]:
    moves = hanoi(disks)
    print(f"\\n{disks} дисков: {len(moves)} ходов (2^{disks}-1={2**disks-1})")
    if disks <= 3:
        for i, (src, dst) in enumerate(moves, 1):
            print(f"  Ход {i}: {src} → {dst}")'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 12 — РАБОТА С ФАЙЛАМИ
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Работа с файлами',
'icon': 'fas fa-file-code',
'order': 12,
'description': 'Чтение и запись файлов. Текстовые и бинарные. CSV, JSON, os.path, pathlib.',
'lessons': [
{
'title': 'Файловый ввод-вывод в Python',
'order': 1,
'estimated_minutes': 80,
'content': '''
<h2>Работа с файлами</h2>
<p>Файлы позволяют данным «пережить» завершение программы. Без файлов (и БД) каждый запуск начинается с нуля.</p>

<h2>Открытие файлов: функция open()</h2>
<pre><code>open(file, mode='r', encoding=None, errors=None)</code></pre>
''' + table(
    ['Режим','Описание','Файл существует','Файл не существует'],
    [
        ["'r'","Чтение (по умолчанию)","Открывается","FileNotFoundError"],
        ["'w'","Запись (перезапись)","Очищается","Создаётся"],
        ["'a'","Добавление в конец","Дополняется","Создаётся"],
        ["'x'","Создание (ошибка если есть)","FileExistsError","Создаётся"],
        ["'r+'","Чтение и запись","Открывается","FileNotFoundError"],
        ["'b'","Двоичный режим (добавляется)","'rb', 'wb', 'ab'","—"],
    ]
) + '''
''' + warn('Всегда закрывай файл после работы. Лучший способ — контекстный менеджер <code>with</code>.') + '''

<h2>Чтение файлов</h2>
<pre><code>with open("data.txt", "r", encoding="utf-8") as f:
    # Вариант 1: весь файл в строку
    content = f.read()

    # Вариант 2: список строк
    lines = f.readlines()

    # Вариант 3: построчно (экономит память!)
    for line in f:
        process(line.rstrip("\\n"))</code></pre>

<h2>Запись в файлы</h2>
<pre><code>with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Первая строка\\n")
    f.write("Вторая строка\\n")

    # Несколько строк сразу:
    lines = ["строка 1\\n", "строка 2\\n", "строка 3\\n"]
    f.writelines(lines)

# Добавление в конец:
with open("log.txt", "a", encoding="utf-8") as f:
    f.write(f"Запись добавлена\\n")</code></pre>

<h2>CSV файлы</h2>
<p>CSV (Comma-Separated Values) — самый распространённый формат табличных данных.</p>
<pre><code>import csv

# Запись CSV
students = [["Иван", 21, 4.5], ["Мария", 22, 4.8]]
with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Имя", "Возраст", "ОценкаГПА"])  # заголовок
    writer.writerows(students)

# Чтение CSV
with open("students.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["Имя"], row["ОценкаГПА"])

# DictReader — каждая строка как словарь</code></pre>

<h2>JSON файлы</h2>
<p>JSON (JavaScript Object Notation) — стандарт обмена данными в веб. Легко читается человеком.</p>
<pre><code>import json

data = {"name": "Иван", "scores": [85, 90, 78], "active": True}

# Запись JSON
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Чтение JSON
with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)

# Строка ↔ JSON
json_str = json.dumps(data, ensure_ascii=False)
data2 = json.loads(json_str)</code></pre>

<h2>pathlib — современная работа с путями</h2>
<pre><code>from pathlib import Path

# Создание пути
p = Path("data") / "students" / "group_a.csv"
# data/students/group_a.csv

print(p.name)        # group_a.csv
print(p.stem)        # group_a
print(p.suffix)      # .csv
print(p.parent)      # data/students

# Создание директории
p.parent.mkdir(parents=True, exist_ok=True)

# Чтение файла через pathlib
text = Path("readme.txt").read_text(encoding="utf-8")

# Обход файлов
for csv_file in Path(".").glob("**/*.csv"):
    print(csv_file)</code></pre>
''',
'code_example': '''import json
import csv
import os
from pathlib import Path

# Создаём временный файл для демонстрации
sample_data = """Имя,Группа,Балл1,Балл2,Балл3
Иван Петров,А1,85,92,78
Мария Иванова,А1,92,88,95
Пётр Сидоров,Б2,70,75,68
Анна Козлова,Б2,88,91,84
Дмитрий Новиков,В3,60,65,58
"""

# Записываем CSV
with open("students.csv", "w", encoding="utf-8", newline="") as f:
    f.write(sample_data)

# Читаем и обрабатываем CSV
results = []
with open("students.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        scores = [int(row["Балл1"]), int(row["Балл2"]), int(row["Балл3"])]
        avg = sum(scores) / len(scores)
        results.append({
            "name": row["Имя"],
            "group": row["Группа"],
            "scores": scores,
            "average": round(avg, 1),
            "grade": "Отл" if avg >= 90 else "Хор" if avg >= 75 else "Уд"
        })

# Выводим таблицу
print(f"{'Имя':<20} {'Группа':<6} {'Средний':>8} {'Оценка':>7}")
print("-" * 45)
for s in sorted(results, key=lambda x: -x["average"]):
    print(f"{s['name']:<20} {s['group']:<6} {s['average']:>8.1f} {s['grade']:>7}")

# Сохраняем в JSON
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\\nJSON сохранён. Первая запись:")
with open("results.json", encoding="utf-8") as f:
    data = json.load(f)
print(json.dumps(data[0], ensure_ascii=False, indent=2))

# Удаляем временные файлы
for fname in ["students.csv", "results.json"]:
    if os.path.exists(fname):
        os.remove(fname)
        print(f"Удалён: {fname}")'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 13 — ООП
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Объектно-ориентированное программирование',
'icon': 'fas fa-cubes',
'order': 13,
'description': 'Классы, объекты, инкапсуляция, наследование, полиморфизм. Dunder-методы.',
'lessons': [
{
'title': 'Классы и объекты в Python',
'order': 1,
'estimated_minutes': 95,
'content': '''
<h2>Что такое ООП?</h2>
<p>Объектно-ориентированное программирование — парадигма, в которой программа строится из объектов, каждый из которых объединяет <strong>данные</strong> (атрибуты) и <strong>поведение</strong> (методы).</p>

<h3>Четыре принципа ООП:</h3>
<ul>
  <li><strong>Инкапсуляция</strong> — скрытие внутренних деталей, предоставление интерфейса</li>
  <li><strong>Наследование</strong> — создание новых классов на основе существующих</li>
  <li><strong>Полиморфизм</strong> — одинаковый интерфейс для разных типов</li>
  <li><strong>Абстракция</strong> — выделение существенных характеристик</li>
</ul>

<h2>Класс и объект</h2>
<ul>
  <li><strong>Класс</strong> — шаблон (чертёж). Описывает что за объект и как себя ведёт.</li>
  <li><strong>Объект (экземпляр)</strong> — конкретный представитель класса с конкретными данными.</li>
</ul>
<p>Класс «Студент» описывает: есть имя, есть возраст, можно учиться. Объект «Иван Петров, 21 год» — конкретный студент.</p>

<h2>Определение класса</h2>
<pre><code>class Student:
    # Атрибут класса (общий для всех экземпляров)
    institution = "ОАИП University"

    def __init__(self, name, age, group):
        # Атрибуты экземпляра (уникальные для каждого)
        self.name = name
        self.age = age
        self.group = group
        self.grades = []    # изменяемый — создаём в __init__!

    def add_grade(self, subject, score):
        self.grades.append({"subject": subject, "score": score})

    def average(self):
        if not self.grades:
            return 0.0
        return sum(g["score"] for g in self.grades) / len(self.grades)

    def __str__(self):
        return f"Student({self.name}, группа {self.group})"

    def __repr__(self):
        return f"Student(name={self.name!r}, age={self.age}, group={self.group!r})"</code></pre>

<h2>Dunder-методы (магические методы)</h2>
''' + table(
    ['Метод','Когда вызывается','Пример использования'],
    [
        ['__init__','При создании объекта','obj = MyClass(args)'],
        ['__str__','str(obj), print(obj)','Читаемое описание'],
        ['__repr__','repr(obj), отладчик','Точное техническое описание'],
        ['__len__','len(obj)','Длина/размер'],
        ['__eq__','obj1 == obj2','Равенство'],
        ['__lt__','obj1 < obj2','Сравнение (для sort)'],
        ['__add__','obj1 + obj2','Сложение'],
        ['__contains__','x in obj','Принадлежность'],
        ['__iter__','for x in obj','Итерация'],
        ['__getitem__','obj[key]','Индексация'],
    ]
) + '''

<h2>Наследование</h2>
<pre><code>class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Привет, я {self.name}"

class Student(Person):   # Student наследует Person
    def __init__(self, name, age, group):
        super().__init__(name, age)   # вызов конструктора родителя
        self.group = group

    def greet(self):     # переопределение метода
        base = super().greet()
        return f"{base}, студент группы {self.group}"

class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def greet(self):
        base = super().greet()
        return f"{base}, преподаю {self.subject}"</code></pre>

<h2>Инкапсуляция и свойства</h2>
<pre><code>class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance    # приватный (name mangling)

    @property
    def balance(self):              # getter
        return self.__balance

    @balance.setter
    def balance(self, amount):      # setter с валидацией
        if amount < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self.__balance = amount

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Недостаточно средств")
        self.__balance -= amount
        return self.__balance</code></pre>
''' + tip('@property позволяет контролировать доступ к атрибутам: добавить валидацию, вычисляемые значения, логирование.') + '''

<h2>dataclass — классы данных (Python 3.7+)</h2>
<pre><code>from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

p1 = Point(0, 0)
p2 = Point(3, 4)
print(p1)                # Point(x=0, y=0)
print(p1.distance_to(p2))  # 5.0
# __init__, __repr__, __eq__ генерируются автоматически!</code></pre>
''',
'code_example': '''from dataclasses import dataclass, field
from typing import List

@dataclass
class Student:
    name: str
    age: int
    group: str
    grades: List[float] = field(default_factory=list)

    def add_grade(self, score: float):
        if not 0 <= score <= 100:
            raise ValueError(f"Оценка должна быть 0-100, получено {score}")
        self.grades.append(score)

    @property
    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0.0

    @property
    def letter_grade(self):
        avg = self.average
        if avg >= 90: return "A"
        if avg >= 80: return "B"
        if avg >= 70: return "C"
        if avg >= 60: return "D"
        return "F"

    def __lt__(self, other):
        return self.average < other.average


class Group:
    def __init__(self, name):
        self.name = name
        self.students: List[Student] = []

    def add_student(self, student):
        self.students.append(student)

    def top_students(self, n=3):
        return sorted(self.students, reverse=True)[:n]

    def statistics(self):
        if not self.students:
            return {}
        avgs = [s.average for s in self.students]
        return {
            "count": len(self.students),
            "mean": sum(avgs) / len(avgs),
            "best": max(avgs),
            "worst": min(avgs),
        }

    def __repr__(self):
        return f"Group({self.name}, {len(self.students)} студентов)"


# Демонстрация
group = Group("А1")
data = [
    ("Иван Петров", 21, [85, 92, 78, 88]),
    ("Мария Иванова", 20, [92, 95, 98, 91]),
    ("Пётр Сидоров", 22, [70, 65, 72, 68]),
    ("Анна Козлова", 21, [88, 85, 90, 87]),
    ("Дмитрий Новиков", 20, [60, 68, 62, 65]),
]

for name, age, grades in data:
    s = Student(name, age, "А1")
    for g in grades:
        s.add_grade(g)
    group.add_student(s)

print(f"Группа: {group}")
stats = group.statistics()
print(f"Средний балл: {stats['mean']:.1f}")
print(f"Лучший: {stats['best']:.1f}, Худший: {stats['worst']:.1f}")

print("\\nТоп-3 студента:")
for i, s in enumerate(group.top_students(), 1):
    print(f"  {i}. {s.name:<20} {s.average:>6.1f} ({s.letter_grade})")

print("\\nРаспределение оценок:")
from collections import Counter
dist = Counter(s.letter_grade for s in group.students)
for grade in "ABCDF":
    count = dist.get(grade, 0)
    bar = "█" * count
    print(f"  {grade}: {bar} ({count})")'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 14 — МОДУЛИ И СТАНДАРТНАЯ БИБЛИОТЕКА
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Модули и стандартная библиотека Python',
'icon': 'fas fa-puzzle-piece',
'order': 14,
'description': 'import, пакеты, обзор стандартной библиотеки: os, sys, datetime, random, collections.',
'lessons': [
{
'title': 'Модули, пакеты и стандартная библиотека',
'order': 1,
'estimated_minutes': 80,
'content': '''
<h2>Что такое модуль?</h2>
<p>Модуль — любой <code>.py</code> файл. Позволяет организовать код по темам и переиспользовать его.</p>

<h2>Способы импорта</h2>
<pre><code>import math                    # импорт модуля
import math as m               # с псевдонимом
from math import sqrt, pi      # конкретные имена
from math import *             # всё (не рекомендуется!)
from math import sqrt as sq    # имя с псевдонимом</code></pre>
''' + warn('<code>from module import *</code> загрязняет пространство имён. Используй только в интерактивном режиме или если явно документировано <code>__all__</code>.') + '''

<h2>Стандартная библиотека Python</h2>
<p>Python «batteries included» — в стандартной библиотеке есть почти всё для повседневной работы:</p>
''' + table(
    ['Модуль','Назначение','Ключевые возможности'],
    [
        ['math','Математика','sqrt, pi, e, sin, log, factorial'],
        ['random','Случайные числа','randint, random, choice, shuffle, sample'],
        ['datetime','Дата и время','date, time, datetime, timedelta'],
        ['os','Операции ОС','getcwd, listdir, mkdir, remove, environ'],
        ['sys','Системные параметры','argv, path, exit, version'],
        ['re','Регулярные выражения','match, search, findall, sub'],
        ['json','JSON формат','load, dump, loads, dumps'],
        ['csv','CSV файлы','reader, writer, DictReader'],
        ['collections','Специальные коллекции','Counter, defaultdict, deque, OrderedDict'],
        ['itertools','Итераторы','chain, product, combinations, permutations'],
        ['functools','Функциональные инструменты','lru_cache, reduce, partial, wraps'],
        ['pathlib','Пути к файлам','Path, glob, mkdir, read_text'],
        ['typing','Аннотации типов','List, Dict, Optional, Union, Tuple'],
        ['unittest','Тестирование','TestCase, assertEqual, assertRaises'],
        ['logging','Логирование','getLogger, debug, info, warning, error'],
        ['time','Время и паузы','time(), sleep(), perf_counter()'],
        ['copy','Копирование','copy, deepcopy'],
        ['hashlib','Хеширование','md5, sha256'],
        ['urllib','HTTP запросы','request, parse'],
        ['socket','Сетевые операции','socket, connect, bind'],
    ]
) + '''

<h2>datetime — работа с датой и временем</h2>
<pre><code>from datetime import date, time, datetime, timedelta

today = date.today()
now = datetime.now()

# Форматирование
print(now.strftime("%d.%m.%Y %H:%M:%S"))   # 14.05.2026 10:30:45
print(now.strftime("%A, %B %d, %Y"))        # Thursday, May 14, 2026

# Парсинг строки
dt = datetime.strptime("14.05.2026", "%d.%m.%Y")

# Арифметика дат
delta = timedelta(days=30)
future = today + delta
print(f"Через 30 дней: {future}")

# Разница дат
deadline = date(2026, 6, 1)
days_left = (deadline - today).days
print(f"До дедлайна: {days_left} дней")</code></pre>

<h2>collections — специальные коллекции</h2>
<pre><code>from collections import Counter, defaultdict, deque, OrderedDict

# Counter
words = "to be or not to be that is the question".split()
freq = Counter(words)
print(freq.most_common(3))   # [('be', 2), ('to', 2), ('or', 1)]

# defaultdict
from collections import defaultdict
graph = defaultdict(list)
graph["A"].append("B")   # нет KeyError, список создаётся автоматически

# deque — двусторонняя очередь
dq = deque([1, 2, 3], maxlen=5)
dq.appendleft(0)    # добавить слева
dq.rotate(1)        # повернуть</code></pre>

<h2>itertools — инструменты для итерации</h2>
<pre><code>import itertools

# Все комбинации
for combo in itertools.combinations([1,2,3,4], 2):
    print(combo)  # (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)

# Все перестановки
list(itertools.permutations("ABC", 2))
# [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]

# Декартово произведение
for pair in itertools.product([0,1], repeat=3):
    print(pair)  # все 8 комбинаций битов

# Цепочка итераторов
chain = list(itertools.chain([1,2], [3,4], [5,6]))
# [1, 2, 3, 4, 5, 6]</code></pre>
''',
'code_example': '''import random
import datetime
from collections import Counter, defaultdict
import itertools

# 1. Симуляция броска кубиков
def dice_simulation(rolls=10000, sides=6):
    results = Counter()
    for _ in range(rolls):
        d1 = random.randint(1, sides)
        d2 = random.randint(1, sides)
        results[d1 + d2] += 1

    print(f"Симуляция {rolls:,} бросков двух кубиков:")
    for total in range(2, 13):
        count = results[total]
        expected = (total - 1 if total <= 7 else 13 - total) / 36
        bar = "█" * (count // (rolls // 100))
        print(f"  {total:2}: {bar:<15} {count:5} ({count/rolls*100:.1f}%,"
              f" теор: {expected*100:.1f}%)")

dice_simulation()

# 2. Аналитика по датам
from datetime import date, timedelta

def weekday_stats(year=2026):
    days = defaultdict(int)
    day_names = ["Пн","Вт","Ср","Чт","Пт","Сб","Вс"]
    d = date(year, 1, 1)
    while d.year == year:
        days[d.weekday()] += 1
        d += timedelta(days=1)

    print(f"\\nДни недели в {year} году:")
    for i, name in enumerate(day_names):
        count = days[i]
        bar = "█" * (count - 50)
        print(f"  {name}: {bar} {count}")

weekday_stats()

# 3. Комбинаторика
subjects = ["Матем", "Физика", "Химия", "История"]
print(f"\\nКомбинации по 2 из {len(subjects)} предметов:")
for combo in itertools.combinations(subjects, 2):
    print(f"  {combo[0]} + {combo[1]}")

print(f"\\nВсего: {len(list(itertools.combinations(subjects, 2)))} комбинаций")
print(f"C({len(subjects)}, 2) = {len(subjects)*(len(subjects)-1)//2}")

# 4. Генератор расписания
def make_schedule(groups, days, pairs_per_day=4):
    schedule = defaultdict(lambda: defaultdict(list))
    subjects = ["Математика", "Физика", "Программирование",
                "История", "Русский", "Химия", "Физкультура"]
    for group in groups:
        for day in days:
            daily = random.sample(subjects, pairs_per_day)
            schedule[group][day] = daily
    return schedule

groups = ["А1", "Б2"]
days = ["Пн", "Вт", "Ср"]
schedule = make_schedule(groups, days, 3)

print("\\nРасписание:")
for group, week in schedule.items():
    print(f"\\n  Группа {group}:")
    for day, subjects in week.items():
        print(f"    {day}: {', '.join(subjects)}")'''
},
]
},

]  # конец MODULES


class Command(BaseCommand):
    help = 'Модули 9-14: исключения, сортировки, рекурсия, файлы, ООП, библиотеки'

    def handle(self, *args, **options):
        for mod_data in MODULES:
            lessons = mod_data.pop('lessons')
            module, _ = TheoryModule.objects.update_or_create(
                title=mod_data['title'], defaults=mod_data)
            for les in lessons:
                TheoryLesson.objects.update_or_create(
                    module=module, title=les['title'], defaults=les)

        from django.db.models import Sum
        total = TheoryLesson.objects.aggregate(t=Sum('estimated_minutes'))['t'] or 0
        self.stdout.write(self.style.SUCCESS(
            f'OK  Модулей: {TheoryModule.objects.count()}, '
            f'Уроков: {TheoryLesson.objects.count()} '
            f'(~{total//60}ч {total%60}мин)'
        ))
