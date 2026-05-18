"""
Заполняет базу тестами по теории программирования.
Запуск: python manage.py seed_quizzes
"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, Quiz, Question, AnswerChoice

QUIZZES = [
    {
        "module_title": "Переменные и типы данных",
        "title": "Тест: Переменные и типы данных",
        "description": "Проверь знания о переменных, типах int, float, str.",
        "pass_score": 70,
        "order": 1,
        "questions": [
            {
                "text": "Что выведет код?\n```\nx = 10\ny = 3\nprint(x // y)\n```",
                "q_type": "single",
                "order": 1,
                "explanation": "Оператор // — целочисленное деление. 10 // 3 = 3 (дробная часть отбрасывается).",
                "choices": [
                    ("3.33", False), ("3", True), ("4", False), ("1", False),
                ],
            },
            {
                "text": "Какой тип имеет переменная x после выполнения: x = input('Введи число: ')?",
                "q_type": "single",
                "order": 2,
                "explanation": "Функция input() всегда возвращает строку (str), даже если пользователь ввёл цифры.",
                "choices": [
                    ("int", False), ("float", False), ("str", True), ("bool", False),
                ],
            },
            {
                "text": "Что выведет код?\n```\nprint(type(3.14))\n```",
                "q_type": "single",
                "order": 3,
                "explanation": "3.14 — число с десятичной точкой, поэтому тип float.",
                "choices": [
                    ("<class 'int'>", False), ("<class 'float'>", True),
                    ("<class 'str'>", False), ("<class 'double'>", False),
                ],
            },
            {
                "text": "Какие из следующих имён переменных являются ПРАВИЛЬНЫМИ?",
                "q_type": "multiple",
                "order": 4,
                "explanation": "Имена не могут начинаться с цифры (1name) и не могут содержать дефис (my-var). for — ключевое слово Python.",
                "choices": [
                    ("student_name", True), ("1name", False),
                    ("myVar", True), ("my-var", False),
                    ("_count", True), ("for", False),
                ],
            },
            {
                "text": "Что произойдёт при выполнении: print(10 / 0)?",
                "q_type": "single",
                "order": 5,
                "explanation": "Деление на ноль вызывает исключение ZeroDivisionError.",
                "choices": [
                    ("Выведет 0", False), ("Выведет infinity", False),
                    ("ZeroDivisionError", True), ("Выведет None", False),
                ],
            },
            {
                "text": "Что выведет код?\n```\nname = 'Анна'\nage = 20\nprint(f'Мне {age} лет')\n```",
                "q_type": "single",
                "order": 6,
                "explanation": "f-строка подставляет значение переменной age в строку.",
                "choices": [
                    ("Мне age лет", False), ("Мне {age} лет", False),
                    ("Мне 20 лет", True), ("Ошибка", False),
                ],
            },
            {
                "text": "Что выведет: print(2 ** 8)?",
                "q_type": "single",
                "order": 7,
                "explanation": "** — оператор возведения в степень. 2^8 = 256.",
                "choices": [
                    ("16", False), ("256", True), ("64", False), ("512", False),
                ],
            },
        ],
    },
    {
        "module_title": "Условные операторы",
        "title": "Тест: Условные операторы",
        "description": "Проверь знания об операторах if, elif, else и логических операторах.",
        "pass_score": 70,
        "order": 2,
        "questions": [
            {
                "text": "Что выведет код?\n```\nx = 15\nif x > 10:\n    print('A')\nelif x > 5:\n    print('B')\nelse:\n    print('C')\n```",
                "q_type": "single",
                "order": 1,
                "explanation": "x=15 > 10, поэтому выполняется первая ветка — выводится 'A'. Остальные ветки не проверяются.",
                "choices": [
                    ("A", True), ("B", False), ("C", False), ("A и B", False),
                ],
            },
            {
                "text": "Какой оператор проверяет, что ОБА условия истинны одновременно?",
                "q_type": "single",
                "order": 2,
                "explanation": "Логический оператор and возвращает True только если оба операнда True.",
                "choices": [
                    ("or", False), ("and", True), ("not", False), ("xor", False),
                ],
            },
            {
                "text": "Что выведет код?\n```\na = 5\nresult = 'чётное' if a % 2 == 0 else 'нечётное'\nprint(result)\n```",
                "q_type": "single",
                "order": 3,
                "explanation": "5 % 2 = 1, не равно 0, поэтому выполняется ветка else — 'нечётное'.",
                "choices": [
                    ("чётное", False), ("нечётное", True),
                    ("True", False), ("False", False),
                ],
            },
            {
                "text": "Выбери все ИСТИННЫЕ утверждения о Python-отступах:",
                "q_type": "multiple",
                "order": 4,
                "explanation": "Python использует отступы для обозначения блоков кода. Стандарт — 4 пробела. Нельзя смешивать пробелы и табуляцию.",
                "choices": [
                    ("Отступы обязательны", True),
                    ("Можно использовать любое количество пробелов", False),
                    ("Стандарт — 4 пробела", True),
                    ("Нельзя смешивать пробелы и табуляцию", True),
                    ("Отступы только для красоты", False),
                ],
            },
            {
                "text": "Что вернёт выражение: not (5 > 3)?",
                "q_type": "single",
                "order": 5,
                "explanation": "5 > 3 = True, not True = False.",
                "choices": [
                    ("True", False), ("False", True),
                    ("None", False), ("Ошибка", False),
                ],
            },
        ],
    },
    {
        "module_title": "Циклы",
        "title": "Тест: Циклы",
        "description": "Проверь знания о циклах for и while, операторах break и continue.",
        "pass_score": 70,
        "order": 3,
        "questions": [
            {
                "text": "Сколько раз выполнится цикл?\n```\nfor i in range(2, 10, 3):\n    print(i)\n```",
                "q_type": "single",
                "order": 1,
                "explanation": "range(2, 10, 3) генерирует числа: 2, 5, 8 — всего 3 числа.",
                "choices": [
                    ("2", False), ("3", True), ("4", False), ("8", False),
                ],
            },
            {
                "text": "Что делает оператор break внутри цикла?",
                "q_type": "single",
                "order": 2,
                "explanation": "break немедленно прерывает выполнение цикла и передаёт управление следующей строке после цикла.",
                "choices": [
                    ("Пропускает текущую итерацию", False),
                    ("Немедленно завершает цикл", True),
                    ("Перезапускает цикл с начала", False),
                    ("Выходит из программы", False),
                ],
            },
            {
                "text": "Что выведет код?\n```\ni = 0\nwhile i < 3:\n    i += 1\n    if i == 2:\n        continue\n    print(i)\n```",
                "q_type": "single",
                "order": 3,
                "explanation": "continue пропускает print для i=2. Выводятся 1 и 3.",
                "choices": [
                    ("1 2 3", False), ("1 3", True), ("2", False), ("1 2", False),
                ],
            },
            {
                "text": "Какой цикл лучше использовать, когда заранее неизвестно количество итераций?",
                "q_type": "single",
                "order": 4,
                "explanation": "Цикл while продолжается пока условие истинно — подходит для неизвестного числа итераций. for лучше для перебора последовательностей.",
                "choices": [
                    ("for", False), ("while", True),
                    ("do-while", False), ("repeat-until", False),
                ],
            },
            {
                "text": "Что выведет код?\n```\ntotal = 0\nfor i in range(1, 5):\n    total += i\nprint(total)\n```",
                "q_type": "single",
                "order": 5,
                "explanation": "range(1, 5) = [1, 2, 3, 4]. Сумма: 1+2+3+4 = 10.",
                "choices": [
                    ("15", False), ("10", True), ("14", False), ("5", False),
                ],
            },
        ],
    },
    {
        "module_title": "Функции",
        "title": "Тест: Функции",
        "description": "Проверь знания об определении и вызове функций, параметрах и return.",
        "pass_score": 70,
        "order": 4,
        "questions": [
            {
                "text": "Что выведет код?\n```\ndef add(a, b=5):\n    return a + b\n\nprint(add(3))\n```",
                "q_type": "single",
                "order": 1,
                "explanation": "b имеет значение по умолчанию 5. add(3) вызывает функцию с a=3, b=5. Результат: 8.",
                "choices": [
                    ("3", False), ("5", False), ("8", True), ("Ошибка", False),
                ],
            },
            {
                "text": "Что вернёт функция, если в ней нет оператора return?",
                "q_type": "single",
                "order": 2,
                "explanation": "Функция без return возвращает None.",
                "choices": [
                    ("0", False), ("None", True), ("False", False), ("Ошибка", False),
                ],
            },
            {
                "text": "Что выведет код?\n```\ndef swap(a, b):\n    return b, a\n\nx, y = swap(1, 2)\nprint(x, y)\n```",
                "q_type": "single",
                "order": 3,
                "explanation": "Функция возвращает два значения в обратном порядке. x=2, y=1.",
                "choices": [
                    ("1 2", False), ("2 1", True), ("(2, 1)", False), ("Ошибка", False),
                ],
            },
            {
                "text": "Что такое рекурсия?",
                "q_type": "single",
                "order": 4,
                "explanation": "Рекурсия — функция, которая вызывает сама себя. Обязательно должен быть базовый случай для остановки.",
                "choices": [
                    ("Вызов нескольких функций одновременно", False),
                    ("Функция, вызывающая сама себя", True),
                    ("Функция без параметров", False),
                    ("Вложенные функции", False),
                ],
            },
        ],
    },
    {
        "module_title": "Алгоритмы сортировки",
        "title": "Тест: Алгоритмы сортировки",
        "description": "Проверь знания о пузырьковой сортировке и сортировке выбором.",
        "pass_score": 60,
        "order": 5,
        "questions": [
            {
                "text": "Какова сложность пузырьковой сортировки в худшем случае?",
                "q_type": "single",
                "order": 1,
                "explanation": "Пузырьковая сортировка делает n*(n-1)/2 сравнений, что соответствует O(n²).",
                "choices": [
                    ("O(n)", False), ("O(n log n)", False),
                    ("O(n²)", True), ("O(n³)", False),
                ],
            },
            {
                "text": "Что произойдёт с массивом [5, 3, 8, 1] после одного прохода пузырьковой сортировки?",
                "q_type": "single",
                "order": 2,
                "explanation": "За один проход: (5,3)→(3,5,8,1), (5,8)→нет обмена, (8,1)→(3,5,1,8). Наибольший 8 оказывается в конце.",
                "choices": [
                    ("[1, 3, 5, 8]", False), ("[3, 5, 1, 8]", True),
                    ("[3, 5, 8, 1]", False), ("[1, 5, 3, 8]", False),
                ],
            },
            {
                "text": "В каком случае пузырьковая сортировка работает быстрее всего?",
                "q_type": "single",
                "order": 3,
                "explanation": "Если массив уже отсортирован, оптимизированная пузырьковая сортировка завершится за один проход — O(n).",
                "choices": [
                    ("Массив отсортирован в обратном порядке", False),
                    ("Массив уже отсортирован", True),
                    ("Массив случайный", False),
                    ("Все элементы одинаковые", False),
                ],
            },
            {
                "text": "Выбери ВЕРНЫЕ утверждения о сортировке вставками:",
                "q_type": "multiple",
                "order": 4,
                "explanation": "Сортировка вставками эффективна для почти отсортированных данных и небольших массивов. Сложность в худшем случае O(n²).",
                "choices": [
                    ("Эффективна для почти отсортированных данных", True),
                    ("Сложность O(n log n) в худшем случае", False),
                    ("Сложность O(n²) в худшем случае", True),
                    ("Хороша для небольших наборов данных", True),
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Заполняет базу данных тестами по теории'

    def handle(self, *args, **options):
        created_q = 0
        created_quiz = 0

        for quiz_data in QUIZZES:
            module_title = quiz_data.pop('module_title')
            questions_data = quiz_data.pop('questions')

            module = TheoryModule.objects.filter(title=module_title).first()

            quiz, created = Quiz.objects.get_or_create(
                title=quiz_data['title'],
                defaults={'title': quiz_data['title'], 'description': quiz_data.get('description',''), 'pass_score': quiz_data.get('pass_score',70), 'order': quiz_data.get('order',0), 'module': module},
            )
            if created:
                created_quiz += 1
            elif module:
                quiz.module = module
                quiz.save()

            for q_data in questions_data:
                choices = q_data.pop('choices')
                question, q_created = Question.objects.get_or_create(
                    quiz=quiz,
                    text=q_data['text'],
                    defaults=q_data,
                )
                if q_created:
                    created_q += 1
                    for i, (text, is_correct) in enumerate(choices):
                        AnswerChoice.objects.create(
                            question=question,
                            text=text,
                            is_correct=is_correct,
                            order=i,
                        )

        self.stdout.write(self.style.SUCCESS(
            f'✓ Тестов создано: {created_quiz}, вопросов: {created_q}'
        ))
