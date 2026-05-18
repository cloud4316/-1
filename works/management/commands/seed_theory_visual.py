"""python manage.py seed_theory_visual
Добавляет SVG-диаграммы в существующие уроки + новые модули 15-18.
Повторный запуск безопасен (маркер VISUAL_OK предотвращает дублирование).
"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson

MARKER = '<!-- VISUAL_OK -->'

# ── SVG-обёртка ──────────────────────────────────────────────────────────────
def diagram(inner_svg, w=600, h=300, caption=''):
    cap = f'<p style="text-align:center;color:#64748b;font-size:13px;margin-top:6px">{caption}</p>' if caption else ''
    return (
        f'\n{MARKER}\n'
        f'<div style="overflow-x:auto;margin:1.5rem 0;text-align:center">'
        f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;'
        f'border-radius:12px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.08))" '
        f'xmlns="http://www.w3.org/2000/svg">{inner_svg}</svg>{cap}</div>'
    )

# ── Общие defs (стрелки) ──────────────────────────────────────────────────────
DEFS = '''<defs>
  <marker id="a" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#64748b"/>
  </marker>
  <marker id="ag" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#16a34a"/>
  </marker>
  <marker id="ar" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#dc2626"/>
  </marker>
  <marker id="av" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#6366f1"/>
  </marker>
</defs>'''

F = "font-family=\"'Segoe UI',Arial,sans-serif\""

# ═════════════════════════════════════════════════════════════════════════════
# ДИАГРАММЫ ДЛЯ СУЩЕСТВУЮЩИХ УРОКОВ
# ═════════════════════════════════════════════════════════════════════════════

# ── Модуль 1: Блок-схема алгоритма ───────────────────────────────────────────
FLOWCHART = diagram(f'''{DEFS}
<rect width="600" height="340" fill="#f8fafc" rx="12"/>
<text x="300" y="28" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Стандартные блоки блок-схемы</text>

<!-- Терминатор (начало/конец) -->
<ellipse cx="80" cy="80" rx="55" ry="24" fill="#6366f1"/>
<text x="80" y="85" text-anchor="middle" {F} font-size="13" fill="white" font-weight="600">Начало/Конец</text>
<text x="160" y="85" {F} font-size="12" fill="#475569">— терминатор (овал)</text>

<!-- Процесс -->
<rect x="25" y="128" width="110" height="36" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
<text x="80" y="151" text-anchor="middle" {F} font-size="13" fill="#15803d">Действие</text>
<text x="160" y="151" {F} font-size="12" fill="#475569">— процесс (прямоугольник)</text>

<!-- Ввод/вывод -->
<polygon points="25,188 135,188 120,224 10,224" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>
<text x="72" y="210" text-anchor="middle" {F} font-size="12" fill="#1d4ed8">Ввод / Вывод</text>
<text x="160" y="210" {F} font-size="12" fill="#475569">— данные (параллелограмм)</text>

<!-- Условие -->
<polygon points="80,248 135,272 80,296 25,272" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
<text x="80" y="277" text-anchor="middle" {F} font-size="12" fill="#92400e">условие?</text>
<text x="160" y="277" {F} font-size="12" fill="#475569">— решение (ромб)</text>
<text x="160" y="295" {F} font-size="11" fill="#94a3b8">Выходы: Да / Нет</text>

<!-- Разделитель -->
<line x1="320" y1="50" x2="320" y2="320" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4,3"/>

<!-- Правая часть: пример алгоритма -->
<text x="460" y="28" text-anchor="middle" {F} font-size="14" font-weight="700" fill="#1e293b">Пример: чётное число?</text>

<ellipse cx="460" cy="68" rx="50" ry="20" fill="#6366f1"/>
<text x="460" y="73" text-anchor="middle" {F} font-size="13" fill="white">Начало</text>

<line x1="460" y1="88" x2="460" y2="108" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>

<polygon points="370,110 460,110 550,110 460,110" fill="transparent"/>
<polygon points="410,110 510,110 490,140 430,140" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>
<text x="460" y="129" text-anchor="middle" {F} font-size="12" fill="#1d4ed8">Ввести n</text>

<line x1="460" y1="140" x2="460" y2="160" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>

<polygon points="460,162 520,185 460,208 400,185" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
<text x="460" y="182" text-anchor="middle" {F} font-size="12" fill="#92400e">n % 2 == 0</text>
<text x="460" y="197" text-anchor="middle" {F} font-size="11" fill="#92400e">?</text>

<!-- Да ветка -->
<line x1="460" y1="208" x2="460" y2="228" stroke="#16a34a" stroke-width="2" marker-end="url(#ag)"/>
<text x="470" y="223" {F} font-size="11" fill="#16a34a">Да</text>
<polygon points="415,230 505,230 490,254 400,254" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
<text x="450" y="247" text-anchor="middle" {F} font-size="12" fill="#15803d">Чётное!</text>

<!-- Нет ветка -->
<line x1="520" y1="185" x2="560" y2="185" stroke="#dc2626" stroke-width="2"/>
<line x1="560" y1="185" x2="560" y2="247" stroke="#dc2626" stroke-width="2"/>
<line x1="560" y1="247" x2="520" y2="247" stroke="#dc2626" stroke-width="2" marker-end="url(#ar)"/>
<text x="565" y="182" {F} font-size="11" fill="#dc2626">Нет</text>
<polygon points="520,237 560,237 545,258 505,258" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
<text x="532" y="252" text-anchor="middle" {F} font-size="12" fill="#dc2626">Нечётное!</text>

<!-- Конец -->
<line x1="460" y1="254" x2="460" y2="290" stroke="#64748b" stroke-width="2"/>
<line x1="460" y1="290" x2="375" y2="290" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>
<ellipse cx="345" cy="290" rx="38" ry="18" fill="#6366f1"/>
<text x="345" y="295" text-anchor="middle" {F} font-size="13" fill="white">Конец</text>
''', 600, 330, 'Стандартные обозначения блок-схем ISO 5807')

# ── Модуль 2: Модель памяти Python ───────────────────────────────────────────
MEMORY_MODEL = diagram(f'''{DEFS}
<rect width="620" height="280" fill="#f8fafc" rx="12"/>
<text x="310" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Переменные Python — имена, не ячейки</text>

<!-- Левая панель: пространство имён -->
<rect x="20" y="50" width="180" height="210" rx="8" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>
<text x="110" y="72" text-anchor="middle" {F} font-size="13" font-weight="700" fill="#5b21b6">Пространство имён</text>
<text x="110" y="87" text-anchor="middle" {F} font-size="11" fill="#7c3aed">(namespace)</text>

<!-- Имена -->
<rect x="35" y="100" width="100" height="28" rx="5" fill="white" stroke="#7c3aed" stroke-width="1.5"/>
<text x="85" y="119" text-anchor="middle" {F} font-size="13" fill="#3730a3">x</text>

<rect x="35" y="145" width="100" height="28" rx="5" fill="white" stroke="#7c3aed" stroke-width="1.5"/>
<text x="85" y="164" text-anchor="middle" {F} font-size="13" fill="#3730a3">name</text>

<rect x="35" y="190" width="100" height="28" rx="5" fill="white" stroke="#7c3aed" stroke-width="1.5"/>
<text x="85" y="209" text-anchor="middle" {F} font-size="13" fill="#3730a3">items</text>

<rect x="35" y="235" width="100" height="28" rx="5" fill="#fef9c3" stroke="#7c3aed" stroke-width="1.5"/>
<text x="85" y="254" text-anchor="middle" {F} font-size="13" fill="#3730a3">y</text>

<!-- Стрелки к объектам -->
<line x1="135" y1="114" x2="280" y2="114" stroke="#6366f1" stroke-width="2" marker-end="url(#av)"/>
<line x1="135" y1="159" x2="280" y2="159" stroke="#6366f1" stroke-width="2" marker-end="url(#av)"/>
<line x1="135" y1="204" x2="280" y2="204" stroke="#6366f1" stroke-width="2" marker-end="url(#av)"/>
<line x1="135" y1="249" x2="280" y2="114" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#av)"/>
<text x="200" y="240" {F} font-size="11" fill="#d97706" transform="rotate(-15,200,240)">y = x</text>

<!-- Правая панель: объекты в куче -->
<rect x="280" y="50" width="320" height="210" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
<text x="440" y="72" text-anchor="middle" {F} font-size="13" font-weight="700" fill="#15803d">Куча (Heap)</text>
<text x="440" y="87" text-anchor="middle" {F} font-size="11" fill="#16a34a">объекты хранятся здесь</text>

<!-- Объект int -->
<rect x="295" y="100" width="140" height="28" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="365" y="119" text-anchor="middle" {F} font-size="12" fill="#15803d">int: 42  (id=0x7fa3)</text>

<!-- Объект str -->
<rect x="295" y="145" width="140" height="28" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="365" y="164" text-anchor="middle" {F} font-size="12" fill="#15803d">str: "Алиса"</text>

<!-- Объект list -->
<rect x="295" y="190" width="140" height="28" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="365" y="209" text-anchor="middle" {F} font-size="12" fill="#15803d">list: [1, 2, 3]</text>

<!-- Замечание -->
<rect x="20" y="268" width="580" height="0" rx="5" fill="transparent"/>
<text x="310" y="270" text-anchor="middle" {F} font-size="11" fill="#64748b">Переменная — это лишь ярлык. Несколько имён могут ссылаться на один объект.</text>
''', 620, 280, 'x = 42 | name = "Алиса" | items = [1,2,3] | y = x  →  y is x → True')

# ── Модуль 3: if / elif / else ────────────────────────────────────────────────
IF_FLOW = diagram(f'''{DEFS}
<rect width="560" height="320" fill="#f8fafc" rx="12"/>
<text x="280" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Поток выполнения if / elif / else</text>

<!-- Вход -->
<line x1="280" y1="40" x2="280" y2="58" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>

<!-- ромб 1 -->
<polygon points="280,60 360,90 280,120 200,90" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
<text x="280" y="87" text-anchor="middle" {F} font-size="12" fill="#92400e">if условие1</text>
<text x="280" y="102" text-anchor="middle" {F} font-size="11" fill="#92400e">True?</text>

<!-- True → блок 1 -->
<line x1="280" y1="120" x2="280" y2="148" stroke="#16a34a" stroke-width="2" marker-end="url(#ag)"/>
<text x="290" y="138" {F} font-size="11" fill="#16a34a">True</text>
<rect x="220" y="150" width="120" height="36" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
<text x="280" y="173" text-anchor="middle" {F} font-size="12" fill="#15803d">блок if</text>

<!-- Нет → ромб 2 -->
<line x1="360" y1="90" x2="430" y2="90" stroke="#64748b" stroke-width="2"/>
<line x1="430" y1="90" x2="430" y2="175" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>
<text x="395" y="84" {F} font-size="11" fill="#64748b">False</text>

<polygon points="430,177 510,207 430,237 350,207" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
<text x="430" y="204" text-anchor="middle" {F} font-size="12" fill="#92400e">elif условие2</text>
<text x="430" y="219" text-anchor="middle" {F} font-size="11" fill="#92400e">True?</text>

<!-- True → блок 2 -->
<line x1="430" y1="237" x2="430" y2="262" stroke="#16a34a" stroke-width="2" marker-end="url(#ag)"/>
<text x="440" y="255" {F} font-size="11" fill="#16a34a">True</text>
<rect x="370" y="264" width="120" height="36" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
<text x="430" y="287" text-anchor="middle" {F} font-size="12" fill="#15803d">блок elif</text>

<!-- Нет → else -->
<line x1="510" y1="207" x2="540" y2="207" stroke="#64748b" stroke-width="2"/>
<line x1="540" y1="207" x2="540" y2="282" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>
<text x="522" y="201" {F} font-size="11" fill="#64748b">False</text>
<rect x="510" y="264" width="60" height="36" rx="5" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
<text x="540" y="287" text-anchor="middle" {F} font-size="12" fill="#dc2626">else</text>

<!-- Слияние -->
<line x1="280" y1="186" x2="280" y2="305" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,3"/>
<line x1="430" y1="300" x2="430" y2="305" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,3"/>
<line x1="540" y1="300" x2="540" y2="305" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,3"/>
<line x1="280" y1="305" x2="540" y2="305" stroke="#64748b" stroke-width="1.5"/>
<line x1="410" y1="305" x2="410" y2="315" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>
<text x="410" y="312" text-anchor="middle" {F} font-size="12" fill="#475569">продолжение программы</text>
''', 560, 330, 'Выполняется ровно один из блоков — первый с True')

# ── Модуль 4: while-цикл ─────────────────────────────────────────────────────
WHILE_FLOW = diagram(f'''{DEFS}
<rect width="500" height="300" fill="#f8fafc" rx="12"/>
<text x="250" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Поток выполнения while-цикла</text>

<!-- Вход -->
<line x1="140" y1="42" x2="140" y2="62" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>

<!-- Ромб -->
<polygon points="140,64 230,100 140,136 50,100" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
<text x="140" y="97" text-anchor="middle" {F} font-size="13" fill="#92400e">условие</text>
<text x="140" y="113" text-anchor="middle" {F} font-size="11" fill="#92400e">True?</text>

<!-- True → тело -->
<line x1="140" y1="136" x2="140" y2="160" stroke="#16a34a" stroke-width="2" marker-end="url(#ag)"/>
<text x="152" y="153" {F} font-size="11" fill="#16a34a">True</text>
<rect x="75" y="162" width="130" height="48" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
<text x="140" y="183" text-anchor="middle" {F} font-size="13" fill="#15803d">тело цикла</text>
<text x="140" y="200" text-anchor="middle" {F} font-size="11" fill="#16a34a">(изменяем условие!)</text>

<!-- Обратная стрелка -->
<line x1="140" y1="210" x2="140" y2="230" stroke="#64748b" stroke-width="2"/>
<line x1="140" y1="230" x2="20" y2="230" stroke="#64748b" stroke-width="2"/>
<line x1="20" y1="230" x2="20" y2="100" stroke="#64748b" stroke-width="2"/>
<line x1="20" y1="100" x2="50" y2="100" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>
<text x="10" y="165" {F} font-size="11" fill="#64748b" writing-mode="tb">повтор</text>

<!-- False → выход -->
<line x1="230" y1="100" x2="290" y2="100" stroke="#dc2626" stroke-width="2" marker-end="url(#ar)"/>
<text x="258" y="92" {F} font-size="11" fill="#dc2626">False</text>
<rect x="292" y="80" width="100" height="40" rx="5" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
<text x="342" y="105" text-anchor="middle" {F} font-size="13" fill="#dc2626">выход</text>
<line x1="342" y1="120" x2="342" y2="148" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>
<text x="342" y="165" text-anchor="middle" {F} font-size="12" fill="#475569">следующий</text>
<text x="342" y="180" text-anchor="middle" {F} font-size="12" fill="#475569">код</text>

<!-- break и continue -->
<text x="250" y="240" text-anchor="middle" {F} font-size="14" font-weight="700" fill="#1e293b">break и continue</text>
<rect x="20" y="255" width="140" height="35" rx="5" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
<text x="90" y="275" text-anchor="middle" {F} font-size="12" fill="#dc2626">break → немедленный выход</text>
<rect x="175" y="255" width="140" height="35" rx="5" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
<text x="245" y="275" text-anchor="middle" {F} font-size="12" fill="#92400e">continue → следующая итерация</text>
<rect x="330" y="255" width="140" height="35" rx="5" fill="#f0f9ff" stroke="#0ea5e9" stroke-width="1.5"/>
<text x="400" y="270" text-anchor="middle" {F} font-size="12" fill="#0369a1">while/else → блок else</text>
<text x="400" y="284" text-anchor="middle" {F} font-size="11" fill="#0369a1">если не было break</text>
''', 500, 300, 'while условие: — проверяет ПЕРЕД каждой итерацией')

# ── Модуль 5: for-цикл ───────────────────────────────────────────────────────
FOR_ITER = diagram(f'''{DEFS}
<rect width="620" height="260" fill="#f8fafc" rx="12"/>
<text x="310" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">for-цикл: итерация по последовательности</text>

<!-- Последовательность -->
<text x="30" y="60" {F} font-size="13" fill="#475569">fruits = [</text>
<rect x="30" y="70" width="80" height="38" rx="5" fill="#6366f1"/>
<text x="70" y="94" text-anchor="middle" {F} font-size="14" fill="white" font-weight="600">"яблоко"</text>
<rect x="120" y="70" width="80" height="38" rx="5" fill="#6366f1"/>
<text x="160" y="94" text-anchor="middle" {F} font-size="14" fill="white" font-weight="600">"банан"</text>
<rect x="210" y="70" width="80" height="38" rx="5" fill="#6366f1"/>
<text x="250" y="94" text-anchor="middle" {F} font-size="14" fill="white" font-weight="600">"вишня"</text>
<text x="295" y="94" {F} font-size="13" fill="#475569">]</text>

<!-- Индексы -->
<text x="70" y="122" text-anchor="middle" {F} font-size="12" fill="#94a3b8">[0]</text>
<text x="160" y="122" text-anchor="middle" {F} font-size="12" fill="#94a3b8">[1]</text>
<text x="250" y="122" text-anchor="middle" {F} font-size="12" fill="#94a3b8">[2]</text>

<!-- Стрелка итерации 1 -->
<line x1="70" y1="108" x2="70" y2="145" stroke="#6366f1" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#av)"/>
<rect x="20" y="148" width="100" height="30" rx="5" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
<text x="70" y="168" text-anchor="middle" {F} font-size="12" fill="#5b21b6">fruit="яблоко"</text>

<line x1="160" y1="108" x2="160" y2="145" stroke="#6366f1" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#av)"/>
<rect x="110" y="148" width="100" height="30" rx="5" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
<text x="160" y="168" text-anchor="middle" {F} font-size="12" fill="#5b21b6">fruit="банан"</text>

<line x1="250" y1="108" x2="250" y2="145" stroke="#6366f1" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#av)"/>
<rect x="200" y="148" width="100" height="30" rx="5" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
<text x="250" y="168" text-anchor="middle" {F} font-size="12" fill="#5b21b6">fruit="вишня"</text>

<!-- Тело -->
<text x="30" y="205" {F} font-size="13" fill="#334155">    print(fruit)</text>
<line x1="20" y1="178" x2="20" y2="220" stroke="#16a34a" stroke-width="2"/>
<line x1="20" y1="220" x2="320" y2="220" stroke="#16a34a" stroke-width="1" stroke-dasharray="3,2"/>
<text x="30" y="238" {F} font-size="11" fill="#64748b">тело выполняется для каждого элемента</text>

<!-- range() -->
<line x1="350" y1="50" x2="620" y2="50" stroke="#e2e8f0" stroke-width="1"/>
<text x="490" y="40" text-anchor="middle" {F} font-size="11" fill="#94a3b8">← отдельный блок →</text>
<text x="370" y="75" {F} font-size="14" font-weight="700" fill="#1e293b">range(start, stop, step)</text>

<rect x="360" y="85" width="240" height="30" rx="4" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
<text x="370" y="105" {F} font-size="12" fill="#1d4ed8">range(5)        → 0,1,2,3,4</text>
<rect x="360" y="122" width="240" height="30" rx="4" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
<text x="370" y="142" {F} font-size="12" fill="#1d4ed8">range(1,6)      → 1,2,3,4,5</text>
<rect x="360" y="159" width="240" height="30" rx="4" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
<text x="370" y="179" {F} font-size="12" fill="#1d4ed8">range(0,10,2)   → 0,2,4,6,8</text>
<rect x="360" y="196" width="240" height="30" rx="4" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
<text x="370" y="216" {F} font-size="12" fill="#1d4ed8">range(10,0,-1)  → 10,9,...,1</text>
<text x="370" y="250" {F} font-size="11" fill="#64748b">range — ленивый генератор, памяти не тратит!</text>
''', 620, 260, 'for fruit in fruits: — перебирает элементы по одному')

# ── Модуль 6: Стек вызовов ───────────────────────────────────────────────────
CALL_STACK = diagram(f'''{DEFS}
<rect width="540" height="300" fill="#f8fafc" rx="12"/>
<text x="270" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Стек вызовов функций (Call Stack)</text>

<!-- Код слева -->
<text x="20" y="55" {F} font-size="12" fill="#475569" font-weight="600">Код:</text>
<rect x="15" y="62" width="220" height="220" rx="6" fill="#1e293b"/>
<text x="28" y="84" {F} font-size="12" fill="#a5b4fc">def</text>
<text x="55" y="84" {F} font-size="12" fill="#34d399">square</text>
<text x="115" y="84" {F} font-size="12" fill="#e2e8f0">(x):</text>
<text x="28" y="103" {F} font-size="12" fill="#e2e8f0">    return x * x</text>

<text x="28" y="128" {F} font-size="12" fill="#a5b4fc">def</text>
<text x="55" y="128" {F} font-size="12" fill="#34d399">sum_sq</text>
<text x="118" y="128" {F} font-size="12" fill="#e2e8f0">(a, b):</text>
<text x="28" y="147" {F} font-size="12" fill="#e2e8f0">    s1 = square(a)</text>
<text x="28" y="166" {F} font-size="12" fill="#e2e8f0">    s2 = square(b)</text>
<text x="28" y="185" {F} font-size="12" fill="#e2e8f0">    return s1 + s2</text>

<text x="28" y="210" {F} font-size="12" fill="#fbbf24">result</text>
<text x="78" y="210" {F} font-size="12" fill="#e2e8f0"> = sum_sq(3, 4)</text>
<text x="28" y="229" {F} font-size="12" fill="#fbbf24">print</text>
<text x="67" y="229" {F} font-size="12" fill="#e2e8f0">(result)  # 25</text>
<rect x="15" y="200" width="220" height="14" rx="2" fill="#fbbf24" opacity="0.15"/>

<!-- Стрелка -->
<text x="252" y="165" {F} font-size="22" fill="#64748b">→</text>

<!-- Стек справа -->
<text x="285" y="55" {F} font-size="12" fill="#475569" font-weight="600">Стек во время square(3):</text>

<!-- Фрейм square -->
<rect x="285" y="65" width="230" height="60" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
<text x="295" y="83" {F} font-size="12" font-weight="700" fill="#15803d">square(x=3)    ← текущий</text>
<text x="295" y="100" {F} font-size="12" fill="#166534">  x = 3</text>
<text x="295" y="116" {F} font-size="12" fill="#166534">  return: 9</text>

<!-- Фрейм sum_sq -->
<rect x="285" y="135" width="230" height="70" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>
<text x="295" y="153" {F} font-size="12" font-weight="700" fill="#1d4ed8">sum_sq(a=3, b=4)</text>
<text x="295" y="170" {F} font-size="12" fill="#1e40af">  a = 3, b = 4</text>
<text x="295" y="187" {F} font-size="12" fill="#1e40af">  s1 = ??? (ждёт)</text>
<text x="295" y="203" {F} font-size="12" fill="#1e40af">  s2 = ???</text>

<!-- Фрейм глобальный -->
<rect x="285" y="215" width="230" height="50" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="2"/>
<text x="295" y="233" {F} font-size="12" font-weight="700" fill="#475569">&lt;module&gt;  (глобальный)</text>
<text x="295" y="252" {F} font-size="12" fill="#64748b">  result = ???</text>

<!-- Метки -->
<text x="520" y="95" {F} font-size="11" fill="#16a34a">TOP</text>
<text x="520" y="255" {F} font-size="11" fill="#94a3b8">BOT</text>
<line x1="515" y1="65" x2="515" y2="265" stroke="#e2e8f0" stroke-width="1"/>
<line x1="510" y1="65" x2="515" y2="65" stroke="#16a34a" stroke-width="1.5"/>
<line x1="510" y1="265" x2="515" y2="265" stroke="#94a3b8" stroke-width="1.5"/>

<text x="270" y="285" {F} font-size="11" fill="#64748b">Стек растёт вверх. После return фрейм удаляется (pop).</text>
''', 540, 300, 'Каждый вызов функции добавляет новый фрейм на стек')

# ── Модуль 7: Список — раскладка в памяти ────────────────────────────────────
LIST_LAYOUT = diagram(f'''{DEFS}
<rect width="620" height="270" fill="#f8fafc" rx="12"/>
<text x="310" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Список Python: индексация и срезы</text>

<!-- Заголовок массива -->
<text x="30" y="56" {F} font-size="13" fill="#475569">nums = [</text>

<!-- Ячейки -->
<rect x="120" y="65" width="70" height="50" rx="6" fill="#6366f1"/>
<text x="155" y="88" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">10</text>
<text x="155" y="104" text-anchor="middle" {F} font-size="11" fill="#c7d2fe">[0] / [-5]</text>

<rect x="200" y="65" width="70" height="50" rx="6" fill="#6366f1"/>
<text x="235" y="88" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">20</text>
<text x="235" y="104" text-anchor="middle" {F} font-size="11" fill="#c7d2fe">[1] / [-4]</text>

<rect x="280" y="65" width="70" height="50" rx="6" fill="#6366f1"/>
<text x="315" y="88" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">30</text>
<text x="315" y="104" text-anchor="middle" {F} font-size="11" fill="#c7d2fe">[2] / [-3]</text>

<rect x="360" y="65" width="70" height="50" rx="6" fill="#6366f1"/>
<text x="395" y="88" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">40</text>
<text x="395" y="104" text-anchor="middle" {F} font-size="11" fill="#c7d2fe">[3] / [-2]</text>

<rect x="440" y="65" width="70" height="50" rx="6" fill="#6366f1"/>
<text x="475" y="88" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">50</text>
<text x="475" y="104" text-anchor="middle" {F} font-size="11" fill="#c7d2fe">[4] / [-1]</text>

<text x="520" y="95" {F} font-size="13" fill="#475569">]</text>

<!-- Срезы -->
<text x="30" y="140" {F} font-size="13" font-weight="700" fill="#1e293b">Срезы: nums[start:stop:step]</text>

<!-- Срез 1:3 -->
<rect x="200" y="148" width="145" height="6" rx="3" fill="#f59e0b" opacity="0.8"/>
<text x="272" y="168" text-anchor="middle" {F} font-size="12" fill="#d97706">nums[1:3] → [20, 30]</text>

<!-- Срез ::2 -->
<rect x="120" y="178" width="35" height="6" rx="3" fill="#10b981" opacity="0.8"/>
<rect x="280" y="178" width="35" height="6" rx="3" fill="#10b981" opacity="0.8"/>
<rect x="440" y="178" width="35" height="6" rx="3" fill="#10b981" opacity="0.8"/>
<text x="310" y="198" text-anchor="middle" {F} font-size="12" fill="#059669">nums[::2] → [10, 30, 50]</text>

<!-- Срез ::-1 -->
<text x="30" y="222" {F} font-size="12" fill="#6366f1">nums[::-1] → [50, 40, 30, 20, 10]</text>
<text x="30" y="240" {F} font-size="12" fill="#6366f1">nums[-2:]  → [40, 50]</text>
<text x="310" y="222" {F} font-size="12" fill="#475569">len(nums) = 5</text>
<text x="310" y="240" {F} font-size="12" fill="#475569">Изменение: nums[0] = 99</text>
<text x="310" y="258" {F} font-size="11" fill="#94a3b8">Срез создаёт НОВЫЙ список!</text>
''', 620, 270, 'nums = [10, 20, 30, 40, 50]')

# ── Модуль 8: Словарь — хэш-таблица ─────────────────────────────────────────
DICT_HASH = diagram(f'''{DEFS}
<rect width="600" height="300" fill="#f8fafc" rx="12"/>
<text x="300" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Словарь как хэш-таблица</text>

<!-- Ключи -->
<text x="30" y="58" {F} font-size="13" font-weight="700" fill="#475569">Ключи</text>
<rect x="20" y="68" width="80" height="30" rx="5" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
<text x="60" y="88" text-anchor="middle" {F} font-size="13" fill="#5b21b6">"name"</text>
<rect x="20" y="108" width="80" height="30" rx="5" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
<text x="60" y="128" text-anchor="middle" {F} font-size="13" fill="#5b21b6">"age"</text>
<rect x="20" y="148" width="80" height="30" rx="5" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
<text x="60" y="168" text-anchor="middle" {F} font-size="13" fill="#5b21b6">"city"</text>

<!-- Хэш-функция -->
<rect x="130" y="85" width="110" height="110" rx="8" fill="#1e293b"/>
<text x="185" y="118" text-anchor="middle" {F} font-size="13" fill="#a5b4fc" font-weight="700">hash()</text>
<text x="185" y="138" text-anchor="middle" {F} font-size="11" fill="#94a3b8">функция</text>
<text x="185" y="155" text-anchor="middle" {F} font-size="11" fill="#94a3b8">преобразования</text>
<text x="185" y="172" text-anchor="middle" {F} font-size="11" fill="#94a3b8">ключа → индекс</text>

<line x1="100" y1="83" x2="130" y2="110" stroke="#7c3aed" stroke-width="1.5" marker-end="url(#av)"/>
<line x1="100" y1="123" x2="130" y2="140" stroke="#7c3aed" stroke-width="1.5" marker-end="url(#av)"/>
<line x1="100" y1="163" x2="130" y2="165" stroke="#7c3aed" stroke-width="1.5" marker-end="url(#av)"/>

<!-- Бакеты (ячейки) -->
<text x="270" y="58" {F} font-size="13" font-weight="700" fill="#475569">Внутренняя таблица</text>
<rect x="260" y="65" width="20" height="25" rx="2" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
<text x="270" y="82" text-anchor="middle" {F} font-size="10" fill="#64748b">0</text>
<rect x="260" y="93" width="20" height="25" rx="2" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="270" y="110" text-anchor="middle" {F} font-size="10" fill="#15803d">1</text>
<rect x="260" y="121" width="20" height="25" rx="2" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="270" y="138" text-anchor="middle" {F} font-size="10" fill="#15803d">2</text>
<rect x="260" y="149" width="20" height="25" rx="2" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
<text x="270" y="166" text-anchor="middle" {F} font-size="10" fill="#64748b">3</text>
<rect x="260" y="177" width="20" height="25" rx="2" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="270" y="194" text-anchor="middle" {F} font-size="10" fill="#15803d">4</text>
<rect x="260" y="205" width="20" height="25" rx="2" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
<text x="270" y="222" text-anchor="middle" {F} font-size="10" fill="#64748b">5</text>

<line x1="240" y1="140" x2="260" y2="106" stroke="#10b981" stroke-width="1.5" marker-end="url(#ag)"/>
<line x1="240" y1="140" x2="260" y2="134" stroke="#10b981" stroke-width="1.5" marker-end="url(#ag)"/>
<line x1="240" y1="140" x2="260" y2="189" stroke="#10b981" stroke-width="1.5" marker-end="url(#ag)"/>

<!-- Пары ключ-значение -->
<rect x="295" y="90" width="160" height="30" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="375" y="110" text-anchor="middle" {F} font-size="12" fill="#15803d">"name" → "Алиса"</text>
<rect x="295" y="120" width="160" height="30" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="375" y="140" text-anchor="middle" {F} font-size="12" fill="#15803d">"age"  → 21</text>
<rect x="295" y="174" width="160" height="30" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="375" y="194" text-anchor="middle" {F} font-size="12" fill="#15803d">"city" → "Москва"</text>

<!-- Характеристики -->
<text x="480" y="70" {F} font-size="13" font-weight="700" fill="#1e293b">Сложность:</text>
<text x="480" y="92" {F} font-size="13" fill="#15803d">get:    O(1) ✓</text>
<text x="480" y="112" {F} font-size="13" fill="#15803d">set:    O(1) ✓</text>
<text x="480" y="132" {F} font-size="13" fill="#15803d">delete: O(1) ✓</text>
<text x="480" y="152" {F} font-size="13" fill="#dc2626">поиск:  O(n) ✗</text>
<rect x="470" y="170" width="115" height="80" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
<text x="527" y="190" text-anchor="middle" {F} font-size="11" fill="#92400e">Ключи должны</text>
<text x="527" y="207" text-anchor="middle" {F} font-size="11" fill="#92400e">быть hashable!</text>
<text x="527" y="224" text-anchor="middle" {F} font-size="11" fill="#92400e">str, int, tuple ✓</text>
<text x="527" y="240" text-anchor="middle" {F} font-size="11" fill="#dc2626">list, dict ✗</text>

<text x="30" y="265" {F} font-size="11" fill="#64748b">С Python 3.7+ словари сохраняют порядок вставки (insertion order).</text>
''', 600, 280, 'd = {"name":"Алиса", "age":21} | d["name"] → O(1)')

# ── Модуль 9: Иерархия исключений ────────────────────────────────────────────
EXCEPTION_TREE = diagram(f'''{DEFS}
<rect width="620" height="310" fill="#f8fafc" rx="12"/>
<text x="310" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Иерархия исключений Python</text>

<!-- BaseException -->
<rect x="235" y="40" width="150" height="30" rx="5" fill="#dc2626"/>
<text x="310" y="60" text-anchor="middle" {F} font-size="13" fill="white" font-weight="700">BaseException</text>

<!-- Ветки от BaseException -->
<line x1="280" y1="70" x2="120" y2="100" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="310" y1="70" x2="310" y2="100" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="340" y1="70" x2="500" y2="100" stroke="#94a3b8" stroke-width="1.5"/>

<!-- SystemExit -->
<rect x="40" y="102" width="110" height="26" rx="4" fill="#fca5a5" stroke="#dc2626" stroke-width="1"/>
<text x="95" y="120" text-anchor="middle" {F} font-size="12" fill="#7f1d1d">SystemExit</text>

<!-- KeyboardInterrupt -->
<rect x="255" y="102" width="115" height="26" rx="4" fill="#fca5a5" stroke="#dc2626" stroke-width="1"/>
<text x="312" y="120" text-anchor="middle" {F} font-size="12" fill="#7f1d1d">KeyboardInterrupt</text>

<!-- Exception -->
<rect x="435" y="102" width="115" height="30" rx="5" fill="#f97316"/>
<text x="492" y="122" text-anchor="middle" {F} font-size="13" fill="white" font-weight="700">Exception</text>

<!-- Ветки от Exception -->
<line x1="492" y1="132" x2="390" y2="162" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="492" y1="132" x2="492" y2="162" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="492" y1="132" x2="580" y2="162" stroke="#94a3b8" stroke-width="1.5"/>

<!-- ValueError -->
<rect x="330" y="164" width="110" height="24" rx="4" fill="#fed7aa" stroke="#f97316" stroke-width="1"/>
<text x="385" y="180" text-anchor="middle" {F} font-size="11" fill="#7c2d12">ValueError</text>
<!-- TypeError -->
<rect x="450" y="164" width="95" height="24" rx="4" fill="#fed7aa" stroke="#f97316" stroke-width="1"/>
<text x="497" y="180" text-anchor="middle" {F} font-size="11" fill="#7c2d12">TypeError</text>
<!-- OSError -->
<rect x="555" y="164" width="80" height="24" rx="4" fill="#fed7aa" stroke="#f97316" stroke-width="1"/>
<text x="595" y="180" text-anchor="middle" {F} font-size="11" fill="#7c2d12">OSError</text>

<!-- OSError дети -->
<line x1="595" y1="188" x2="575" y2="210" stroke="#94a3b8" stroke-width="1"/>
<line x1="595" y1="188" x2="600" y2="210" stroke="#94a3b8" stroke-width="1"/>
<rect x="540" y="212" width="80" height="22" rx="3" fill="#ffedd5" stroke="#f97316" stroke-width="1"/>
<text x="580" y="227" text-anchor="middle" {F} font-size="10" fill="#7c2d12">FileNotFoundError</text>
<rect x="540" y="238" width="80" height="22" rx="3" fill="#ffedd5" stroke="#f97316" stroke-width="1"/>
<text x="580" y="253" text-anchor="middle" {F} font-size="10" fill="#7c2d12">PermissionError</text>

<!-- ArithmeticError -->
<line x1="492" y1="132" x2="200" y2="162" stroke="#94a3b8" stroke-width="1.5"/>
<rect x="140" y="164" width="125" height="24" rx="4" fill="#fed7aa" stroke="#f97316" stroke-width="1"/>
<text x="202" y="180" text-anchor="middle" {F} font-size="11" fill="#7c2d12">ArithmeticError</text>
<line x1="202" y1="188" x2="202" y2="208" stroke="#94a3b8" stroke-width="1"/>
<rect x="148" y="210" width="108" height="22" rx="3" fill="#ffedd5" stroke="#f97316" stroke-width="1"/>
<text x="202" y="225" text-anchor="middle" {F} font-size="10" fill="#7c2d12">ZeroDivisionError</text>

<!-- LookupError -->
<line x1="492" y1="132" x2="60" y2="162" stroke="#94a3b8" stroke-width="1.5"/>
<rect x="10" y="164" width="100" height="24" rx="4" fill="#fed7aa" stroke="#f97316" stroke-width="1"/>
<text x="60" y="180" text-anchor="middle" {F} font-size="11" fill="#7c2d12">LookupError</text>
<line x1="60" y1="188" x2="40" y2="208" stroke="#94a3b8" stroke-width="1"/>
<line x1="60" y1="188" x2="80" y2="208" stroke="#94a3b8" stroke-width="1"/>
<rect x="10" y="210" width="55" height="22" rx="3" fill="#ffedd5" stroke="#f97316" stroke-width="1"/>
<text x="37" y="225" text-anchor="middle" {F} font-size="10" fill="#7c2d12">IndexError</text>
<rect x="70" y="210" width="50" height="22" rx="3" fill="#ffedd5" stroke="#f97316" stroke-width="1"/>
<text x="95" y="225" text-anchor="middle" {F} font-size="10" fill="#7c2d12">KeyError</text>

<!-- except подсказка -->
<rect x="30" y="270" width="560" height="32" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
<text x="310" y="284" text-anchor="middle" {F} font-size="12" fill="#15803d">except ValueError ловит ValueError и его подклассы</text>
<text x="310" y="298" text-anchor="middle" {F} font-size="11" fill="#16a34a">except Exception — ловит всё кроме SystemExit и KeyboardInterrupt</text>
''', 620, 315, 'Перехватывать исключение — значит перехватить его и все дочерние')

# ── Модуль 10: Сортировка пузырьком — один проход ────────────────────────────
BUBBLE_SORT = diagram(f'''{DEFS}
<rect width="600" height="300" fill="#f8fafc" rx="12"/>
<text x="300" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Сортировка пузырьком: один проход</text>

<!-- Исходный массив -->
<text x="20" y="56" {F} font-size="12" fill="#64748b">Исходный:</text>
<rect x="20" y="62" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="45" y="87" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">5</text>
<rect x="80" y="62" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="105" y="87" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">3</text>
<rect x="140" y="62" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="165" y="87" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">8</text>
<rect x="200" y="62" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="225" y="87" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">1</text>
<rect x="260" y="62" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="285" y="87" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">4</text>

<!-- Шаг 1: сравнение 5 и 3, обмен -->
<text x="20" y="120" {F} font-size="12" fill="#64748b">Шаг 1  (5&gt;3 → обмен):</text>
<rect x="20" y="126" width="50" height="40" rx="4" fill="#10b981"/>
<text x="45" y="151" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">3</text>
<rect x="80" y="126" width="50" height="40" rx="4" fill="#10b981"/>
<text x="105" y="151" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">5</text>
<rect x="140" y="126" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="165" y="151" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">8</text>
<rect x="200" y="126" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="225" y="151" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">1</text>
<rect x="260" y="126" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="285" y="151" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">4</text>
<path d="M 20,126 Q 45,108 80,126" stroke="#10b981" stroke-width="2" fill="none" marker-end="url(#ag)"/>

<!-- Шаг 2: 5 и 8 — нет обмена -->
<text x="20" y="184" {F} font-size="12" fill="#64748b">Шаг 2  (5&lt;8 → нет обмена):</text>
<rect x="20" y="190" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="45" y="215" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">3</text>
<rect x="80" y="190" width="50" height="40" rx="4" fill="#f59e0b"/>
<text x="105" y="215" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">5</text>
<rect x="140" y="190" width="50" height="40" rx="4" fill="#f59e0b"/>
<text x="165" y="215" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">8</text>
<rect x="200" y="190" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="225" y="215" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">1</text>
<rect x="260" y="190" width="50" height="40" rx="4" fill="#6366f1"/>
<text x="285" y="215" text-anchor="middle" {F} font-size="18" fill="white" font-weight="700">4</text>
<text x="145" y="245" text-anchor="middle" {F} font-size="20" fill="#16a34a">✓</text>

<!-- Big-O таблица -->
<line x1="340" y1="45" x2="340" y2="280" stroke="#e2e8f0" stroke-width="1"/>
<text x="470" y="60" text-anchor="middle" {F} font-size="13" font-weight="700" fill="#1e293b">Сложность алгоритмов</text>
<rect x="350" y="68" width="230" height="26" rx="4" fill="#1e293b"/>
<text x="420" y="85" text-anchor="middle" {F} font-size="11" fill="#94a3b8" font-weight="600">Алгоритм</text>
<text x="540" y="85" text-anchor="middle" {F} font-size="11" fill="#94a3b8" font-weight="600">Лучшее / Среднее / Худшее</text>

<rect x="350" y="96" width="230" height="24" rx="3" fill="#fee2e2"/>
<text x="420" y="112" text-anchor="middle" {F} font-size="11" fill="#1e293b">Пузырьковая</text>
<text x="540" y="112" text-anchor="middle" {F} font-size="11" fill="#dc2626">O(n) / O(n²) / O(n²)</text>

<rect x="350" y="122" width="230" height="24" rx="3" fill="#fef3c7"/>
<text x="420" y="138" text-anchor="middle" {F} font-size="11" fill="#1e293b">Выбором</text>
<text x="540" y="138" text-anchor="middle" {F} font-size="11" fill="#d97706">O(n²) / O(n²) / O(n²)</text>

<rect x="350" y="148" width="230" height="24" rx="3" fill="#fef3c7"/>
<text x="420" y="164" text-anchor="middle" {F} font-size="11" fill="#1e293b">Вставками</text>
<text x="540" y="164" text-anchor="middle" {F} font-size="11" fill="#d97706">O(n) / O(n²) / O(n²)</text>

<rect x="350" y="174" width="230" height="24" rx="3" fill="#dcfce7"/>
<text x="420" y="190" text-anchor="middle" {F} font-size="11" fill="#1e293b">Слиянием</text>
<text x="540" y="190" text-anchor="middle" {F} font-size="11" fill="#15803d">O(n log n) все случаи</text>

<rect x="350" y="200" width="230" height="24" rx="3" fill="#dcfce7"/>
<text x="420" y="216" text-anchor="middle" {F} font-size="11" fill="#1e293b">Быстрая</text>
<text x="540" y="216" text-anchor="middle" {F} font-size="11" fill="#15803d">O(n log n) / O(n log n) / O(n²)</text>

<rect x="350" y="226" width="230" height="24" rx="3" fill="#dbeafe"/>
<text x="420" y="242" text-anchor="middle" {F} font-size="11" fill="#1e293b">Timsort (Python)</text>
<text x="540" y="242" text-anchor="middle" {F} font-size="11" fill="#1d4ed8">O(n) / O(n log n) / O(n log n)</text>
''', 600, 300, '[5,3,8,1,4] → за n-1 проходов максимум "всплывает" вправо')

# ── Модуль 11: Дерево рекурсии ───────────────────────────────────────────────
RECURSION_TREE = diagram(f'''{DEFS}
<rect width="620" height="310" fill="#f8fafc" rx="12"/>
<text x="310" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Дерево рекурсии: factorial(4)</text>

<!-- Уровень 0 -->
<rect x="265" y="38" width="90" height="30" rx="5" fill="#6366f1"/>
<text x="310" y="58" text-anchor="middle" {F} font-size="13" fill="white" font-weight="600">factorial(4)</text>
<text x="360" y="52" {F} font-size="11" fill="#64748b"> = 4 × 6 = 24</text>

<line x1="310" y1="68" x2="220" y2="95" stroke="#64748b" stroke-width="1.5" marker-end="url(#a)"/>
<text x="248" y="88" {F} font-size="11" fill="#64748b">вызов</text>

<!-- Уровень 1 -->
<rect x="165" y="97" width="90" height="30" rx="5" fill="#7c3aed"/>
<text x="210" y="117" text-anchor="middle" {F} font-size="13" fill="white" font-weight="600">factorial(3)</text>
<text x="260" y="112" {F} font-size="11" fill="#64748b"> = 3 × 2 = 6</text>

<line x1="210" y1="127" x2="150" y2="155" stroke="#64748b" stroke-width="1.5" marker-end="url(#a)"/>

<!-- Уровень 2 -->
<rect x="90" y="157" width="90" height="30" rx="5" fill="#0ea5e9"/>
<text x="135" y="177" text-anchor="middle" {F} font-size="13" fill="white" font-weight="600">factorial(2)</text>
<text x="185" y="172" {F} font-size="11" fill="#64748b"> = 2 × 1 = 2</text>

<line x1="135" y1="187" x2="100" y2="215" stroke="#64748b" stroke-width="1.5" marker-end="url(#a)"/>

<!-- Уровень 3 -->
<rect x="40" y="217" width="90" height="30" rx="5" fill="#10b981"/>
<text x="85" y="237" text-anchor="middle" {F} font-size="13" fill="white" font-weight="600">factorial(1)</text>
<text x="135" y="232" {F} font-size="11" fill="#64748b"> = 1 × 1 = 1</text>

<line x1="85" y1="247" x2="60" y2="272" stroke="#64748b" stroke-width="1.5" marker-end="url(#a)"/>

<!-- Базовый случай -->
<rect x="20" y="274" width="90" height="30" rx="5" fill="#16a34a"/>
<text x="65" y="294" text-anchor="middle" {F} font-size="13" fill="white" font-weight="700">factorial(0)</text>
<text x="115" y="289" {F} font-size="11" fill="#16a34a" font-weight="600">← BASE CASE → return 1</text>

<!-- Обратный ход -->
<text x="350" y="58" {F} font-size="13" font-weight="700" fill="#1e293b">Обратный ход (return):</text>
<text x="320" y="80" {F} font-size="12" fill="#16a34a">factorial(0) → 1</text>
<line x1="310" y1="83" x2="310" y2="95" stroke="#16a34a" stroke-width="1.5" marker-end="url(#ag)"/>
<text x="320" y="110" {F} font-size="12" fill="#10b981">factorial(1) → 1×1 = 1</text>
<line x1="310" y1="113" x2="310" y2="125" stroke="#10b981" stroke-width="1.5" marker-end="url(#ag)"/>
<text x="320" y="140" {F} font-size="12" fill="#0ea5e9">factorial(2) → 2×1 = 2</text>
<line x1="310" y1="143" x2="310" y2="155" stroke="#0ea5e9" stroke-width="1.5" marker-end="url(#ag)"/>
<text x="320" y="170" {F} font-size="12" fill="#7c3aed">factorial(3) → 3×2 = 6</text>
<line x1="310" y1="173" x2="310" y2="185" stroke="#7c3aed" stroke-width="1.5" marker-end="url(#ag)"/>
<text x="320" y="200" {F} font-size="12" fill="#6366f1">factorial(4) → 4×6 = 24</text>
<rect x="310" y="207" width="200" height="30" rx="5" fill="#6366f1"/>
<text x="410" y="227" text-anchor="middle" {F} font-size="13" fill="white" font-weight="700">Результат: 24 ✓</text>

<!-- Глубина стека -->
<rect x="320" y="250" width="280" height="50" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
<text x="460" y="268" text-anchor="middle" {F} font-size="12" fill="#92400e">Глубина стека = n+1 фреймов</text>
<text x="460" y="285" text-anchor="middle" {F} font-size="11" fill="#92400e">Без базового случая → RecursionError!</text>
<text x="460" y="298" text-anchor="middle" {F} font-size="11" fill="#92400e">(sys.setrecursionlimit по умолчанию 1000)</text>
''', 620, 315, 'Каждый вызов ожидает результат от следующего уровня')

# ── Модуль 13: Диаграмма классов ─────────────────────────────────────────────
CLASS_DIAGRAM = diagram(f'''{DEFS}
<rect width="620" height="320" fill="#f8fafc" rx="12"/>
<text x="310" y="26" text-anchor="middle" {F} font-size="15" font-weight="700" fill="#1e293b">Наследование классов (UML-диаграмма)</text>

<!-- Базовый класс Animal -->
<rect x="220" y="42" width="180" height="100" rx="6" fill="#1e293b" stroke="#6366f1" stroke-width="2"/>
<rect x="220" y="42" width="180" height="28" rx="6" fill="#6366f1"/>
<rect x="220" y="56" width="180" height="14" rx="0" fill="#6366f1"/>
<text x="310" y="62" text-anchor="middle" {F} font-size="14" fill="white" font-weight="700">Animal</text>
<line x1="220" y1="72" x2="400" y2="72" stroke="#334155" stroke-width="1"/>
<text x="228" y="88" {F} font-size="12" fill="#a5b4fc">+ name: str</text>
<text x="228" y="104" {F} font-size="12" fill="#a5b4fc">+ sound: str</text>
<line x1="220" y1="112" x2="400" y2="112" stroke="#334155" stroke-width="1"/>
<text x="228" y="128" {F} font-size="12" fill="#34d399">+ speak()</text>
<text x="228" y="143" {F} font-size="12" fill="#34d399">+ __str__()</text>

<!-- Стрелки наследования -->
<line x1="250" y1="142" x2="130" y2="175" stroke="#64748b" stroke-width="2"/>
<line x1="370" y1="142" x2="490" y2="175" stroke="#64748b" stroke-width="2"/>
<!-- Треугольники (наследование) -->
<polygon points="120,168 140,168 130,155" fill="white" stroke="#64748b" stroke-width="2"/>
<polygon points="480,168 500,168 490,155" fill="white" stroke="#64748b" stroke-width="2"/>

<!-- Класс Dog -->
<rect x="20" y="178" width="210" height="120" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
<rect x="20" y="178" width="210" height="28" rx="6" fill="#10b981"/>
<rect x="20" y="192" width="210" height="14" rx="0" fill="#10b981"/>
<text x="125" y="198" text-anchor="middle" {F} font-size="14" fill="white" font-weight="700">Dog</text>
<text x="50" y="208" {F} font-size="11" fill="#86efac">наследует Animal</text>
<line x1="20" y1="210" x2="230" y2="210" stroke="#334155" stroke-width="1"/>
<text x="28" y="225" {F} font-size="12" fill="#a5b4fc">+ breed: str</text>
<line x1="20" y1="234" x2="230" y2="234" stroke="#334155" stroke-width="1"/>
<text x="28" y="250" {F} font-size="12" fill="#34d399">+ speak()  → "Гав!"</text>
<text x="28" y="266" {F} font-size="12" fill="#34d399">+ fetch()</text>
<text x="28" y="282" {F} font-size="11" fill="#64748b">переопределяет speak()</text>

<!-- Класс Cat -->
<rect x="390" y="178" width="210" height="120" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
<rect x="390" y="178" width="210" height="28" rx="6" fill="#f59e0b"/>
<rect x="390" y="192" width="210" height="14" rx="0" fill="#f59e0b"/>
<text x="495" y="198" text-anchor="middle" {F} font-size="14" fill="white" font-weight="700">Cat</text>
<text x="420" y="208" {F} font-size="11" fill="#fde68a">наследует Animal</text>
<line x1="390" y1="210" x2="600" y2="210" stroke="#334155" stroke-width="1"/>
<text x="398" y="225" {F} font-size="12" fill="#a5b4fc">+ indoor: bool</text>
<line x1="390" y1="234" x2="600" y2="234" stroke="#334155" stroke-width="1"/>
<text x="398" y="250" {F} font-size="12" fill="#34d399">+ speak() → "Мяу!"</text>
<text x="398" y="266" {F} font-size="12" fill="#34d399">+ purr()</text>
<text x="398" y="282" {F} font-size="11" fill="#64748b">переопределяет speak()</text>

<!-- Полиморфизм -->
<rect x="160" y="310" width="300" height="0" rx="5"/>
<text x="310" y="308" text-anchor="middle" {F} font-size="12" fill="#6366f1">Полиморфизм: for a in [Dog("Рекс"), Cat("Мурка")]: a.speak()</text>
''', 620, 320, 'Дочерний класс наследует атрибуты и методы родителя')

# ─────────────────────────────────────────────────────────────────────────────
# Сопоставление: заголовок урока → SVG для добавления
# ─────────────────────────────────────────────────────────────────────────────
VISUALS = {
    'Что такое программирование и алгоритм': FLOWCHART,
    'Переменные, имена и память':            MEMORY_MODEL,
    'if / elif / else — полный разбор':      IF_FLOW,
    'Цикл while — от простого к сложному':  WHILE_FLOW,
    'Цикл for: итерация по последовательностям': FOR_ITER,
    'Функции: определение, аргументы, возврат':  CALL_STACK,
    'Списки: создание, индексация, методы':      LIST_LAYOUT,
    'Словари: хранение данных по ключу':         DICT_HASH,
    'Исключения: try, except, finally, raise':   EXCEPTION_TREE,
    'Квадратичные алгоритмы сортировки':         BUBBLE_SORT,
    'Рекурсия: суть, принципы, практика':        RECURSION_TREE,
    'Классы и объекты в Python':                 CLASS_DIAGRAM,
}

# ─────────────────────────────────────────────────────────────────────────────
# НОВЫЕ МОДУЛИ
# ─────────────────────────────────────────────────────────────────────────────
def tip(t):   return f'<div class="tip">💡 {t}</div>'
def warn(t):  return f'<div class="warning">⚠️ {t}</div>'
def info(t):  return f'<div class="tip" style="background:#e0f2fe;border-color:#0284c7">ℹ️ {t}</div>'

NEW_MODULES = [
{
'title': 'Генераторы и итераторы',
'icon': 'fas fa-infinity',
'order': 15,
'description': 'Ленивые вычисления, yield, генераторные выражения и протокол итератора.',
'lessons': [
{
'title': 'Итераторы: протокол __iter__ и __next__',
'order': 1,
'estimated_minutes': 80,
'content': '''
<h2>Что такое итератор?</h2>
<p><strong>Итератор</strong> — объект, который помнит текущую позицию и умеет выдавать следующий элемент по запросу. Это фундаментальный протокол Python, лежащий в основе всех циклов <code>for</code>.</p>

<h3>Протокол итератора</h3>
<pre><code># Любой итерируемый объект реализует:
# __iter__() → возвращает сам итератор
# __next__() → возвращает следующий элемент или поднимает StopIteration

nums = [10, 20, 30]
it = iter(nums)       # вызывает nums.__iter__()
print(next(it))       # 10  — вызывает it.__next__()
print(next(it))       # 20
print(next(it))       # 30
# next(it)            # StopIteration!</code></pre>
''' + tip('Цикл for — это синтаксический сахар: Python вызывает iter(), затем next() в цикле, ловит StopIteration.') + '''

<h3>Как for работает "под капотом"</h3>
<pre><code># for x in iterable:
#     body(x)
# Эквивалентно:
_it = iter(iterable)
while True:
    try:
        x = next(_it)
        body(x)
    except StopIteration:
        break</code></pre>

<h2>Разница: Iterable vs Iterator</h2>
<table class="theory-table">
<thead><tr><th>Понятие</th><th>Метод</th><th>Пример</th><th>Можно перебрать дважды?</th></tr></thead>
<tbody>
<tr><td>Iterable</td><td>__iter__</td><td>list, str, tuple, dict</td><td>Да (каждый раз новый итератор)</td></tr>
<tr><td>Iterator</td><td>__iter__ + __next__</td><td>iter(list), file, zip, enumerate</td><td>Нет (одноразовый)</td></tr>
</tbody></table>

<pre><code># Список — iterable, не iterator
lst = [1, 2, 3]
print(type(lst))          # list
print(type(iter(lst)))    # list_iterator

# Файл — iterator!
f = open("data.txt")
print(f is iter(f))       # True — файл сам себе итератор
# После исчерпания файла повторное чтение вернёт пустоту</code></pre>

<h2>Создание собственного итератора</h2>
<pre><code>class CountDown:
    """Обратный отсчёт от n до 1."""
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self          # итератор — это мы сами

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

for n in CountDown(5):
    print(n, end=" ")      # 5 4 3 2 1</code></pre>

<h2>Встроенные итераторы</h2>
<pre><code># enumerate — добавляет индекс
for i, ch in enumerate("abc", start=1):
    print(i, ch)   # 1 a, 2 b, 3 c

# zip — параллельный обход
names = ["Иван", "Мария"]
scores = [95, 87]
for n, s in zip(names, scores):
    print(f"{n}: {s}")

# map и filter — ленивые трансформации
squares = map(lambda x: x**2, range(10))  # не считает сразу!
evens   = filter(lambda x: x % 2 == 0, range(10))
print(list(squares))  # [0,1,4,9,16,25,36,49,64,81]

# zip_longest из itertools
from itertools import zip_longest
a = [1, 2, 3]
b = ["a", "b"]
print(list(zip_longest(a, b, fillvalue="-")))
# [(1,"a"), (2,"b"), (3,"-")]</code></pre>
''' + info('map, filter, zip, enumerate — все возвращают итераторы, а не списки. Оборачивай в list() только когда нужны все значения сразу.'),
},
{
'title': 'Генераторы: yield и генераторные выражения',
'order': 2,
'estimated_minutes': 90,
'content': '''
<h2>Что такое генератор?</h2>
<p>Генератор — функция с оператором <code>yield</code>. При вызове она не выполняется сразу, а возвращает объект-генератор. Каждый вызов <code>next()</code> выполняет функцию до следующего <code>yield</code> и <strong>приостанавливается</strong>, сохраняя всё состояние.</p>

<pre><code>def count_up(n):
    i = 1
    while i <= n:
        yield i       # приостановка, возврат значения
        i += 1        # возобновление отсюда при следующем next()

gen = count_up(3)
print(type(gen))     # generator
print(next(gen))     # 1
print(next(gen))     # 2
print(next(gen))     # 3
# next(gen)          # StopIteration</code></pre>

''' + tip('yield — это как return, но функция "запоминает" где остановилась и продолжает с того же места.') + '''

<h2>Бесконечные генераторы</h2>
<pre><code>def fibonacci():
    a, b = 0, 1
    while True:         # бесконечный — никогда не кончается
        yield a
        a, b = b, a + b

fib = fibonacci()
for _ in range(10):
    print(next(fib), end=" ")  # 0 1 1 2 3 5 8 13 21 34

# Первые 10 чисел Фибоначчи без хранения всей последовательности!</code></pre>

<h2>Генераторные выражения</h2>
<p>Как list comprehension, но в круглых скобках. <strong>Ленивые</strong> — не создают список в памяти.</p>
<pre><code># List comprehension — сразу создаёт список
squares_list = [x**2 for x in range(1_000_000)]  # 8 МБ в памяти!

# Генераторное выражение — ленивое
squares_gen = (x**2 for x in range(1_000_000))   # почти 0 байт!

# Используем когда нужно
total = sum(x**2 for x in range(1_000_000))       # sum принимает итерируемое
print(total)

# Цепочка генераторов — конвейер данных
lines = (line.strip() for line in open("data.txt"))
words = (word for line in lines for word in line.split())
upper = (w.upper() for w in words if len(w) > 3)
# Данные текут по конвейеру по одному слову — нет промежуточных списков!</code></pre>

<h2>yield from</h2>
<pre><code>def chain(*iterables):
    for it in iterables:
        yield from it     # делегирование итерации

print(list(chain([1,2], "ab", (3,4))))
# [1, 2, 'a', 'b', 3, 4]</code></pre>

<h2>send() — двунаправленная передача данных</h2>
<pre><code>def accumulator():
    total = 0
    while True:
        value = yield total   # получаем значение через send()
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)                 # запускаем генератор до первого yield
print(acc.send(10))       # 10
print(acc.send(20))       # 30
print(acc.send(5))        # 35</code></pre>

<h2>Сравнение: список vs генератор</h2>
<table class="theory-table">
<thead><tr><th>Характеристика</th><th>Список</th><th>Генератор</th></tr></thead>
<tbody>
<tr><td>Вычисление</td><td>Сразу всё</td><td>По требованию (lazy)</td></tr>
<tr><td>Память</td><td>O(n)</td><td>O(1)</td></tr>
<tr><td>Скорость первого элемента</td><td>Медленнее</td><td>Мгновенно</td></tr>
<tr><td>Повторный обход</td><td>Да</td><td>Нет (одноразовый)</td></tr>
<tr><td>len()</td><td>Да</td><td>Нет</td></tr>
<tr><td>Индексация [i]</td><td>Да</td><td>Нет</td></tr>
</tbody></table>

''' + tip('Правило: если нужен список больше одного раза — создавай list(). Если один проход по большим данным — используй генератор.'),
},
]
},

{
'title': 'Декораторы',
'icon': 'fas fa-magic',
'order': 16,
'description': 'Функции высшего порядка, синтаксис @decorator, functools.wraps, встроенные декораторы.',
'lessons': [
{
'title': 'Декораторы: обёртки над функциями',
'order': 1,
'estimated_minutes': 85,
'content': '''
<h2>Что такое декоратор?</h2>
<p>Декоратор — функция, которая принимает другую функцию и возвращает новую с расширенным поведением. Синтаксис <code>@decorator</code> — это просто синтаксический сахар.</p>

<pre><code># Без синтаксиса @:
def greet(name):
    return f"Привет, {name}!"

def shout(func):            # декоратор
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

greet = shout(greet)        # применяем вручную
print(greet("Иван"))        # ПРИВЕТ, ИВАН!

# С синтаксисом @ (эквивалентно):
@shout
def greet(name):
    return f"Привет, {name}!"</code></pre>

''' + tip('@decorator эквивалентно greet = decorator(greet). Это просто удобная запись.') + '''

<h2>functools.wraps — сохраняем метаданные</h2>
<pre><code>import functools

def timer(func):
    @functools.wraps(func)    # копирует __name__, __doc__ и др.
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} выполнена за {end-start:.4f}с")
        return result
    return wrapper

@timer
def slow_sum(n):
    """Суммирует числа от 0 до n."""
    return sum(range(n))

print(slow_sum(10_000_000))
print(slow_sum.__name__)  # slow_sum (не wrapper!)
print(slow_sum.__doc__)   # Суммирует числа...</code></pre>

<h2>Декоратор с параметрами</h2>
<pre><code>def repeat(times):
    """Декоратор-фабрика: выполняет функцию times раз."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say(msg):
    print(msg)

