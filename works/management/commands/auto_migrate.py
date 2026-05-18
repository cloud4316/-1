from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
	help = 'Автоматически создает и применяет миграции'

	def handle(self, *args, **options):
		call_command('makemigrations', interactive=False)
		call_command('migrate', interactive=False)
		self.stdout.write(self.style.SUCCESS('Миграции применены!'))
