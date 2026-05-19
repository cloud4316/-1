from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
import uuid
import os

# ══════════════════════════════════════════════════════════════════════════════
# ПРЕДМЕТЫ
# ══════════════════════════════════════════════════════════════════════════════

class Subject(models.Model):
    slug        = models.SlugField(unique=True, max_length=20, verbose_name='Slug')
    title       = models.CharField(max_length=100, verbose_name='Название')
    icon        = models.CharField(max_length=50, default='fas fa-book', verbose_name='Иконка')
    color       = models.CharField(max_length=20, default='#667eea', verbose_name='Цвет')
    description = models.TextField(blank=True, verbose_name='Описание')
    order       = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')
    is_active   = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        ordering = ['order']
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.title


# ══════════════════════════════════════════════════════════════════════════════
# ОБЪЯВЛЕНИЯ
# ══════════════════════════════════════════════════════════════════════════════

class Announcement(models.Model):
    author     = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='announcements', verbose_name='Автор')
    subject    = models.ForeignKey('Subject', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='Предмет (пусто = все)')
    title      = models.CharField(max_length=200, verbose_name='Заголовок')
    body       = models.TextField(blank=True, verbose_name='Текст')
    is_active  = models.BooleanField(default=True, verbose_name='Активно')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Скрыть с даты')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return bool(self.expires_at and timezone.now() > self.expires_at)


