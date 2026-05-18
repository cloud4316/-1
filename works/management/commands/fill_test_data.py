from django.core.management.base import BaseCommand
from works.models import UserProgress
from django.contrib.auth.models import User


class Command(BaseCommand):
	help = 'Заполняет тестовыми данными профиль пользователя'

	def handle(self, *args, **options):
		user = User.objects.first()
		if not user:
			self.stdout.write(self.style.ERROR('Пользователи не найдены'))
			return

		progress, _ = UserProgress.objects.get_or_create(user=user)
		progress.total_score = 150
		progress.completed_works = 8
		progress.streak_days = 5
		progress.level = 2
		progress.current_xp = 75
		progress.next_level_xp = 100
		progress.save()

		self.stdout.write(self.style.SUCCESS(f'Тестовые данные установлены для {user.username}'))
