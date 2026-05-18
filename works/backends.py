"""
Кастомный бэкенд авторизации.
Позволяет входить по "Фамилия Имя" (например: Иванов Иван).
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class FullNameBackend(ModelBackend):
    """
    Авторизация по полному имени в формате «Фамилия Имя» или «Имя Фамилия».
    Пароль проверяется стандартно.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        full_name = username.strip()
        user = self._find_user(full_name)
        if user is None:
            return None

        if not user.check_password(password):
            return None

        # Не проверяем is_active здесь — пусть проверяет can_authenticate,
        # но мы хотим вернуть объект даже для неактивных, чтобы views.py
        # показал правильное сообщение (а не просто «неверный логин»).
        return user

    def _find_user(self, full_name):
        """
        Ищет пользователя по «Фамилия Имя» или «Имя Фамилия».
        Поиск регистронезависимый.
        """
        parts = full_name.split()
        if len(parts) < 2:
            return None

        last, first = parts[0], parts[1]

        # Вариант 1: Фамилия Имя
        user = User.objects.filter(
            last_name__iexact=last,
            first_name__iexact=first
        ).first()
        if user:
            return user

        # Вариант 2: Имя Фамилия
        user = User.objects.filter(
            first_name__iexact=last,
            last_name__iexact=first
        ).first()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