say("Привет!")  # выведет 3 раза — три уровня вложенности!</code></pre>

<h2>Декоратор для кэширования (memoize)</h2>
<pre><code>def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

print(fib(50))   # мгновенно! Без кэша — экспоненциальное время

# То же самое, но встроенное:
from functools import lru_cache

@lru_cache(maxsize=None)
def fib2(n):
    if n < 2: return n
    return fib2(n-1) + fib2(n-2)</code></pre>

<h2>Встроенные декораторы</h2>
<pre><code>class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):           # getter — доступ как к атрибуту
        return self._radius

    @radius.setter
    def radius(self, value):    # setter — с валидацией
        if value < 0:
            raise ValueError("Радиус не может быть отрицательным")
        self._radius = value

    @property
    def area(self):             # вычисляемое свойство (read-only)
        import math
        return math.pi * self._radius ** 2

    @staticmethod
    def from_diameter(d):       # не нужен ни self, ни cls
        return Circle(d / 2)

    @classmethod
    def unit(cls):              # фабричный метод
        return cls(1.0)

c = Circle(5)
print(c.area)          # 78.54...
c.radius = 10          # вызывает setter
print(Circle.unit())   # Circle(1.0)</code></pre>

<h2>Цепочка декораторов</h2>
<pre><code>@timer
@memoize
def expensive(n):
    return sum(i**2 for i in range(n))

