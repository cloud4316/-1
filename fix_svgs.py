"""
Полная переработка SVG-диаграмм. Адаптивные, без фиксированной ширины.
Запуск: python fix_svgs.py
"""
import os, sys, django

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algorithm_site.settings')
django.setup()

from works.models import TheoryLesson

MARKER = '<!-- VISUAL_OK -->'

# ─────────────────────────────────────────────────────────────────
# SVG helpers
# ─────────────────────────────────────────────────────────────────

_aid = 0
def _mk():
    global _aid
    _aid += 1
    return f'arr{_aid}'

def wrap(inner, vw, vh):
    """Адаптивная обёртка без фиксированной ширины/высоты."""
    return (
        '<div class="fc-diagram">'
        f'<svg viewBox="0 0 {vw} {vh}" preserveAspectRatio="xMidYMid meet" '
        f'xmlns="http://www.w3.org/2000/svg" overflow="visible">'
        f'{inner}'
        '</svg></div>'
    )

def defs_arrow(aid, color):
    return (f'<defs><marker id="{aid}" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">'
            f'<polygon points="0 0,9 3.5,0 7" fill="{color}"/></marker></defs>')

def line(x1, y1, x2, y2, color='#475569', aw=1.8, arrow=True):
    aid = _mk()
    mk = f' marker-end="url(#{aid})"' if arrow else ''
    d = defs_arrow(aid, color) if arrow else ''
    return f'{d}<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{aw}"{mk}/>'

def path(d, color='#475569', aw=1.8, arrow=True):
    aid = _mk()
    mk = f' marker-end="url(#{aid})"' if arrow else ''
    df = defs_arrow(aid, color) if arrow else ''
    return f'{df}<path d="{d}" fill="none" stroke="{color}" stroke-width="{aw}"{mk}/>'

def oval(cx, cy, rw, rh, fill, stroke, tc, text, bold=False):
    fw = 'bold' if bold else 'normal'
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rw}" ry="{rh}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
            f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="13" font-weight="{fw}" fill="{tc}" font-family="sans-serif">{text}</text>')

def box(cx, cy, w, h, fill, stroke, tc, text, fs=13, bold=False, rx=7):
    fw = 'bold' if bold else 'normal'
    lines = text.split('\n')
    lh = 16
    total = lh * (len(lines) - 1)
    ty = cy - total / 2
    txt = ''.join(
        f'<text x="{cx}" y="{ty + i*lh}" text-anchor="middle" dominant-baseline="central" '
        f'font-size="{fs}" font-weight="{fw}" fill="{tc}" font-family="monospace">{ln}</text>'
        for i, ln in enumerate(lines)
    )
    return (f'<rect x="{cx-w//2}" y="{cy-h//2}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>{txt}')

def diamond(cx, cy, hw, hh, fill, stroke, tc, text, fs=12):
    pts = f'{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}'
    lines = text.split('\n')
    lh = 15
    total = lh * (len(lines) - 1)
    ty = cy - total / 2
    txt = ''.join(
        f'<text x="{cx}" y="{ty + i*lh}" text-anchor="middle" dominant-baseline="central" '
        f'font-size="{fs}" fill="{tc}" font-family="monospace">{ln}</text>'
        for i, ln in enumerate(lines)
    )
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>{txt}'

