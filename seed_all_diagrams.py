"""
Добавляет SVG-диаграммы во все уроки теории + исправляет старый формат.
Запуск: python seed_all_diagrams.py
"""
import os, sys, re, django

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algorithm_site.settings')
django.setup()

from works.models import TheoryLesson

MARKER = '<!-- VISUAL_OK -->'

# ═══════════════════════════════════════════════════════════
#  SVG helpers
# ═══════════════════════════════════════════════════════════

_c = 0
def _id():
    global _c; _c += 1; return f'm{_c}'

def wrap(inner, vw, vh):
    return (
        '<div class="fc-diagram">'
        f'<svg viewBox="0 0 {vw} {vh}" preserveAspectRatio="xMidYMid meet" '
        f'xmlns="http://www.w3.org/2000/svg" overflow="visible">'
        f'{inner}'
        '</svg></div>'
    )

def _mk(color):
    i = _id()
    return i, (f'<defs><marker id="{i}" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">'
               f'<polygon points="0 0,9 3.5,0 7" fill="{color}"/></marker></defs>')

def arr(x1, y1, x2, y2, color='#475569', w=1.8):
    i, d = _mk(color)
    return f'{d}<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" marker-end="url(#{i})"/>'

def parr(d_path, color='#475569', w=1.8):
    i, d = _mk(color)
    return f'{d}<path d="{d_path}" fill="none" stroke="{color}" stroke-width="{w}" marker-end="url(#{i})"/>'

def rct(cx, cy, bw, bh, fill, stroke='#94a3b8', rx=7, text='', fs=12, bold=False, tc='#1e293b'):
    fw = 'bold' if bold else 'normal'
    lines = text.split('\n') if text else []
    lh = fs + 3
    ty = cy - (len(lines)-1)*lh/2
    t = ''.join(
        f'<text x="{cx}" y="{ty+i*lh}" text-anchor="middle" dominant-baseline="central" '
        f'font-size="{fs}" font-weight="{fw}" fill="{tc}" font-family="monospace">{ln}</text>'
        for i, ln in enumerate(lines)
    )
    return f'<rect x="{cx-bw//2}" y="{cy-bh//2}" width="{bw}" height="{bh}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>{t}'

def dmd(cx, cy, hw, hh, fill, stroke='#94a3b8', text='', fs=11, tc='#1e293b'):
    pts = f'{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}'
    lines = text.split('\n') if text else []
    lh = fs + 3
    ty = cy - (len(lines)-1)*lh/2
    t = ''.join(
        f'<text x="{cx}" y="{ty+i*lh}" text-anchor="middle" dominant-baseline="central" '
        f'font-size="{fs}" fill="{tc}" font-family="monospace">{ln}</text>'
        for i, ln in enumerate(lines)
    )
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>{t}'

def lbl(x, y, text, fill='#64748b', fs=11, anc='start'):
    return f'<text x="{x}" y="{y}" font-size="{fs}" fill="{fill}" font-family="sans-serif" text-anchor="{anc}">{text}</text>'

def ttl(x, y, text, fill='#1e293b'):
    return lbl(x, y, text, fill, 13, 'middle') .replace('font-family="sans-serif"', 'font-family="sans-serif" font-weight="bold"')

def vline(x, y1, y2, color='#e2e8f0', dash='5,4'):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="1.5" stroke-dasharray="{dash}"/>'

def hline(x1, x2, y, color='#e2e8f0', w=1):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{w}"/>'

def cbx(x, y, w, h, lines):
    """Тёмный блок с кодом: lines = [(text, color_index)]"""
    clrs = ['#cdd6f4','#a6e3a1','#89dceb','#f9e2af','#cba6f7','#fab387','#f38ba8']
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#1e1e2e" stroke="#44475a" stroke-width="1"/>'
    for i, (txt, ci) in enumerate(lines):
        s += f'<text x="{x+12}" y="{y+18+i*16}" font-size="11" fill="{clrs[ci%7]}" font-family="monospace">{txt}</text>'
    return s