# Эквивалентно:
# expensive = timer(memoize(expensive))
# Порядок важен: декораторы применяются снизу вверх!</code></pre>

''' + warn('Порядок декораторов снизу вверх: @timer @memoize def f → timer(memoize(f)). При цепочке декораторов думай о порядке!'),
},
]
},

{
'title': 'Регулярные выражения',
'icon': 'fas fa-search',
'order': 17,
'description': 'Шаблоны re, поиск, замена, группы, флаги. Практические примеры.',
'lessons': [
{
'title': 'Регулярные выражения: поиск и замена текста',
'order': 1,
'estimated_minutes': 85,
'content': '''
<h2>Что такое регулярные выражения?</h2>
<p>Регулярное выражение (regex) — язык описания шаблонов для поиска в тексте. Один шаблон может заменить десятки строк кода на цикл с условиями.</p>
<pre><code>import re

# Проверка e-mail вручную vs regex:
# Вручную: десятки строк кода
# Regex:
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
result = re.match(email_pattern, "user@example.com")
print(bool(result))   # True</code></pre>

''' + tip('Используй r"..." (raw string) для regex — тогда \\ не нужно экранировать как \\\\\\\\.') + '''

<h2>Специальные символы</h2>
<table class="theory-table">
<thead><tr><th>Символ</th><th>Значение</th><th>Пример</th><th>Совпадает с</th></tr></thead>
<tbody>
<tr><td>.</td><td>Любой символ кроме \\n</td><td>a.c</td><td>abc, aXc, a1c</td></tr>
<tr><td>^</td><td>Начало строки</td><td>^Hello</td><td>"Hello world"</td></tr>
<tr><td>$</td><td>Конец строки</td><td>world$</td><td>"Hello world"</td></tr>
<tr><td>*</td><td>0 и более раз</td><td>ab*c</td><td>ac, abc, abbc</td></tr>
<tr><td>+</td><td>1 и более раз</td><td>ab+c</td><td>abc, abbc (не ac)</td></tr>
<tr><td>?</td><td>0 или 1 раз</td><td>colou?r</td><td>color, colour</td></tr>
<tr><td>{n,m}</td><td>От n до m раз</td><td>\\d{2,4}</td><td>12, 123, 1234</td></tr>
<tr><td>[...]</td><td>Один из символов</td><td>[aeiou]</td><td>a, e, i, o, u</td></tr>
<tr><td>[^...]</td><td>Не один из</td><td>[^0-9]</td><td>любой не цифра</td></tr>
<tr><td>\\d</td><td>Цифра [0-9]</td><td>\\d+</td><td>42, 007</td></tr>
<tr><td>\\w</td><td>Буква/цифра/_ [a-zA-Z0-9_]</td><td>\\w+</td><td>hello, var_1</td></tr>
<tr><td>\\s</td><td>Пробельный символ</td><td>\\s+</td><td>пробел, таб</td></tr>
<tr><td>|</td><td>ИЛИ</td><td>cat|dog</td><td>cat, dog</td></tr>
<tr><td>(...)</td><td>Группа</td><td>(ab)+</td><td>ab, abab</td></tr>
</tbody></table>

