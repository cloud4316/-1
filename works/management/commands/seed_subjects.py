"""Создать предметы Python и МК, привязать существующий контент к Python."""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, PracticalWork


SUBJECTS = [
    {
        'slug': 'python',
        'title': 'Программирование на Python',
        'icon': 'fab fa-python',
        'color': '#667eea',
        'order': 1,
        'description': 'Основы алгоритмизации и программирования на Python: '
                       'переменные, циклы, функции, структуры данных, алгоритмы сортировки и поиска.',
    },
    {
        'slug': 'mcu',
        'title': 'Микроконтроллеры',
        'icon': 'fas fa-microchip',
        'color': '#10b981',
        'order': 2,
        'description': 'Программирование микроконтроллеров Arduino и ESP32: '
                       'GPIO, ШИМ, датчики, I2C/SPI, прерывания, Tinkercad-симуляция.',
    },
]


class Command(BaseCommand):
    help = 'Создать предметы и привязать существующий контент к Python'

    def handle(self, *args, **options):
        for data in SUBJECTS:
            subj, created = Subject.objects.update_or_create(
                slug=data['slug'], defaults=data
            )
            action = 'Создан' if created else 'Обновлён'
            self.stdout.write(f'{action}: {subj.title}')

        python_subj = Subject.objects.get(slug='python')

        # Привязываем все модули теории без предмета к Python
        updated = TheoryModule.objects.filter(subject__isnull=True).update(subject=python_subj)
        self.stdout.write(f'Привязано к Python: {updated} модулей теории')

        updated_works = PracticalWork.objects.filter(subject__isnull=True).update(subject=python_subj)
        self.stdout.write(f'Привязано к Python: {updated_works} практических работ')

        self.stdout.write(self.style.SUCCESS('Предметы готовы!'))
