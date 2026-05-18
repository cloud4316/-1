"""
Создаёт администратора admin/admin если его ещё нет.
Запуск: python manage.py create_default_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Создаёт администратора admin/admin (если не существует)'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write('  Администратор admin уже существует — пропускаем')
            return

        # first_name и last_name = 'admin', чтобы вход "admin admin" работал
        User.objects.create_superuser(
            username='admin',
            password='admin',
            first_name='admin',
            last_name='admin',
            email='',
        )
        self.stdout.write(self.style.SUCCESS(
            'OK Создан администратор:\n'
            '   Поле входа  : admin admin  (Фамилия Имя через пробел)\n'
            '   Пароль      : admin\n'
            '   Смените пароль: /admin/ -> Пользователи -> admin'
        ))
