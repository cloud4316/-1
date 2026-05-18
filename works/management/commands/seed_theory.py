"""
Загружает теоретический материал из theory_data.json.
Запуск: python manage.py seed_theory
"""
import json
import os
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson


class Command(BaseCommand):
    help = 'Заполняет базу теорией (72 академических часа)'

    def handle(self, *args, **options):
        json_path = os.path.join(os.path.dirname(__file__), 'theory_data.json')
        with open(json_path, encoding='utf-8') as f:
            modules_data = json.load(f)

        created_m = created_l = 0

        for mod_data in modules_data:
            lessons = mod_data.pop('lessons')
            module, mc = TheoryModule.objects.update_or_create(
                title=mod_data['title'],
                defaults=mod_data,
            )
            if mc:
                created_m += 1

            for les_data in lessons:
                _, lc = TheoryLesson.objects.update_or_create(
                    module=module,
                    title=les_data['title'],
                    defaults=les_data,
                )
                if lc:
                    created_l += 1

        total_min = sum(
            TheoryLesson.objects.filter(module__title=m['title'])
                .values_list('estimated_minutes', flat=True)
            for m in TheoryModule.objects.values('title')
        ) if False else 0

        from django.db.models import Sum
        total_min = TheoryLesson.objects.aggregate(t=Sum('estimated_minutes'))['t'] or 0

        self.stdout.write(self.style.SUCCESS(
            f'OK  Модулей: {TheoryModule.objects.count()}, '
            f'Уроков: {TheoryLesson.objects.count()} '
            f'(~{total_min // 60}ч {total_min % 60}мин)'
        ))