<h2>Основные функции модуля re</h2>
<pre><code>import re

text = "Позвони мне 8-905-123-45-67 или 8(495)777-88-99"

# re.search — ищет первое совпадение где угодно
m = re.search(r"\\d+", text)
print(m.group())   # "8"
print(m.span())    # (15, 16) — позиция

# re.match — только с начала строки
m = re.match(r"\\d+", text)
print(m)    # None — текст начинается с буквы

# re.findall — все совпадения, список строк
phones = re.findall(r"[\\d\\-\\(\\)]{10,}", text)
print(phones)    # все телефоны

# re.sub — замена
clean = re.sub(r"[^\\d]", "", "8-905-123-45-67")
print(clean)   # "89051234567"

# re.split — разбиение по паттерну
parts = re.split(r"[,;\\s]+", "один, два;три  четыре")
print(parts)   # ["один","два","три","четыре"]</code></pre>

<h2>Группы и именованные группы</h2>
<pre><code>date_text = "Сегодня 14-05-2026, завтра 15-05-2026"

# Группы по номеру
for m in re.finditer(r"(\\d{2})-(\\d{2})-(\\d{4})", date_text):
    day, month, year = m.group(1), m.group(2), m.group(3)
    print(f"{year}/{month}/{day}")   # 2026/05/14