class PracticalWork(models.Model):
    TOPIC_CHOICES = [
        ('search', 'Алгоритмы поиска'),
        ('sorting', 'Сортировка'),
        ('data_structures', 'Структуры данных'),
        ('recursion', 'Рекурсия'),
        ('other', 'Другое'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкая'),
        ('medium', 'Средняя'),
        ('hard', 'Сложная'),
    ]
    
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('c', 'C'),
        ('javascript', 'JavaScript'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название работы")
    description = models.TextField(verbose_name="Описание задания")
    theory_text = models.TextField(verbose_name="Теоретический материал", blank=True)
    input_example = models.TextField(verbose_name="Пример входных данных", blank=True)
    output_example = models.TextField(verbose_name="Пример выходных данных", blank=True)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES, default='other', verbose_name="Тема")
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python', verbose_name="Язык программирования")
    is_active = models.BooleanField(default=True, verbose_name="Доступна для сдачи")
    order = models.IntegerField(default=0, verbose_name="Порядковый номер")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium', verbose_name="Сложность")
    deadline      = models.DateTimeField(null=True, blank=True, verbose_name="Срок сдачи")
    subject       = models.ForeignKey('Subject', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='works', verbose_name='Предмет')
    tinkercad_url = models.URLField(blank=True, verbose_name='Ссылка Tinkercad (для МК)')
    max_score = models.IntegerField(default=10, verbose_name="Максимальный балл")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Практическая работа"
        verbose_name_plural = "Практические работы"
        ordering = ['order']


def solution_upload_path(instance, filename):
    # сохраняем исходное имя отдельно, файл кладём по UUID
    ext = os.path.splitext(filename)[1].lower()
    return os.path.join('solutions', timezone.now().strftime('%Y/%m/%d'), f"{uuid.uuid4()}{ext}")

class Solution(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Отправлено'),
        ('checking', 'Проверяется'),
        ('correct', 'Верно'),
        ('incorrect', 'Есть ошибки'),
        ('partially_correct', 'Частично верно'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    work = models.ForeignKey(PracticalWork, on_delete=models.CASCADE, verbose_name="Работа")
    original_filename = models.CharField(max_length=255, blank=True, verbose_name="Оригинальное имя файла")
    code_file = models.FileField(upload_to=solution_upload_path, verbose_name="Файл с решением")
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата отправки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted', verbose_name="Статус")
    score = models.IntegerField(default=0, verbose_name="Баллы")
    execution_time = models.FloatField(null=True, blank=True, verbose_name="Время выполнения")
    memory_usage = models.FloatField(null=True, blank=True, verbose_name="Использование памяти")
    comment = models.TextField(blank=True, verbose_name="Комментарий проверяющего")
    test_results = models.JSONField(default=dict, verbose_name="Результаты тестов")
    compile_log = models.TextField(blank=True, verbose_name="Лог компиляции")
    run_log = models.TextField(blank=True, verbose_name="Лог выполнения")
    verdict_text = models.TextField(blank=True, verbose_name="Вердикт")
    attempt_number = models.PositiveIntegerField(default=1, verbose_name="Номер попытки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return f"Решение {self.student.username} для {self.work.title}"

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = "Решения"
        ordering = ['-submitted_at']

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    total_works = models.IntegerField(default=0, verbose_name="Всего работ")
    completed_works = models.IntegerField(default=0, verbose_name="Выполнено работ")
    total_score = models.IntegerField(default=0, verbose_name="Общий балл")
    average_score = models.FloatField(default=0, verbose_name="Средний балл")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="Последняя активность")
    group       = models.CharField(max_length=20, blank=True, default="", verbose_name="Группа")
    streak_days = models.IntegerField(default=0, verbose_name="Дней подряд")
    level = models.IntegerField(default=1, verbose_name="Уровень")
    current_xp = models.IntegerField(default=0, verbose_name="Текущий опыт")
    next_level_xp = models.IntegerField(default=100, verbose_name="Опыт до след. уровня")

    @property
    def completion_percentage(self):
        if self.total_works > 0:
            return round((self.completed_works / self.total_works) * 100)
        return 0
    
    @property
    def level_progress(self):
        if self.next_level_xp > 0:
            return round((self.current_xp / self.next_level_xp) * 100)
        return 0

    def __str__(self):
        return f"Прогресс {self.user.username}"

    class Meta:
        verbose_name = "Прогресс пользователя"
        verbose_name_plural = "Прогресс пользователей"


class UserSession(models.Model):
    """Модель для отслеживания времени, проведенного пользователем на сайте"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    session_key = models.CharField(max_length=40, verbose_name="Ключ сессии")
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Время окончания")
    duration_seconds = models.IntegerField(default=0, verbose_name="Длительность в секундах")
    page_views = models.IntegerField(default=0, verbose_name="Количество просмотров страниц")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    
    @property
    def duration_minutes(self):
        return round(self.duration_seconds / 60, 1)
    
    @property
    def duration_hours(self):
        return round(self.duration_seconds / 3600, 2)
    
    def __str__(self):
        return f"Сессия {self.user.username} - {self.duration_minutes} мин"
    
    class Meta:
        verbose_name = "Сессия пользователя"
        verbose_name_plural = "Сессии пользователей"
        ordering = ['-start_time']


class PageView(models.Model):
    """Модель для отслеживания просмотров страниц"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, verbose_name="Сессия")
    page_url = models.CharField(max_length=500, verbose_name="URL страницы")
    page_title = models.CharField(max_length=200, verbose_name="Название страницы")
    view_time = models.DateTimeField(auto_now_add=True, verbose_name="Время просмотра")
    time_spent = models.IntegerField(default=0, verbose_name="Время на странице (сек)")
    
    def __str__(self):
        return f"{self.user.username} - {self.page_title}"
    
    class Meta:
        verbose_name = "Просмотр страницы"
        verbose_name_plural = "Просмотры страниц"


class CodeCheck(models.Model):
    """Модель для автоматической проверки кода"""
    STATUS_CHOICES = (
        ('pending', 'Ожидает проверки'),
        ('in_progress', 'Проверяется'),
        ('completed', 'Проверка завершена'),
        ('failed', 'Ошибка проверки'),
    )
    
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, verbose_name="Решение")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    score = models.IntegerField(default=0, verbose_name="Оценка")
    feedback = models.TextField(blank=True, verbose_name="Обратная связь")
    suggestions = models.JSONField(default=list, verbose_name="Предложения по улучшению")
    errors = models.JSONField(default=list, verbose_name="Найденные ошибки")
    warnings = models.JSONField(default=list, verbose_name="Предупреждения")
    check_type = models.CharField(max_length=50, default='comprehensive', verbose_name="Тип проверки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершено")
    
    def __str__(self):
        return f"Проверка кода для {self.solution}"
    
    class Meta:
        verbose_name = "Проверка кода"
        verbose_name_plural = "Проверки кода"
        ordering = ['-created_at']

# ══════════════════════════════════════════════════════════════════════════════
# ТЕОРИЯ
# ══════════════════════════════════════════════════════════════════════════════

class TheoryModule(models.Model):
    """Раздел теории (напр. 'Переменные и типы данных')"""
    ICON_CHOICES = [
        ('fas fa-variable', 'Переменные'), ('fas fa-code-branch', 'Ветвление'),
        ('fas fa-sync', 'Циклы'), ('fas fa-function', 'Функции'),
        ('fas fa-list', 'Списки'), ('fas fa-book', 'Общее'),
        ('fas fa-file-alt', 'Файлы'), ('fas fa-cubes', 'ООП'),
        ('fas fa-sort', 'Сортировка'), ('fas fa-redo', 'Рекурсия'),
        ('fas fa-keyboard', 'Ввод/Вывод'), ('fas fa-calculator', 'Арифметика'),
    ]
    title       = models.CharField(max_length=200, verbose_name='Название раздела')
    description = models.TextField(blank=True, verbose_name='Описание')
    icon        = models.CharField(max_length=50, default='fas fa-book', verbose_name='Иконка')
    order       = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active          = models.BooleanField(default=True)
    requires_quiz_pass = models.BooleanField(default=False, verbose_name='Требует сдачи предыдущего теста')
    subject     = models.ForeignKey('Subject', null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='modules', verbose_name='Предмет')

    class Meta:
        verbose_name = 'Раздел теории'
        verbose_name_plural = 'Разделы теории'
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def lessons_count(self):
        return self.lessons.count()


class TheoryLesson(models.Model):
    """Отдельный урок внутри раздела"""
    module            = models.ForeignKey(TheoryModule, on_delete=models.CASCADE,
                                          related_name='lessons', verbose_name='Раздел')
    title             = models.CharField(max_length=200, verbose_name='Название урока')
    content           = models.TextField(verbose_name='Содержание (HTML)')
    code_example      = models.TextField(blank=True, verbose_name='Пример кода')
    order             = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    estimated_minutes = models.PositiveIntegerField(default=10, verbose_name='Время (мин)')

    class Meta:
        verbose_name = 'Урок теории'
        verbose_name_plural = 'Уроки теории'
        ordering = ['order']

    def __str__(self):
        return f'{self.module.title} → {self.title}'


# ══════════════════════════════════════════════════════════════════════════════
# КОНСТРУКТОР СХЕМ
# ══════════════════════════════════════════════════════════════════════════════

class CircuitDraft(models.Model):
    """Черновик схемы — сохраняется автоматически при работе студента."""
    student    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='circuit_drafts')
    work       = models.ForeignKey('PracticalWork', on_delete=models.CASCADE,
                                   related_name='circuit_drafts')
    circuit_json = models.TextField(default='{}', verbose_name='JSON схемы')
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'work')
        verbose_name = 'Черновик схемы'
        verbose_name_plural = 'Черновики схем'

    def __str__(self):
        return f'{self.student} / {self.work}'