def tbl(x, y, headers, rows, col_w, row_h=28, hdr_fill='#f1f5f9', hdr_tc='#1e293b'):
    """SVG-таблица."""
    total_w = sum(col_w)
    s = ''
    # Header
    cx = x
    s += f'<rect x="{x}" y="{y}" width="{total_w}" height="{row_h}" rx="6" fill="{hdr_fill}" stroke="#e2e8f0" stroke-width="1"/>'
    for i, (h_txt, cw) in enumerate(zip(headers, col_w)):
        s += lbl(cx + cw//2, y + row_h//2 + 4, h_txt, hdr_tc, 11, 'middle').replace('font-family="sans-serif"', 'font-family="sans-serif" font-weight="bold"')
        if i < len(col_w)-1:
            s += vline(cx+cw, y, y+row_h, '#e2e8f0', '')
        cx += cw
    # Rows
    fills = ['#ffffff', '#f8fafc']
    for ri, row in enumerate(rows):
        ry = y + (ri+1)*row_h
        fill = fills[ri%2]
        s += f'<rect x="{x}" y="{ry}" width="{total_w}" height="{row_h}" fill="{fill}" stroke="#e2e8f0" stroke-width="1"/>'
        cx = x
        for ci, (cell, cw) in enumerate(zip(row, col_w)):
            cell_fill = cell[1] if isinstance(cell, tuple) else '#1e293b'
            cell_text = cell[0] if isinstance(cell, tuple) else cell
            s += lbl(cx + cw//2, ry + row_h//2 + 4, cell_text, cell_fill, 10, 'middle')
            if ci < len(col_w)-1:
                s += vline(cx+cw, ry, ry+row_h, '#e2e8f0', '')
            cx += cw
    # Border
    total_h = (len(rows)+1)*row_h
    s += f'<rect x="{x}" y="{y}" width="{total_w}" height="{total_h}" rx="6" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>'
    return s


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 1: Python execution pipeline (MOD1-L2)
# ═══════════════════════════════════════════════════════════
def diag_ide():
    VW, VH = 600, 210
    s = ''
    steps = [
        ('script.py', '#dbeafe', '#3b82f6', '#1e40af', 'Исходный\nкод'),
        ('python\nкоманда', '#ede9fe', '#8b5cf6', '#4c1d95', 'Запуск\nинтерпретатора'),
        ('bytecode\n(.pyc)', '#fef9c3', '#d97706', '#78350f', 'Компиляция\nв байткод'),
        ('CPython\nVM', '#dcfce7', '#16a34a', '#14532d', 'Виртуальная\nмашина'),
        ('результат', '#f0fdf4', '#22c55e', '#14532d', 'Вывод /\nрезультат'),
    ]
    box_w, box_h = 88, 52
    gap = 24
    total = len(steps) * box_w + (len(steps)-1) * gap
    x0 = (VW - total) // 2
    cy = 85

    for i, (title, fill, stroke, tc, desc) in enumerate(steps):
        cx = x0 + i*(box_w + gap) + box_w//2
        s += rct(cx, cy, box_w, box_h, fill, stroke, 8, title, 11, True, tc)
        s += lbl(cx, cy + box_h//2 + 22, desc, '#64748b', 10, 'middle')
        if i < len(steps)-1:
            ax = cx + box_w//2 + 2
            s += arr(ax, cy, ax + gap - 4, cy, '#94a3b8')

    s += ttl(VW//2, 22, 'Как Python выполняет программу')
    s += lbl(VW//2, VH-8, 'Каждый запуск проходит этот путь. Байткод кэшируется в __pycache__/', '#94a3b8', 10, 'middle')
    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 2: Numeric types (MOD2-L2)
# ═══════════════════════════════════════════════════════════
def diag_numbers():
    VW, VH = 640, 280
    s = ''
    s += vline(320, 15, VH-10)
    s += ttl(160, 22, 'Числовые типы Python')
    s += ttl(480, 22, 'Конвертация типов')

    # Иерархия (левая)
    root_x, root_y = 155, 65
    s += rct(root_x, root_y, 100, 32, '#e0f2fe', '#0284c7', 8, 'числа (число)', 11, True, '#0369a1')
    types = [
        (75, 140, 'int', '#dbeafe', '#3b82f6', '#1e40af', '-2, 0, 42, 10**9'),
        (155, 140, 'float', '#dcfce7', '#16a34a', '#14532d', '3.14, -0.5, 1e10'),
        (235, 140, 'complex', '#fef9c3', '#d97706', '#78350f', '2+3j, 1j'),
    ]
    for cx, cy, name, fill, stroke, tc, example in types:
        s += arr(root_x, root_y+16, cx, cy-16, '#94a3b8')
        s += rct(cx, cy, 70, 28, fill, stroke, 6, name, 12, True, tc)
        s += lbl(cx, cy+28, example, '#64748b', 9, 'middle')

    # Особенности int
    s += lbl(75, 185, 'Точность', '#475569', 9, 'middle')
    s += lbl(75, 196, 'не ограничена', '#475569', 9, 'middle')

    # Конвертации (правая)
    convs = [
        ('int(3.7)', '→ 3', '#dbeafe', '#1e40af'),
        ('int("42")', '→ 42', '#dbeafe', '#1e40af'),
        ('float(5)', '→ 5.0', '#dcfce7', '#14532d'),
        ('float("3.14")', '→ 3.14', '#dcfce7', '#14532d'),
        ('int(True)', '→ 1', '#fef9c3', '#78350f'),
        ('complex(3,4)', '→ (3+4j)', '#ede9fe', '#4c1d95'),
        ('round(3.756, 2)', '→ 3.76', '#f0fdf4', '#166534'),
    ]
    for i, (expr, result, fill, tc) in enumerate(convs):
        y = 42 + i*31
        s += rct(410, y, 120, 24, fill, '#cbd5e1', 5, expr, 11, False, tc)
        s += lbl(478, y+5, result, tc, 11, 'middle')
        s += rct(565, y, 80, 24, fill, '#94a3b8', 5, result, 11, True, tc)

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 3: String indexing (MOD2-L3)
# ═══════════════════════════════════════════════════════════
def diag_strings():
    VW, VH = 620, 300
    s = ''
    s += ttl(VW//2, 22, 'Строки Python: индексы и срезы')

    word = 'Python'
    cw = 62
    x0 = (VW - len(word)*cw) // 2
    cy_char = 85

    for i, ch in enumerate(word):
        cx = x0 + i*cw + cw//2
        # Прямой индекс
        s += lbl(cx, 45, str(i), '#3b82f6', 11, 'middle')
        s += arr(cx, 50, cx, cy_char-16, '#3b82f6', 1.2)
        # Символ
        s += rct(cx, cy_char, cw-4, 32, '#f1f5f9', '#94a3b8', 4, ch, 18, True, '#0f172a')
        # Обратный индекс
        s += arr(cx, cy_char+16, cx, cy_char+36, '#dc2626', 1.2)
        s += lbl(cx, cy_char+50, str(i - len(word)), '#dc2626', 11, 'middle')

    s += lbl(x0 - 35, 45, 's[i]:', '#3b82f6', 11, 'start')
    s += lbl(x0 - 35, cy_char+50, 's[-i]:', '#dc2626', 11, 'start')

    # Срезы
    slice_y = 155
    s += hline(20, VW-20, slice_y, '#e2e8f0', 1)
    s += ttl(VW//2, slice_y+18, 'Срезы s[start:stop:step]')

    slices = [
        ("s[1:4]", "yth", '#dbeafe', [1,2,3]),
        ("s[::2]", "Pto", '#dcfce7', [0,2,4]),
        ("s[::-1]", "nohtyP", '#fef9c3', list(range(5,-1,-1))),
        ("s[2:]", "thon", '#ede9fe', [2,3,4,5]),
    ]
    for i, (expr, result, fill, _) in enumerate(slices):
        col = i % 2
        row = i // 2
        bx = 40 + col * 300
        by = slice_y + 32 + row * 40
        s += rct(bx + 55, by, 100, 26, fill, '#94a3b8', 5, expr, 12, True, '#1e293b')
        s += lbl(bx+105+8, by+2, '= ', '#94a3b8', 12, 'start')
        s += rct(bx + 200, by, 90, 26, '#f8fafc', '#94a3b8', 5, f'"{result}"', 12, False, '#16a34a')

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 4: Boolean logic (MOD2-L4)
# ═══════════════════════════════════════════════════════════
def diag_booleans():
    VW, VH = 640, 300
    s = ''
    s += vline(330, 15, VH-10)
    s += ttl(165, 22, 'Таблицы истинности')
    s += ttl(485, 22, 'Truthy и Falsy значения')

    # AND / OR / NOT tables
    tables = [
        ('and', ['A and B'], [('T','T','→ True','#16a34a'), ('T','F','→ False','#dc2626'), ('F','T','→ False','#dc2626'), ('F','F','→ False','#dc2626')]),
        ('or',  ['A or B'],  [('T','T','→ True','#16a34a'), ('T','F','→ True','#16a34a'), ('F','T','→ True','#16a34a'), ('F','F','→ False','#dc2626')]),
    ]
    tx_start = 20
    for ti, (op, header, rows) in enumerate(tables):
        ty = 38 + ti * 105
        s += lbl(tx_start + 55, ty, header[0], '#1e293b', 12, 'middle')
        for ri, (a, b, res, rc) in enumerate(rows):
            ry = ty + 18 + ri*18
            s += lbl(tx_start + 10, ry+5, a, '#3b82f6', 11)
            s += lbl(tx_start + 35, ry+5, b, '#8b5cf6', 11)
            s += lbl(tx_start + 65, ry+5, res, rc, 11)

    # not table
    s += lbl(tx_start+45, 258, 'not A:', '#1e293b', 12)
    s += lbl(tx_start+105, 258, 'True→False, False→True', '#64748b', 10)

    # Truthy / Falsy
    s += lbl(340, 42, 'Falsy (==False):', '#dc2626', 12)
    falsy = ['0, 0.0, 0j', '""  \'\'  """"""', '[]  ()  {}', 'set()  None', 'False']
    for i, v in enumerate(falsy):
        s += rct(480, 58 + i*26, 200, 22, '#fee2e2', '#fca5a5', 4, v, 11, False, '#7f1d1d')

    s += lbl(340, 200, 'Truthy (==True):', '#16a34a', 12)
    truthy = ['любое ненулевое число', 'непустая строка', 'непустой список/dict', 'True и почти всё остальное']
    for i, v in enumerate(truthy):
        s += rct(480, 215 + i*20, 210, 17, '#f0fdf4', '#86efac', 3, v, 10, False, '#14532d')

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 5: Python gotchas (MOD2-L99)
# ═══════════════════════════════════════════════════════════
def diag_gotchas():
    VW, VH = 640, 300
    s = ''
    s += ttl(VW//2, 18, 'Ловушки Python — типичные ошибки')

    gotchas = [
        ('Изменяемый\nаргумент по умолчанию',
         'def f(lst=[]):  # ⚠️\n    lst.append(1)',
         'def f(lst=None):  # ✓\n    if lst is None: lst=[]'),
        ('== vs is',
         'a=1000; b=1000\na is b  # False !\n',
         'a=42; b=42\na is b  # True (кэш)\nИспользуй == для значений'),
        ('Позднее связывание\nв lambda',
         'fns=[lambda: i for i in range(3)]\nfns[0]()  # → 2 ⚠️',
         'fns=[lambda i=i: i for i in range(3)]\nfns[0]()  # → 0 ✓'),
        ('Копирование списка',
         'b = a    # та же ссылка ⚠️\nb.append(1) → a тоже меняется',
         'b = a[:]  # или list(a)  ✓\nimport copy; b = copy.deepcopy(a)'),
    ]

    col_w = 155
    for i, (title, wrong, right) in enumerate(gotchas):
        col = i % 2
        row = i // 2
        bx = 14 + col * 318
        by = 35 + row * 128
        s += lbl(bx + col_w, by, title, '#1e293b', 10, 'middle')
        s += cbx(bx, by+14, col_w-4, int(wrong.count('\n')+1)*16+10,
                 [(ln, 6 if '⚠️' in ln or 'False !' in ln else 0) for ln in wrong.split('\n')])
        s += arr(bx + col_w, by + 30, bx + col_w + 12, by + 30, '#16a34a')
        s += cbx(bx + col_w + 18, by+14, col_w,  int(right.count('\n')+1)*16+10,
                 [(ln, 1) for ln in right.split('\n')])

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 6: List comprehension anatomy (MOD5-L2)
# ═══════════════════════════════════════════════════════════
def diag_comprehension():
    VW, VH = 640, 290
    s = ''
    s += ttl(VW//2, 20, 'Генератор списков: анатомия выражения')

    # Main expression
    parts = [
        ('[', None, None, None),
        ('выражение', 120, '#dbeafe', '#1e40af'),
        ('  for  ', None, None, None),
        ('переменная', 105, '#dcfce7', '#14532d'),
        ('  in  ', None, None, None),
        ('последовательность', 160, '#fef9c3', '#78350f'),
        ('  if  ', None, None, None),
        ('условие', 80, '#ede9fe', '#4c1d95'),
        (']', None, None, None),
    ]

    x = 18
    y = 65
    h_box = 36
    seg_data = []
    for text, bw, fill, tc in parts:
        if fill:
            s += rct(x + bw//2, y, bw, h_box, fill, '#94a3b8', 6, text, 12, True, tc)
            seg_data.append((x + bw//2, y, bw, text, tc))
            x += bw
        else:
            tw = len(text) * 8
            s += lbl(x + tw//2, y + h_box//2 + 4, text, '#64748b', 13, 'middle')
            x += tw

    # Стрелки с метками вниз
    arrow_data = [
        (seg_data[0][0], 'Что кладём\nв список', '#1e40af'),
        (seg_data[1][0], 'Имя\nэлемента', '#14532d'),
        (seg_data[2][0], 'Откуда берём\nэлементы', '#78350f'),
        (seg_data[3][0], 'Фильтр\n(опционально)', '#4c1d95'),
    ]
    for ax, label_text, tc in arrow_data:
        ay_start = y + h_box//2
        ay_end = y + h_box//2 + 35
        s += arr(ax, ay_start, ax, ay_end, tc, 1.5)
        for li, ln in enumerate(label_text.split('\n')):
            s += lbl(ax, ay_end + 14 + li*14, ln, tc, 10, 'middle')

    # Example
    ex_y = 195
    s += hline(20, VW-20, ex_y-8, '#e2e8f0')
    s += ttl(VW//2, ex_y+8, 'Примеры')
    examples = [
        ('[x**2 for x in range(6)]', '→  [0, 1, 4, 9, 16, 25]'),
        ('[x for x in range(10) if x%2==0]', '→  [0, 2, 4, 6, 8]'),
        ('[s.upper() for s in ["a","b","c"]]', '→  ["A", "B", "C"]'),
    ]
    for i, (expr, result) in enumerate(examples):
        ey = ex_y + 26 + i*24
        s += cbx(20, ey, 320, 20, [(expr, 2)])
        s += lbl(350, ey+13, result, '#16a34a', 11)

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 7: Tuples & Sets (MOD7-L2)
# ═══════════════════════════════════════════════════════════
def diag_tuples_sets():
    VW, VH = 640, 310
    s = ''
    s += vline(320, 15, VH-10)
    s += ttl(160, 20, 'Tuple vs List')
    s += ttl(480, 20, 'Операции с множествами')

    # Tuple vs List table
    headers = ['', 'tuple', 'list']
    rows = [
        ('Изменяемый',    ('Нет', '#dc2626'), ('Да', '#16a34a')),
        ('Синтаксис',     ('(a, b, c)', '#1e40af'), ('[a, b, c]', '#1e40af')),
        ('Хешируемый',   ('Да ✓', '#16a34a'), ('Нет ✗', '#dc2626')),
        ('Ключ dict',    ('Да ✓', '#16a34a'), ('Нет ✗', '#dc2626')),
        ('Быстрее',      ('✓ итерация', '#16a34a'), ('✓ изменение', '#16a34a')),
        ('Применение',   ('возврат >1', '#64748b'), ('коллекция', '#64748b')),
    ]
    col_w = [95, 80, 80]
    s += tbl(15, 35, ['Свойство', 'tuple', 'list'], rows, col_w)

    # Venn diagram for sets
    cx1, cx2, cy = 415, 505, 165
    r = 70
    # Two overlapping circles
    s += f'<circle cx="{cx1}" cy="{cy}" r="{r}" fill="#dbeafe" stroke="#3b82f6" stroke-width="2" opacity="0.7"/>'
    s += f'<circle cx="{cx2}" cy="{cy}" r="{r}" fill="#dcfce7" stroke="#16a34a" stroke-width="2" opacity="0.7"/>'
    s += ttl(cx1-25, cy, 'A', '#1e40af')
    s += ttl(cx2+25, cy, 'B', '#14532d')
    s += ttl((cx1+cx2)//2, cy, 'A∩B', '#92400e')

    # Labels
    ops = [
        (cx1-65, cy+95, 'A | B', 'A ∪ B — объединение', '#3b82f6'),
        (cx1-65, cy+115, 'A & B', 'A ∩ B — пересечение', '#d97706'),
        (cx1-65, cy+135, 'A - B', 'A \\ B — разность', '#dc2626'),
        (cx1-65, cy+155, 'A ^ B', 'A △ B — симм. разность', '#8b5cf6'),
    ]
    for bx, by, code, desc, tc in ops:
        s += cbx(bx, by-13, 55, 16, [(code, 2)])
        s += lbl(bx+62, by, desc, tc, 10)

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 8: Quicksort + Mergesort (MOD10-L2)
# ═══════════════════════════════════════════════════════════
def diag_quicksort():
    VW, VH = 640, 320
    s = ''
    s += vline(320, 15, VH-10)
    s += ttl(160, 18, 'Быстрая сортировка (Quicksort)')
    s += ttl(480, 18, 'Сортировка слиянием (Mergesort)')

    # Quicksort visualization
    arr_vals = [5, 3, 8, 1, 9, 2, 7]
    bw, bh = 34, 28
    ay = 50
    x0 = 15
    # Original array
    s += lbl(x0, ay-4, 'Массив:', '#64748b', 10)
    for i, v in enumerate(arr_vals):
        cx = x0 + i*(bw+2) + bw//2
        fill = '#fef9c3' if i == 0 else '#f1f5f9'
        stroke = '#d97706' if i == 0 else '#94a3b8'
        s += rct(cx, ay+bh//2, bw, bh, fill, stroke, 4, str(v), 12, i==0)
    s += lbl(x0 + len(arr_vals)*(bw+2) + 4, ay+bh//2+4, '← pivot=5', '#d97706', 10)

    # After partition
    py = ay + 55
    s += arr(160, ay+bh+2, 160, py-4, '#475569')
    s += lbl(x0, py-4, 'Разбиение:', '#64748b', 10)
    left_v = [3, 1, 2]
    right_v = [8, 9, 7]
    for i, v in enumerate(left_v):
        cx = x0 + i*(bw+2) + bw//2
        s += rct(cx, py+bh//2, bw, bh, '#dbeafe', '#3b82f6', 4, str(v), 12)
    pcx = x0 + 3*(bw+2) + bw//2
    s += rct(pcx, py+bh//2, bw, bh, '#fef9c3', '#d97706', 4, '5', 13, True, '#78350f')
    s += lbl(pcx, py+bh//2+20, '↑ pivot', '#d97706', 9, 'middle')
    for i, v in enumerate(right_v):
        cx = pcx + (i+1)*(bw+2) + bw//2
        s += rct(cx, py+bh//2, bw, bh, '#dcfce7', '#16a34a', 4, str(v), 12)

    # Recurse labels
    ry = py + 65
    s += arr(75, py+bh+2, 75, ry-4, '#3b82f6')
    s += arr(240, py+bh+2, 240, ry-4, '#16a34a')
    s += lbl(x0, ry, '[1, 2, 3]', '#3b82f6', 11)
    s += lbl(pcx, ry, '5', '#d97706', 13)
    s += lbl(pcx+(bw+2), ry, '[7, 8, 9]', '#16a34a', 11)
    s += lbl(x0, ry+16, '→ [1,2,3,5,7,8,9]', '#64748b', 10)
    s += lbl(x0, ry+30, 'O(n log n) среднее, O(n²) худшее', '#94a3b8', 9)

    # Mergesort tree (right side)
    mx0 = 330
    ms_arr = [4, 7, 2, 6, 1, 5]
    level_y = [35, 85, 135, 185]
    # Level 0: full array
    for i, v in enumerate(ms_arr):
        cx = mx0 + i*(bw+2) + bw//2
        s += rct(cx, level_y[0]+bh//2, bw, bh, '#ede9fe', '#8b5cf6', 4, str(v), 12)

    # Level 1: split in 2
    s += arr(mx0+len(ms_arr)//2*(bw+2)-bw, level_y[0]+bh+4, mx0+45, level_y[1]-4, '#8b5cf6')
    s += arr(mx0+len(ms_arr)//2*(bw+2)+bw, level_y[0]+bh+4, mx0+155, level_y[1]-4, '#8b5cf6')
    for i, v in enumerate([4,7,2]):
        s += rct(mx0 + i*(bw+2) + bw//2, level_y[1]+bh//2, bw, bh, '#fef9c3', '#d97706', 4, str(v), 11)
    for i, v in enumerate([6,1,5]):
        s += rct(mx0 + 110 + i*(bw+2) + bw//2, level_y[1]+bh//2, bw, bh, '#dcfce7', '#16a34a', 4, str(v), 11)

    # Merged result
    s += arr(mx0+90, level_y[1]+bh+4, mx0+90, level_y[2]-4, '#475569')
    for i, v in enumerate([1,2,4,5,6,7]):
        s += rct(mx0 + i*(bw+2) + bw//2, level_y[2]+bh//2, bw, bh, '#dbeafe', '#3b82f6', 4, str(v), 12, True)
    s += lbl(mx0, level_y[2]+bh+10, 'O(n log n) всегда, O(n) память', '#94a3b8', 9)

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 9: Sort Big-O table (MOD10-L99)
# ═══════════════════════════════════════════════════════════
def diag_sort_bigo():
    VW, VH = 640, 250
    s = ''
    s += ttl(VW//2, 18, 'Сравнение алгоритмов сортировки')

    G = '#16a34a'; Y = '#d97706'; R = '#dc2626'; B = '#3b82f6'; P = '#8b5cf6'
    headers = ['Алгоритм', 'Лучшее', 'Среднее', 'Худшее', 'Память', 'Устойч.']
    rows = [
        ('Пузырьк.', ('O(n)', G), ('O(n²)', R), ('O(n²)', R), ('O(1)', G), ('Да', G)),
        ('Вставка',  ('O(n)', G), ('O(n²)', Y), ('O(n²)', R), ('O(1)', G), ('Да', G)),
        ('Выборка',  ('O(n²)', R),('O(n²)', R), ('O(n²)', R), ('O(1)', G), ('Нет', R)),
        ('Слияние',  ('O(n log n)', G),('O(n log n)', G),('O(n log n)', G),('O(n)', Y),('Да', G)),
        ('Быстрая',  ('O(n log n)', G),('O(n log n)', G),('O(n²)', R),('O(log n)', G),('Нет', R)),
        ('Timsort',  ('O(n)', G), ('O(n log n)', G),('O(n log n)', G),('O(n)', Y),('Да', G)),
    ]
    col_w = [80, 90, 100, 90, 85, 70]
    s += tbl(10, 30, headers, rows, col_w)

    s += lbl(VW//2, VH-8, 'Timsort — алгоритм sorted() и list.sort() в CPython', '#94a3b8', 10, 'middle')
    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 10: File I/O (MOD12-L1)
# ═══════════════════════════════════════════════════════════
def diag_files():
    VW, VH = 640, 300
    s = ''
    s += vline(330, 15, VH-10)
    s += ttl(165, 18, 'Жизненный цикл файла')
    s += ttl(485, 18, 'Режимы открытия')

    # Flow (left)
    steps = [
        (165, 50,  180, 34, '#dbeafe', '#3b82f6', '#1e40af', 'open(file, mode)\nоткрытие'),
        (165, 115, 180, 34, '#dcfce7', '#16a34a', '#14532d', 'read() / write()\nчтение / запись'),
        (165, 180, 180, 34, '#fef9c3', '#d97706', '#78350f', 'close() или\nwith as f:'),
    ]
    for cx, cy, bw, bh, fill, stroke, tc, text in steps:
        s += rct(cx, cy, bw, bh, fill, stroke, 7, text, 11, False, tc)

    s += arr(165, 67, 165, 98, '#475569')
    s += arr(165, 132, 165, 163, '#475569')

    # with statement
    s += rct(165, 240, 280, 34, '#ede9fe', '#8b5cf6', 7, 'with open(f) as file:  # рекомендуется\n    file.write(data)  # авто-close', 10, False, '#4c1d95')

    # Mode table (right)
    headers = ['Режим', 'Назначение', 'Существующий файл']
    rows = [
        ('r',   'Чтение',          'Читает с начала'),
        ('w',   'Запись',          '⚠️ Очищает файл'),
        ('a',   'Дополнение',      'Пишет в конец'),
        ('r+',  'Чтение+запись',   'Не очищает'),
        ('x',   'Создать новый',   '⚠️ Ошибка если есть'),
        ('rb',  'Бинарное чтение', 'Байты, не текст'),
        ('wb',  'Бинарная запись', '⚠️ Очищает файл'),
    ]
    col_w = [45, 100, 145]
    s += tbl(335, 30, headers, rows, col_w)
    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 11: Module import system (MOD14-L1)
# ═══════════════════════════════════════════════════════════
def diag_modules():
    VW, VH = 620, 270
    s = ''
    s += ttl(VW//2, 18, 'Как Python находит и загружает модуль')

    steps = [
        (80,  80, 130, 38, '#dbeafe', '#3b82f6', '#1e40af', 'import math\nвстречено'),
        (230, 80, 130, 38, '#fef9c3', '#d97706', '#78350f', 'sys.modules\nуже есть?'),
        (390, 80, 130, 38, '#dcfce7', '#16a34a', '#14532d', 'найти файл\nв sys.path'),
        (540, 80, 110, 38, '#ede9fe', '#8b5cf6', '#4c1d95', 'выполнить\n__init__ / .py'),
    ]
    for cx, cy, bw, bh, fill, stroke, tc, text in steps:
        s += rct(cx, cy, bw, bh, fill, stroke, 7, text, 11, False, tc)

    s += arr(145, 80, 165, 80, '#475569')
    s += arr(295, 80, 325, 80, '#475569')
    s += arr(455, 80, 480, 80, '#475569')

    # Yes branch from sys.modules
    s += lbl(230+5, 60, 'Да → сразу вернуть', '#16a34a', 10)
    s += parr(f'M 230 61 L 230 80', '#16a34a')
    s += lbl(230+65, 55, '→ вернуть из кэша', '#16a34a', 10)

    # sys.path locations
    s += hline(20, VW-20, 130, '#e2e8f0')
    s += ttl(VW//2, 148, 'sys.path — где Python ищет модули')
    paths = [
        ('1. Директория скрипта', '#1e40af'),
        ('2. PYTHONPATH переменная окружения', '#d97706'),
        ('3. Стандартная библиотека (lib/)', '#14532d'),
        ('4. site-packages (pip install)', '#4c1d95'),
    ]
    for i, (p, tc) in enumerate(paths):
        col = i % 2
        row = i // 2
        s += lbl(30 + col*300, 168 + row*26, p, tc, 11)

    s += hline(20, VW-20, 225, '#e2e8f0')
    s += cbx(20, 232, 580, 30, [
        ('import math          # встроенный', 0),
        ('from os import path  # из пакета', 1),
    ])
    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 12: Iterator protocol (MOD15-L1)
# ═══════════════════════════════════════════════════════════
def diag_iterators():
    VW, VH = 620, 280
    s = ''
    s += ttl(VW//2, 18, 'Протокол итератора в Python')

    # Main flow
    flow = [
        (70,  90, 110, 38, '#f1f5f9', '#94a3b8', '#475569', 'итерируемый\n объект'),
        (230, 90, 110, 38, '#dbeafe', '#3b82f6', '#1e40af', 'итератор\n(iter object)'),
        (390, 90, 110, 38, '#dcfce7', '#16a34a', '#14532d', 'следующее\nзначение'),
        (540, 90, 80,  38, '#fee2e2', '#dc2626', '#7f1d1d', 'Stop\nIteration'),
    ]
    for cx, cy, bw, bh, fill, stroke, tc, text in flow:
        s += rct(cx, cy, bw, bh, fill, stroke, 7, text, 11, False, tc)

    s += arr(125, 90, 175, 90, '#475569')
    s += lbl(150, 82, 'iter(obj)\n__iter__()', '#3b82f6', 9, 'middle')

    s += arr(285, 90, 335, 90, '#475569')
    s += lbl(310, 82, 'next(it)\n__next__()', '#16a34a', 9, 'middle')

    s += arr(445, 90, 500, 90, '#475569')
    s += lbl(473, 81, 'ещё есть?', '#64748b', 9, 'middle')

    # Loop back
    s += parr(f'M 390 109 L 390 145 L 230 145 L 230 109', '#16a34a')
    s += lbl(310, 157, 'повтор (следующий элемент)', '#16a34a', 10, 'middle')

    # Code example
    s += hline(20, VW-20, 175, '#e2e8f0')
    s += ttl(VW//2, 192, 'Пример: for = iter() + while + next()')
    s += cbx(20, 202, 290, 65, [
        ('# for x in [1, 2, 3]:', 0),
        ('it = iter([1, 2, 3])', 1),
        ('while True:', 0),
        ('    try: x = next(it)', 2),
        ('    except StopIteration: break', 6),
    ])
    s += cbx(330, 202, 280, 65, [
        ('# Свой итератор:', 0),
        ('class Counter:', 0),
        ('    def __iter__(self): return self', 2),
        ('    def __next__(self):', 2),
        ('        ...', 3),
    ])
    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 13: Generator yield (MOD15-L2)
# ═══════════════════════════════════════════════════════════
def diag_generators():
    VW, VH = 640, 310
    s = ''
    s += vline(320, 15, VH-10)
    s += ttl(160, 18, 'Обычная функция')
    s += ttl(480, 18, 'Функция-генератор (yield)')

    # Regular function flow
    reg_steps = [
        (160, 52, 'вызов f()', '#dbeafe', '#3b82f6', '#1e40af'),
        (160, 100, 'выполняется\nполностью', '#f1f5f9', '#94a3b8', '#475569'),
        (160, 152, 'return value', '#dcfce7', '#16a34a', '#14532d'),
        (160, 200, 'память\nосвобождена', '#fee2e2', '#dc2626', '#7f1d1d'),
    ]
    for cx, cy, text, fill, stroke, tc in reg_steps:
        s += rct(cx, cy, 140, 30, fill, stroke, 6, text, 11, False, tc)
    for i in range(len(reg_steps)-1):
        s += arr(160, reg_steps[i][1]+15, 160, reg_steps[i+1][1]-15, '#475569')

    # Generator flow
    gen_steps = [
        (480, 45,  'вызов gen()',  '#dbeafe', '#3b82f6', '#1e40af'),
        (480, 85,  'генераторный\nобъект создан', '#ede9fe', '#8b5cf6', '#4c1d95'),
        (480, 130, 'next() →\nвыполняется до yield', '#fef9c3', '#d97706', '#78350f'),
        (480, 177, 'yield value\n(приостановлен)', '#dcfce7', '#16a34a', '#14532d'),
        (480, 222, 'next() →\nпродолжает', '#fef9c3', '#d97706', '#78350f'),
        (480, 262, 'return / конец →\nStopIteration', '#fee2e2', '#dc2626', '#7f1d1d'),
    ]
    for cx, cy, text, fill, stroke, tc in gen_steps:
        s += rct(cx, cy, 150, 28, fill, stroke, 6, text, 10, False, tc)
    for i in range(len(gen_steps)-1):
        s += arr(480, gen_steps[i][1]+14, 480, gen_steps[i+1][1]-14, '#475569')

    # Loop-back arrow
    s += parr(f'M 555 191 L 580 191 L 580 144 L 555 144', '#16a34a')
    s += lbl(584, 170, '↻', '#16a34a', 16)

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 14: Decorators (MOD16-L1)
# ═══════════════════════════════════════════════════════════
def diag_decorators():
    VW, VH = 640, 310
    s = ''
    s += ttl(VW//2, 18, 'Декоратор: обёртка над функцией')

    # Syntax equivalence
    s += cbx(20, 30, 240, 50, [
        ('@timer', 4),
        ('def greet(name):', 0),
        ('    return f"Hello, {name}"', 1),
    ])
    s += arr(265, 55, 295, 55, '#475569')
    s += lbl(280, 47, '=', '#64748b', 14, 'middle')
    s += cbx(300, 30, 320, 50, [
        ('def greet(name):', 0),
        ('    return f"Hello, {name}"', 1),
        ('greet = timer(greet)', 4),
    ])

    # Stack diagram
    s += hline(20, VW-20, 98, '#e2e8f0')
    s += ttl(VW//2, 114, 'Стек вызовов при greet("Alice")')

    stack = [
        (320, 145, 280, 30, '#1e1e2e', '#44475a', '#cdd6f4', 'вызов: greet("Alice")'),
        (320, 183, 280, 30, '#dbeafe', '#3b82f6', '#1e40af', 'входит: timer_wrapper("Alice")'),
        (320, 221, 280, 30, '#fef9c3', '#d97706', '#78350f', 'start = time.time()'),
        (320, 259, 280, 30, '#dcfce7', '#16a34a', '#14532d', 'вызывает original greet("Alice")'),
        (320, 297, 280, 30, '#dcfce7', '#22c55e', '#14532d', 'возврат "Hello, Alice" + замер'),
    ]
    for cx, cy, bw, bh, fill, stroke, tc, text in stack:
        s += rct(cx, cy, bw, bh, fill, stroke, 6, text, 11, False, tc)

    for i in range(len(stack)-1):
        s += arr(320, stack[i][1]+15, 320, stack[i+1][1]-15, '#475569')

    # Example decorator
    s += cbx(20, 118, 280, 172, [
        ('def timer(func):', 0),
        ('    def wrapper(*args, **kw):', 0),
        ('        import time', 5),
        ('        start = time.time()', 3),
        ('        result = func(*args, **kw)', 1),
        ('        end = time.time()', 3),
        ('        print(f"Время: {end-start:.3f}s")', 4),
        ('        return result', 2),
        ('    return wrapper', 0),
        ('', 0),
    ])

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 15: Regex (MOD17-L1)
# ═══════════════════════════════════════════════════════════
def diag_regex():
    VW, VH = 640, 300
    s = ''
    s += ttl(VW//2, 18, 'Регулярные выражения: анатомия паттерна')

    # Pattern anatomy: (label, cx, bw, color, desc_or_None)
    char_y = 62
    parts = [
        ('^',       28,  24, '#dc2626', 'начало\nстроки'),
        ('(',       60,  20, '#94a3b8', None),
        ('[A-Z]',   98,  52, '#3b82f6', 'заглавная\nбуква'),
        ('\\d{2}', 145,  46, '#d97706', 'ровно 2\nцифры'),
        (')',      178,  20, '#94a3b8', None),
        ('-',      210,  20, '#475569', None),
        ('(',      238,  20, '#94a3b8', None),
        ('\\w+',  280,  44, '#16a34a', 'слово\n(1+)'),
        (')',      312,  20, '#94a3b8', None),
        ('$',      342,  24, '#dc2626', 'конец\nстроки'),
    ]

    for lbl_txt, cx, bw, color, desc in parts:
        s += rct(cx, char_y, bw, 28, '#f8fafc', color, 4, lbl_txt, 11)
        if desc:
            s += arr(cx, char_y+14, cx, char_y+44, color, 1.3)
            for li, ln in enumerate(desc.split('\n')):
                s += lbl(cx, char_y+57+li*13, ln, color, 9, 'middle')

    # Pattern label
    s += lbl(380, char_y+8, '^([A-Z]\\d{2})-(\\w+)$', '#1e293b', 13)

    # Quick reference table
    s += hline(20, VW-20, 125, '#e2e8f0')
    s += ttl(VW//2, 141, 'Шпаргалка по спецсимволам')

    qr = [
        [('\\d', '#3b82f6'), ('цифра [0-9]', '#1e293b'),  ('\\D', '#dc2626'), ('не цифра', '#1e293b')],
        [('\\w', '#16a34a'), ('буква/цифра/_', '#1e293b'), ('\\W', '#dc2626'), ('не \\w', '#1e293b')],
        [('\\s', '#d97706'), ('пробел/\\t/\\n', '#1e293b'),('\\S', '#dc2626'), ('не пробел', '#1e293b')],
        [('.', '#8b5cf6'),   ('любой символ', '#1e293b'),  ('^', '#dc2626'),   ('начало строки', '#1e293b')],
        [('*', '#3b82f6'),   ('0 или больше', '#1e293b'),  ('+', '#3b82f6'),   ('1 или больше', '#1e293b')],
        [('?', '#d97706'),   ('0 или 1', '#1e293b'),       ('{n,m}', '#16a34a'),('от n до m раз', '#1e293b')],
        [('[]', '#8b5cf6'),  ('класс символов', '#1e293b'),('()', '#4c1d95'),  ('группа захвата', '#1e293b')],
    ]

    cw = [50, 120, 50, 130]
    for ri, row in enumerate(qr):
        ry = 152 + ri*20
        cx = 20
        for ci, (cell_txt, cell_clr) in enumerate(row):
            s += lbl(cx, ry, cell_txt, cell_clr, 11)
            cx += cw[ci]

    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  ДИАГРАММА 16: Binary search (MOD18-L1)
# ═══════════════════════════════════════════════════════════
def diag_search():
    VW, VH = 640, 320
    s = ''
    s += vline(320, 15, VH-10)
    s += ttl(160, 18, 'Линейный поиск O(n)')
    s += ttl(480, 18, 'Бинарный поиск O(log n)')

    arr_vals = [2, 5, 8, 12, 16, 23, 38, 56]
    target = 23
    bw, bh = 30, 26
    x0 = 15

    # Linear search (left)
    for i, v in enumerate(arr_vals):
        cx = x0 + i*(bw+2) + bw//2
        found = (v == target)
        checked = (v <= target)
        fill = '#dcfce7' if found else ('#fef9c3' if checked else '#f1f5f9')
        stroke = '#16a34a' if found else ('#d97706' if checked else '#94a3b8')
        s += rct(cx, 42, bw, bh, fill, stroke, 4, str(v), 11, found)
        if checked:
            s += lbl(cx, 72, '✓' if not found else '★', '#d97706' if not found else '#16a34a', 10, 'middle')
    s += lbl(x0, 88, f'Проверено {len([v for v in arr_vals if v <= target])} шагов', '#dc2626', 10)

    # Steps description
    for i, v in enumerate(arr_vals):
        if v <= target:
            y = 100 + i*18
            icon = '✓ найдено!' if v == target else f'[{i}]={v} ≠ {target}'
            color = '#16a34a' if v == target else '#64748b'
            s += lbl(x0, y, icon, color, 10)

    # Binary search (right)
    rx0 = 330
    for i, v in enumerate(arr_vals):
        cx = rx0 + i*(bw+2) + bw//2
        s += rct(cx, 42, bw, bh, '#f1f5f9', '#94a3b8', 4, str(v), 11)
        s += lbl(cx, 72, str(i), '#94a3b8', 9, 'middle')

    steps_bs = [
        (0, 7, 3, 12, 23, 'lo=0,hi=7→mid=3: arr[3]=12 < 23, lo=4'),
        (4, 7, 5, 38, 23, 'lo=4,hi=7→mid=5: arr[5]=38 > 23, hi=4'),
        (4, 4, 4, 23, 23, 'lo=4,hi=4→mid=4: arr[4]=23 = 23 ✓'),
    ]
    for si, (lo, hi, mid, val, tgt, desc) in enumerate(steps_bs):
        sy = 88 + si*22
        s += lbl(rx0, sy, f'Шаг {si+1}: {desc}', '#1e293b' if si < 2 else '#16a34a', 9)
        # Highlight mid
        mcx = rx0 + mid*(bw+2) + bw//2
        clr = '#16a34a' if val == tgt else '#3b82f6'
        s += rct(mcx, 42, bw, bh, clr, clr, 4, str(val), 11, True, '#fff')

    # Comparison
    s += hline(20, VW-20, 160, '#e2e8f0')
    s += ttl(VW//2, 175, 'Сравнение производительности (n = 1 000 000)')

    comp_rows = [
        ('1 000 000', ('~1 000 000 шагов', '#dc2626'), ('~20 шагов', '#16a34a')),
        ('1 000',     ('~1 000 шагов', '#d97706'),     ('~10 шагов', '#16a34a')),
        ('100',       ('~100 шагов', '#d97706'),        ('~7 шагов', '#16a34a')),
    ]
    s += tbl(20, 185, ['Размер n', 'Линейный O(n)', 'Бинарный O(log₂n)'], comp_rows, [120, 155, 145])

    s += lbl(VW//2, 270, 'Требование бинарного поиска: массив должен быть ОТСОРТИРОВАН', '#d97706', 10, 'middle')
    return wrap(s, VW, VH)


# ═══════════════════════════════════════════════════════════
#  Таблица: ключевое слово → функция-строитель
# ═══════════════════════════════════════════════════════════

NEW_DIAGRAMS = [
    ('Установка',              diag_ide),
    ('Числовые типы',          diag_numbers),
    ('Строки: создание',       diag_strings),
    ('Булевы значения',        diag_booleans),
    ('Ловушки и нюансы',       diag_gotchas),
    ('Генераторы списков',     diag_comprehension),
    ('Кортежи, множества',     diag_tuples_sets),
    ('Быстрая сортировка',     diag_quicksort),
    ('Встроенная сортировка',  diag_sort_bigo),
    ('Файловый ввод-вывод',    diag_files),
    ('Модули, пакеты',         diag_modules),
    ('Итераторы: протокол',    diag_iterators),
    ('yield',                  diag_generators),
    ('Декоратор',              diag_decorators),
    ('Регулярные выражения',   diag_regex),
    ('Линейный и бинарный',    diag_search),
]

# ═══════════════════════════════════════════════════════════
#  Исправление старого формата wrapper'а
# ═══════════════════════════════════════════════════════════

# Старый формат wrapper'а: любой <div style="..."> содержащий text-align:center или overflow-x,
# который непосредственно предшествует <svg
OLD_WRAPPER_RE = re.compile(
    r'<div style="[^"]*(?:text-align:center|overflow-x)[^"]*">\s*(?=<svg)',
    re.IGNORECASE | re.DOTALL
)
OLD_SVG_STYLE_RE = re.compile(
    r'(<svg\b[^>]*?)\s*style="[^"]*(?:max-width|height:auto)[^"]*"',
    re.IGNORECASE
)

def fix_old_wrapper(content):
    """Заменяет старый div-wrapper на fc-diagram."""
    changed = False
    if OLD_WRAPPER_RE.search(content):
        content = OLD_WRAPPER_RE.sub('<div class="fc-diagram">', content)
        # Убрать старый inline style с SVG (CSS теперь управляет размером)
        content = OLD_SVG_STYLE_RE.sub(
            r'\1 preserveAspectRatio="xMidYMid meet" overflow="visible"',
            content
        )
        changed = True
    return content, changed


# ═══════════════════════════════════════════════════════════
#  Главный цикл
# ═══════════════════════════════════════════════════════════

fixed_old = 0
added_new = 0
errors = []

# Шаг 1: исправить старый формат
for lesson in TheoryLesson.objects.all():
    content = lesson.content or ''
    new_content, changed = fix_old_wrapper(content)
    if changed:
        lesson.content = new_content
        lesson.save(update_fields=['content'])
        fixed_old += 1

# Шаг 2: добавить новые диаграммы
for keyword, builder in NEW_DIAGRAMS:
    try:
        svg = builder()
    except Exception as e:
        errors.append(f'BUILD {keyword}: {e}')
        continue

    lessons = TheoryLesson.objects.filter(title__icontains=keyword)
    if not lessons.exists():
        errors.append(f'NOT FOUND: {keyword}')
        continue

    for lesson in lessons:
        content = lesson.content or ''
        if 'fc-diagram' in content:
            continue  # уже есть
        if MARKER in content:
            before = content[:content.index(MARKER) + len(MARKER)]
            lesson.content = before + '\n' + svg
        else:
            lesson.content = content + '\n' + MARKER + '\n' + svg
        lesson.save(update_fields=['content'])
        added_new += 1

# Итог
print(f'[OK] Исправлено старых wrapper: {fixed_old}')
print(f'[OK] Добавлено новых диаграмм: {added_new}')
if errors:
    print(f'[!!] Ошибки:')
    for e in errors:
        print(f'     {e}')

# Финальная статистика
from works.models import TheoryLesson as TL
total = TL.objects.count()
with_d = TL.objects.filter(content__contains='fc-diagram').count()
print(f'\nИтого: {with_d}/{total} уроков с диаграммами fc-diagram')