# Именованные группы — читаемее
pattern = r"(?P&lt;day&gt;\\d{2})-(?P&lt;month&gt;\\d{2})-(?P&lt;year&gt;\\d{4})"
for m in re.finditer(pattern, date_text):
    print(m.group("year"), m.group("month"), m.group("day"))</code></pre>

<h2>Компиляция и флаги</h2>
<pre><code># Компилируй паттерн если используешь много раз
email_re = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
    re.IGNORECASE
)

emails = ["User@Gmail.COM", "invalid-email", "test@ya.ru"]
for e in emails:
    if email_re.match(e):
        print(f"Валидный: {e}")

# Флаги:
# re.IGNORECASE (re.I)  — без учёта регистра
# re.MULTILINE  (re.M)  — ^ и $ для каждой строки
# re.DOTALL     (re.S)  — . совпадает с \\n тоже
# re.VERBOSE    (re.X)  — пробелы и комментарии в паттерне</code></pre>

''' + warn('Жадные квантификаторы (* + {}) захватывают максимум. Добавь ? для ленивого: *? +? {n,m}? — захватит минимум.'),
},
]
},

{
'title': 'Алгоритмы поиска',
'icon': 'fas fa-search-plus',
'order': 18,
'description': 'Линейный и бинарный поиск, поиск в строках, алгоритм KMP, хэш-поиск.',
'lessons': [
{
'title': 'Линейный и бинарный поиск: от O(n) до O(log n)',
'order': 1,
'estimated_minutes': 80,
'content': '''
<h2>Задача поиска</h2>
<p>Найти элемент в коллекции — одна из самых частых операций в программировании. Выбор алгоритма зависит от:</p>
<ul>
  <li>Отсортирован ли массив?</li>
  <li>Сколько раз будем искать?</li>
  <li>Какой размер данных?</li>