class CircuitSolution(models.Model):
    """Сданная схема как решение практической работы."""
    STATUS_CHOICES = [
        ('submitted',  'Сдано'),
        ('reviewed',   'Проверено'),
        ('correct',    'Зачтено'),
        ('incorrect',  'Не зачтено'),
    ]
    student      = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='circuit_solutions')
    work         = models.ForeignKey('PracticalWork', on_delete=models.CASCADE,
                                     related_name='circuit_solutions')
    circuit_json = models.TextField(verbose_name='JSON схемы')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    score        = models.IntegerField(default=0, verbose_name='Балл')
    comment      = models.TextField(blank=True, verbose_name='Комментарий студента')
    teacher_comment = models.TextField(blank=True, verbose_name='Комментарий преподавателя')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at  = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Решение схемы'
        verbose_name_plural = 'Решения схем'

    def __str__(self):
        return f'{self.student} / {self.work} — {self.get_status_display()}'


class LessonProgress(models.Model):
    """Отметка о прочитанном уроке + конспект"""
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson     = models.ForeignKey(TheoryLesson, on_delete=models.CASCADE)
    completed  = models.BooleanField(default=False)
    notes      = models.TextField(blank=True, verbose_name='Конспект')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = 'Прогресс по уроку'
        verbose_name_plural = 'Прогресс по урокам'