def label(x, y, text, color='#64748b', fs=11, anchor='start'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{color}" font-family="sans-serif">{text}</text>'

def code_box(x, y, w, h, lines):
    colors = ['#cdd6f4','#a6e3a1','#89dceb','#f9e2af','#cba6f7','#fab387']
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#1e1e2e" stroke="#44475a" stroke-width="1.2"/>'
    for i, (txt, ci) in enumerate(lines):
        c = colors[ci % len(colors)]
        out += f'<text x="{x+12}" y="{y+20+i*17}" font-size="11.5" fill="{c}" font-family="monospace">{txt}</text>'
    return out

def divider(x, y1, y2, vw):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#e2e8f0" stroke-width="1.5" stroke-dasharray="5,4"/>'

def col_title(x, y, text, color='#1e293b'):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="13" font-weight="bold" fill="{color}" font-family="sans-serif">{text}</text>'


# ─────────────────────────────────────────────────────────────────
# 1. IF / ELIF / ELSE
# ─────────────────────────────────────────────────────────────────
def make_if():
    VW, VH = 620, 400
    # Main axis
    mx = 210   # center x of main column
    # Right branch blocks center x
    rx = 460   # center x of action blocks
    bw = 150   # main box width
    rbw = 150  # right box width
    bh = 36
    dw, dh = 82, 27

    s = ''

    # Code hint
    s += code_box(10, 10, 170, 118, [
        ('if x > 0:', 0),
        ('    print("+")', 1),
        ('elif x < 0:', 0),
        ('    print("-")', 1),
        ('else:', 0),
        ('    print("0")', 1),
    ])

    # Start oval
    s += oval(mx, 35, 65, 17, '#dbeafe', '#3b82f6', '#1e40af', 'Начало', bold=True)
    s += line(mx, 52, mx, 80)

    # Diamond 1 (if x > 0)
    y1 = 107
    s += diamond(mx, y1, dw, dh, '#fef9c3', '#d97706', '#78350f', 'x > 0?')
    # Да →
    s += line(mx+dw, y1, rx-rbw//2, y1, '#16a34a', arrow=True)
    s += label(mx+dw+5, y1-5, 'Да', '#16a34a')
    s += box(rx, y1, rbw, bh, '#dcfce7', '#16a34a', '#14532d', 'print("+")')
    # Нет ↓
    s += line(mx, y1+dh, mx, y1+dh+33)
    s += label(mx+5, y1+dh+18, 'Нет', '#dc2626')

    # Diamond 2 (elif x < 0)
    y2 = y1 + dh + 60
    s += diamond(mx, y2, dw, dh, '#fef9c3', '#d97706', '#78350f', 'x < 0?')
    # Да →
    s += line(mx+dw, y2, rx-rbw//2, y2, '#16a34a', arrow=True)
    s += label(mx+dw+5, y2-5, 'Да', '#16a34a')
    s += box(rx, y2, rbw, bh, '#dcfce7', '#16a34a', '#14532d', 'print("-")')
    # Нет ↓
    s += line(mx, y2+dh, mx, y2+dh+33)
    s += label(mx+5, y2+dh+18, 'Нет', '#dc2626')

    # Else block
    y3 = y2 + dh + 60
    s += box(mx, y3, bw, bh, '#ede9fe', '#7c3aed', '#4c1d95', 'print("0")')
    s += line(mx, y3+bh//2, mx, y3+bh//2+35)

    # End oval
    ye = y3 + bh//2 + 52
    s += oval(mx, ye, 65, 17, '#dbeafe', '#3b82f6', '#1e40af', 'Конец', bold=True)

    # Merge: правые блоки → вертикаль → стрелка в Конец
    merge_x = rx + rbw//2 + 22
    end_rx = mx + 65  # right edge of End oval

    # Вертикальные линии от правых блоков вниз
    s += path(f'M {rx+rbw//2} {y1+bh//2} L {merge_x} {y1+bh//2} L {merge_x} {ye}',
              color='#94a3b8', arrow=False)
    s += path(f'M {rx+rbw//2} {y2+bh//2} L {merge_x} {y2+bh//2}',
              color='#94a3b8', arrow=False)
    # Стрелка влево к Конец
    s += line(merge_x, ye, end_rx+2, ye, '#475569', arrow=True)

    return wrap(s, VW, int(ye + 30))


# ─────────────────────────────────────────────────────────────────
# 2. WHILE
# ─────────────────────────────────────────────────────────────────
def make_while():
    VW, VH = 480, 420
    cx = 250
    bw, bh = 170, 38
    dw, dh = 90, 28

    s = ''

    # Code hint
    s += code_box(10, 10, 165, 88, [
        ('i = 0', 0),
        ('while i < n:', 0),
        ('    print(i)', 1),
        ('    i += 1', 2),
    ])

    # Init box
    s += box(cx, 38, bw, bh, '#dbeafe', '#3b82f6', '#1e40af', 'i = 0', bold=True)
    s += line(cx, 38+bh//2, cx, 95)

    # Diamond
    yd = 120
    s += diamond(cx, yd, dw, dh, '#fef9c3', '#d97706', '#78350f', 'i < n?')

    # Нет → выход (вправо)
    s += line(cx+dw, yd, cx+dw+65, yd, '#dc2626', arrow=True)
    s += label(cx+dw+4, yd-5, 'Нет', '#dc2626')
    s += box(cx+dw+65+45, yd, 70, 32, '#fee2e2', '#dc2626', '#7f1d1d', 'выход', fs=12)

    # Да ↓
    s += line(cx, yd+dh, cx, yd+dh+28)
    s += label(cx+5, yd+dh+16, 'Да', '#16a34a')

    # print(i)
    yb1 = yd + dh + 28 + bh//2
    s += box(cx, yb1, bw, bh, '#dcfce7', '#16a34a', '#14532d', 'print(i)')
    s += line(cx, yb1+bh//2, cx, yb1+bh//2+28)

    # i += 1
    yb2 = yb1 + bh//2 + 28 + bh//2
    s += box(cx, yb2, bw, bh, '#ede9fe', '#7c3aed', '#4c1d95', 'i += 1')

    # Петля обратно: из низа i+=1 → по левому краю → обратно к верху diamond
    loop_x = cx - dw - 45
    s += path(
        f'M {cx} {yb2+bh//2} L {cx} {yb2+bh//2+20} '
        f'L {loop_x} {yb2+bh//2+20} L {loop_x} {yd} L {cx-dw-2} {yd}',
        color='#7c3aed', arrow=True
    )
    s += label(loop_x-38, (yd + yb2)//2, '↺ повтор', '#7c3aed', fs=11)

    return wrap(s, VW, int(yb2 + bh//2 + 40))


# ─────────────────────────────────────────────────────────────────
# 3. FOR
# ─────────────────────────────────────────────────────────────────
def make_for():
    VW, VH = 640, 430
    s = ''
    div_x = 310

    # Заголовки
    s += col_title(155, 22, 'for x in список')
    s += col_title(475, 22, 'range(start, stop, step)')
    s += divider(div_x, 30, VH-10, VW)

    # Левая: список → переменная → тело → проверка → петля
    # Элементы списка
    items = [('10','#dbeafe','#1e40af'), ('20','#dcfce7','#14532d'),
             ('30','#fef9c3','#78350f'), ('40','#fce7f3','#9d174d')]
    for i, (v, bg, tc) in enumerate(items):
        bx = 15 + i*65
        s += box(bx+27, 55, 50, 36, bg, '#94a3b8', tc, v, bold=True)

    # Стрелки от списка к переменной
    var_cy = 120
    for i in range(4):
        bx = 15 + i*65 + 27
        s += line(bx, 73, 145, var_cy, '#94a3b8', aw=1.2)

    # Переменная x
    s += box(145, var_cy, 130, 36, '#c7d2fe', '#4f46e5', '#312e81', 'x = текущий', bold=True, fs=12)
    s += line(145, var_cy+18, 145, var_cy+46)

    # Тело цикла
    yb = var_cy + 64
    s += box(145, yb, 130, 36, '#dcfce7', '#16a34a', '#14532d', 'print(x)')
    s += line(145, yb+18, 145, yb+46)

    # Ромб "ещё элементы?"
    yd = yb + 46 + 27
    s += diamond(145, yd, 90, 26, '#fef9c3', '#d97706', '#78350f', 'ещё\nэлем?', fs=11)

    # Нет →
    s += line(145+90, yd, 145+90+40, yd, '#dc2626', arrow=True)
    s += label(145+92, yd-6, 'Нет', '#dc2626', fs=10)
    s += box(145+90+40+38, yd, 60, 28, '#fee2e2', '#dc2626', '#7f1d1d', 'конец', fs=11)

    # Да: петля обратно
    loop_x = 15
    s += path(
        f'M {145} {yd+26} L {145} {yd+46} L {loop_x} {yd+46} '
        f'L {loop_x} {var_cy} L {145-65} {var_cy}',
        color='#7c3aed', arrow=True
    )
    s += label(loop_x+2, (yd+var_cy)//2, 'Да', '#16a34a', fs=10)

    # Правая: range() таблица
    rows = [
        ('range(5)',    '→', '0, 1, 2, 3, 4'),
        ('range(2, 7)', '→', '2, 3, 4, 5, 6'),
        ('range(0,10,2)','→','0, 2, 4, 6, 8'),
        ('range(5,0,-1)','→','5, 4, 3, 2, 1'),
    ]
    for i, (call, arr, result) in enumerate(rows):
        y = 42 + i * 55
        s += box(380, y, 120, 38, '#f8fafc', '#cbd5e1', '#0f172a', call, fs=11)
        s += label(448, y+3, arr, '#64748b', fs=14, anchor='middle')
        s += box(530, y, 120, 38, '#f0fdf4', '#86efac', '#14532d', result, fs=11)

    # Вложенный цикл
    s += code_box(335, 280, 290, 72, [
        ('for i in range(3):', 0),
        ('  for j in range(3):', 0),
        ('    print(i, j)', 1),
        ('# выведет 9 пар (3×3)', 4),
    ])
    s += label(480, 368, '9 итераций = 3 × 3', '#64748b', fs=11, anchor='middle')

    return wrap(s, VW, int(yd + 70))


# ─────────────────────────────────────────────────────────────────
# 4. CALL STACK
# ─────────────────────────────────────────────────────────────────
def make_callstack():
    VW, VH = 600, 420
    s = ''
    div_x = 275

    s += col_title(137, 22, 'Код программы')
    s += col_title(437, 22, 'Стек вызовов')
    s += divider(div_x, 30, VH-10, VW)

    # Код
    s += code_box(15, 35, 248, 178, [
        ('def square(x):', 0),
        ('    return x * x', 1),
        ('', 0),
        ('def sum_sq(a, b):', 0),
        ('    s = square(a)', 2),
        ('    s += square(b)', 2),
        ('    return s', 1),
        ('', 0),
        ('result = sum_sq(3, 4)', 3),
    ])

    # Пояснение
    s += f'<rect x="15" y="225" width="248" height="60" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>'
    for i, txt in enumerate(['Каждый вызов функции', 'создаёт фрейм в стеке.', 'При return — удаляется.']):
        s += label(139, 243 + i*17, txt, '#1e40af', fs=11, anchor='middle')

    # Итог
    s += box(137, 308, 248, 34, '#dbeafe', '#3b82f6', '#1e40af', 'result = 9 + 16 = 25', bold=True, fs=12)

    # Стек фреймов (снизу вверх)
    frames = [
        ('#f1f5f9', '#64748b', '__main__',          'result = sum_sq(3, 4)'),
        ('#dbeafe', '#3b82f6', 'sum_sq(a=3, b=4)',  's = square(3)+square(4)'),
        ('#dcfce7', '#16a34a', 'square(x=3)',        'return 3*3 = 9'),
        ('#fef9c3', '#d97706', 'square(x=4)  ← TOP','return 4*4 = 16'),
    ]
    frame_h = 52
    frame_gap = 8
    for i, (bg, sc, title, detail) in enumerate(frames):
        fy = 40 + i * (frame_h + frame_gap)
        s += f'<rect x="290" y="{fy}" width="295" height="{frame_h}" rx="7" fill="{bg}" stroke="{sc}" stroke-width="1.5"/>'
        s += f'<text x="437" y="{fy+17}" text-anchor="middle" font-size="12" font-weight="bold" fill="{sc}" font-family="monospace">{title}</text>'
        s += f'<text x="437" y="{fy+34}" text-anchor="middle" font-size="11" fill="#475569" font-family="monospace">{detail}</text>'

    # Стрелки между фреймами
    for i in range(3):
        fy = 40 + i * (frame_h + frame_gap) + frame_h
        s += line(437, fy, 437, fy+frame_gap, '#6366f1', aw=1.5, arrow=False)
    s += label(490, 90, '← вызов ↓', '#6366f1', fs=10)
    s += label(490, 185, '↑ return', '#16a34a', fs=10)
    s += label(490, 245, '↑ return', '#16a34a', fs=10)

    return wrap(s, VW, 360)


# ─────────────────────────────────────────────────────────────────
# 5. RECURSION (factorial)
# ─────────────────────────────────────────────────────────────────
def make_recursion():
    VW, VH = 580, 520
    s = ''
    div_x = 285

    s += col_title(142, 22, '↓ Вызовы (раскрытие)', '#6366f1')
    s += col_title(432, 22, '↑ Возвраты (свёртка)', '#16a34a')
    s += divider(div_x, 30, VH-10, VW)

    calls = [
        ('fact(5)', '#dbeafe', '#3b82f6', '#1e40af'),
        ('fact(4)', '#ede9fe', '#8b5cf6', '#4c1d95'),
        ('fact(3)', '#dcfce7', '#16a34a', '#14532d'),
        ('fact(2)', '#fef9c3', '#d97706', '#78350f'),
        ('fact(1)', '#fee2e2', '#ef4444', '#7f1d1d'),
        ('return 1  (база)', '#f1f5f9', '#94a3b8', '#475569'),
    ]
    call_notes = ['5 × fact(4)', '4 × fact(3)', '3 × fact(2)', '2 × fact(1)', '1 × fact(0)=1']

    returns = [
        ('return 120', '#dbeafe', '#3b82f6', '#1e40af'),
        ('return  24', '#ede9fe', '#8b5cf6', '#4c1d95'),
        ('return   6', '#dcfce7', '#16a34a', '#14532d'),
        ('return   2', '#fef9c3', '#d97706', '#78350f'),
        ('return   1', '#fee2e2', '#ef4444', '#7f1d1d'),
        ('= 1', '#f1f5f9', '#94a3b8', '#475569'),
    ]
    ret_notes = ['5×24=120', '4×6=24', '3×2=6', '2×1=2', '1']

    bw, bh = 220, 40
    gap = 14
    step = bh + gap

    for i, ((txt, bg, sc, tc), (rtxt, rbg, rsc, rtc)) in enumerate(zip(calls, returns)):
        y = 38 + i * step
        # Левый блок (вызов)
        s += f'<rect x="20" y="{y}" width="{bw}" height="{bh}" rx="7" fill="{bg}" stroke="{sc}" stroke-width="1.5"/>'
        s += f'<text x="{20+bw//2}" y="{y+bh//2}" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="bold" fill="{tc}" font-family="monospace">{txt}</text>'

        # Правый блок (возврат)
        s += f'<rect x="{div_x+15}" y="{y}" width="{bw}" height="{bh}" rx="7" fill="{rbg}" stroke="{rsc}" stroke-width="1.5"/>'
        bold_r = 'bold' if i == 0 else 'normal'
        s += f'<text x="{div_x+15+bw//2}" y="{y+bh//2}" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="{bold_r}" fill="{rtc}" font-family="monospace">{rtxt}</text>'

        # Стрелки между блоками (кроме последнего)
        if i < 5:
            # Вниз (вызов)
            s += line(20+bw//2, y+bh, 20+bw//2, y+bh+gap, '#6366f1', aw=1.5)
            # Примечание
            s += label(20+bw//2+4, y+bh+gap//2+4, call_notes[i], '#6366f1', fs=10)
        if i > 0:
            # Вверх (возврат)
            s += line(div_x+15+bw//2, y+bh, div_x+15+bw//2, y+bh+gap, '#16a34a', aw=1.5, arrow=False)
            s += path(f'M {div_x+15+bw//2} {y+bh+gap} L {div_x+15+bw//2} {y+bh+gap-2}',
                      color='#16a34a', arrow=True)
            s += label(div_x+15+bw//2+4, y+bh+gap//2+4, ret_notes[i-1], '#16a34a', fs=10)

    total_h = 38 + len(calls) * step + 10
    return wrap(s, VW, total_h)


# ─────────────────────────────────────────────────────────────────
# Обновление уроков
# ─────────────────────────────────────────────────────────────────

FIXES = [
    ('if',       make_if),
    ('while',    make_while),
    ('for',      make_for),
    ('Функци',   make_callstack),
    ('Рекурси',  make_recursion),
]

updated = 0
for keyword, builder in FIXES:
    try:
        new_svg = builder()
    except Exception as e:
        print(f'[BUILD ERROR] {keyword}: {e}')
        import traceback; traceback.print_exc()
        continue

    lessons = TheoryLesson.objects.filter(title__icontains=keyword)
    if not lessons.exists():
        print(f'[NOT FOUND] {keyword}')
        continue

    for lesson in lessons:
        content = lesson.content or ''
        if MARKER in content:
            before = content[:content.index(MARKER) + len(MARKER)]
            lesson.content = before + '\n' + new_svg
        else:
            lesson.content = content + '\n' + MARKER + '\n' + new_svg
        lesson.save(update_fields=['content'])
        print(f'[OK] {lesson.title}')
        updated += 1

print(f'\nГотово: {updated} уроков обновлено.')