</ul>

<h2>Линейный поиск O(n)</h2>
<p>Перебираем элементы один за другим. Работает на любом массиве.</p>
<pre><code>def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

data = [3, 7, 1, 9, 4, 6, 8]
print(linear_search(data, 9))    # 3 (индекс)
print(linear_search(data, 5))    # -1 (не найдено)

# Анализ:
# Лучший случай:  O(1) — первый элемент
# Средний случай: O(n/2) = O(n)
# Худший случай:  O(n) — последний или отсутствует</code></pre>

<h2>Бинарный поиск O(log n)</h2>
<p>Работает только на <strong>отсортированных</strong> данных. Каждый шаг делит область поиска пополам.</p>
<pre><code>def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    steps = 0

    while left <= right:
        steps += 1
        mid = (left + right) // 2    # средний индекс

        if arr[mid] == target:
            print(f"Найдено за {steps} шагов")
            return mid
        elif arr[mid] < target:
            left = mid + 1           # ищем в правой половине
        else:
            right = mid - 1          # ищем в левой половине

    return -1

sorted_data = list(range(1, 1001))   # 1..1000
binary_search(sorted_data, 777)     # найдено за 10 шагов!
binary_search(sorted_data, 500)     # найдено за 1 шаг!</code></pre>

''' + info('log₂(1000) ≈ 10. В массиве миллион элементов потребуется не более 20 шагов. Для сравнения: линейный поиск — до 1 000 000 шагов.') + '''