# ══════════════════════════════════════════════════════════════════════════════
# ТЕСТЫ / КВИЗЫ
# ══════════════════════════════════════════════════════════════════════════════

class Quiz(models.Model):
    """Мини-тест (привязан к разделу теории или существует сам по себе)"""
    module      = models.ForeignKey(TheoryModule, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='quizzes',
                                    verbose_name='Раздел теории')
    title       = models.CharField(max_length=200, verbose_name='Название теста')
    description = models.TextField(blank=True, verbose_name='Описание')
    pass_score  = models.PositiveIntegerField(default=70, verbose_name='Проходной балл (%)')
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def questions_count(self):
        return self.questions.count()


class Question(models.Model):
    TYPE_SINGLE   = 'single'
    TYPE_MULTIPLE = 'multiple'
    TYPE_CODE     = 'code'
    TYPE_CHOICES  = [
        (TYPE_SINGLE,   'Один правильный ответ'),
        (TYPE_MULTIPLE, 'Несколько правильных ответов'),
        (TYPE_CODE,     'Вопрос по коду'),
    ]
    quiz        = models.ForeignKey(Quiz, on_delete=models.CASCADE,
                                    related_name='questions', verbose_name='Тест')
    text        = models.TextField(verbose_name='Текст вопроса')
    code_snippet= models.TextField(blank=True, verbose_name='Код (если нужен)')
    q_type      = models.CharField(max_length=10, choices=TYPE_CHOICES,
                                   default=TYPE_SINGLE, verbose_name='Тип вопроса')
    order       = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True, verbose_name='Пояснение к ответу')

    class Meta:
        ordering = ['order']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'[{self.quiz.title}] {self.text[:60]}'


class AnswerChoice(models.Model):
    question   = models.ForeignKey(Question, on_delete=models.CASCADE,
                                   related_name='choices', verbose_name='Вопрос')
    text       = models.CharField(max_length=500, verbose_name='Текст варианта')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный')
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return f'{"✓" if self.is_correct else "✗"} {self.text[:50]}'


class QuizAttempt(models.Model):
    """Одна попытка прохождения теста пользователем"""
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz       = models.ForeignKey(Quiz, on_delete=models.CASCADE,
                                   related_name='attempts')
    score      = models.PositiveIntegerField(default=0, verbose_name='Баллы (%)')
    passed     = models.BooleanField(default=False, verbose_name='Пройден')
    created_at = models.DateTimeField(auto_now_add=True)
    answers    = models.JSONField(default=dict, verbose_name='Ответы пользователя')

    class Meta:
        verbose_name = 'Попытка теста'
        verbose_name_plural = 'Попытки тестов'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} → {self.quiz.title} ({self.score}%)'


# ══════════════════════════════════════════════════════════════════════════════
# УВЕДОМЛЕНИЯ
# ══════════════════════════════════════════════════════════════════════════════

class Notification(models.Model):
    TYPE_CHOICES = [
        ('approved',   'Регистрация одобрена'),
        ('graded',     'Работа проверена'),
        ('commented',  'Новый комментарий'),
        ('deadline',   'Скоро дедлайн'),
        ('info',       'Информация'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='notifications')
    n_type     = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    title      = models.CharField(max_length=200)
    message    = models.TextField(blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link       = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'{self.user.last_name}: {self.title}'

    @classmethod
    def send(cls, user, n_type, title, message='', link=''):
        return cls.objects.create(
            user=user, n_type=n_type,
            title=title, message=message, link=link
        )


# ══════════════════════════════════════════════════════════════════════════════
# КОММЕНТАРИИ ПРЕПОДАВАТЕЛЯ К РЕШЕНИЯМ
# ══════════════════════════════════════════════════════════════════════════════

class TeacherComment(models.Model):
    solution   = models.ForeignKey(Solution, on_delete=models.CASCADE,
                                   related_name='teacher_comments')
    teacher    = models.ForeignKey(User, on_delete=models.CASCADE)
    text       = models.TextField(verbose_name='Комментарий')
    score      = models.PositiveIntegerField(null=True, blank=True,
                                              verbose_name='Оценка (0-100)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий преподавателя'
        verbose_name_plural = 'Комментарии преподавателя'

    def __str__(self):
        return f'{self.teacher.last_name} → {self.solution}'


# ══════════════════════════════════════════════════════════════════════════════
# ДОСТИЖЕНИЯ
# ══════════════════════════════════════════════════════════════════════════════

class Achievement(models.Model):
    ICON_CHOICES = [
        ('⭐', 'Звезда'), ('🔥', 'Огонь'), ('🏆', 'Трофей'),
        ('📚', 'Книга'), ('💻', 'Код'), ('🎯', 'Цель'),
        ('🚀', 'Ракета'), ('🧠', 'Мозг'), ('⚡', 'Молния'),
    ]
    key         = models.CharField(max_length=50, unique=True, verbose_name='Ключ')
    title       = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    icon        = models.CharField(max_length=4, default='⭐', verbose_name='Иконка')
    xp_reward   = models.PositiveIntegerField(default=0, verbose_name='Награда XP')

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

    def __str__(self):
        return f'{self.icon} {self.title}'


class UserAchievement(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='achievements', verbose_name='Пользователь')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE,
                                    verbose_name='Достижение')
    earned_at   = models.DateTimeField(auto_now_add=True, verbose_name='Получено')

    class Meta:
        unique_together = ('user', 'achievement')
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'
        ordering = ['-earned_at']

    def __str__(self):
        return f'{self.user.last_name}: {self.achievement.title}'


# ══════════════════════════════════════════════════════════════════════════════
# ПОДСКАЗКИ К ЗАДАНИЯМ
# ══════════════════════════════════════════════════════════════════════════════

class WorkHint(models.Model):
    work     = models.ForeignKey(PracticalWork, on_delete=models.CASCADE,
                                 related_name='hints', verbose_name='Работа')
    order    = models.PositiveSmallIntegerField(default=1, verbose_name='Порядок')
    title    = models.CharField(max_length=100, default='Подсказка', verbose_name='Заголовок')
    text     = models.TextField(verbose_name='Текст подсказки')
    xp_cost  = models.PositiveIntegerField(default=5, verbose_name='Стоимость (XP)')

    class Meta:
        ordering = ['order']
        verbose_name = 'Подсказка'
        verbose_name_plural = 'Подсказки'

    def __str__(self):
        return f'[{self.work.title}] Подсказка {self.order}'


class UserHintUnlock(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    hint        = models.ForeignKey(WorkHint, on_delete=models.CASCADE, verbose_name='Подсказка')
    unlocked_at = models.DateTimeField(auto_now_add=True, verbose_name='Открыто')

    class Meta:
        unique_together = ('user', 'hint')
        verbose_name = 'Открытая подсказка'
        verbose_name_plural = 'Открытые подсказки'


# ══════════════════════════════════════════════════════════════════════════════
# ПРОДЛЕНИЕ ДЕДЛАЙНА
# ══════════════════════════════════════════════════════════════════════════════

class DeadlineExtension(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Ожидает'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]
    user         = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='deadline_extensions', verbose_name='Студент')
    work         = models.ForeignKey(PracticalWork, on_delete=models.CASCADE,
                                     verbose_name='Работа')
    reason       = models.TextField(verbose_name='Причина')
    new_deadline = models.DateTimeField(null=True, blank=True, verbose_name='Новый дедлайн')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                    default='pending', verbose_name='Статус')
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name='Запрошено')
    reviewed_at  = models.DateTimeField(null=True, blank=True, verbose_name='Рассмотрено')

    class Meta:
        unique_together = ('user', 'work')
        verbose_name = 'Запрос продления дедлайна'
        verbose_name_plural = 'Запросы продления дедлайна'
        ordering = ['-requested_at']

    def __str__(self):
        return f'{self.user.last_name} → {self.work.title} ({self.get_status_display()})'