<h2>Встроенный bisect</h2>
<pre><code>import bisect

data = [1, 3, 5, 7, 9, 11]
# bisect_left — позиция куда вставить слева
print(bisect.bisect_left(data, 7))    # 3
print(bisect.bisect_left(data, 6))    # 3 (место для 6)

# insort — вставляет сохраняя сортировку O(log n) поиск + O(n) вставка
bisect.insort(data, 6)
print(data)   # [1, 3, 5, 6, 7, 9, 11]</code></pre>

<h2>Рекурсивный бинарный поиск</h2>
<pre><code>def bin_search_rec(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return bin_search_rec(arr, target, mid + 1, right)
    else:
        return bin_search_rec(arr, target, left, mid - 1)</code></pre>

<h2>Сравнение алгоритмов поиска</h2>
<table class="theory-table">
<thead><tr><th>Алгоритм</th><th>Время</th><th>Требования</th><th>Python</th></tr></thead>
<tbody>
<tr><td>Линейный</td><td>O(n)</td><td>Нет</td><td>in оператор, list.index()</td></tr>
<tr><td>Бинарный</td><td>O(log n)</td><td>Отсортирован</td><td>bisect</td></tr>
<tr><td>Хэш-поиск</td><td>O(1) среднее</td><td>Хэшируемые ключи</td><td>dict, set</td></tr>
<tr><td>B-дерево</td><td>O(log n)</td><td>Индекс (БД)</td><td>sqlite индексы</td></tr>
</tbody></table>

<pre><code># Практический совет: когда что использовать
data_list = [1, 5, 3, 9, 7]   # произвольный список
data_set  = {1, 5, 3, 9, 7}   # множество

# Проверка вхождения:
5 in data_list   # O(n) — линейный перебор
5 in data_set    # O(1) — хэш-поиск!

# Если часто ищешь — конвертируй в set или dict:
lookup = set(data_list)
# Теперь "5 in lookup" — O(1)</code></pre>

''' + tip('Правило выбора: список → set для частых проверок "in". Отсортированный список → bisect для поиска. Ключ-значение → dict.'),
},
]
},
]

# ─────────────────────────────────────────────────────────────────────────────
class Command(BaseCommand):
    help = 'Добавляет SVG-диаграммы в уроки и создаёт новые модули 15-18'

    def handle(self, *args, **kwargs):
        # 1. Добавляем диаграммы в существующие уроки
        added = 0
        for title, visual_html in VISUALS.items():
            try:
                lesson = TheoryLesson.objects.get(title=title)
                if MARKER not in lesson.content:
                    lesson.content += visual_html
                    lesson.save()
                    self.stdout.write(f'  [OK] {title}')
                    added += 1
                else:
                    self.stdout.write(f'  [--] {title}')
            except TheoryLesson.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  [?] Not found: {title}'))
            except TheoryLesson.MultipleObjectsReturned:
                lesson = TheoryLesson.objects.filter(title=title).order_by('-estimated_minutes').first()
                if MARKER not in lesson.content:
                    lesson.content += visual_html
                    lesson.save()
                    self.stdout.write(f'  [OK] {title}')
                    added += 1

        self.stdout.write(f'Added diagrams: {added}')

        # 2. Создаём новые модули
        created_m = created_l = 0
        for mod_data in NEW_MODULES:
            lessons_data = mod_data.pop('lessons')
            module, m_created = TheoryModule.objects.update_or_create(
                title=mod_data['title'],
                defaults=mod_data,
            )
            if m_created:
                created_m += 1
            for lesson_data in lessons_data:
                _, l_created = TheoryLesson.objects.update_or_create(
                    module=module,
                    title=lesson_data['title'],
                    defaults={**lesson_data, 'module': module},
                )
                if l_created:
                    created_l += 1
            mod_data['lessons'] = lessons_data  # восстанавливаем

        from django.db.models import Sum, Count
        total_mins = TheoryLesson.objects.aggregate(t=Sum('estimated_minutes'))['t'] or 0
        total_lessons = TheoryLesson.objects.count()
        total_modules = TheoryModule.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'New modules: {created_m}, new lessons: {created_l}\n'
            f'Total: {total_modules} modules, {total_lessons} lessons '
            f'(~{total_mins//60}h {total_mins%60}min)'
        ))
