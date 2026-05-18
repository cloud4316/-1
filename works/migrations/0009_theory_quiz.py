from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0008_practicalwork_language'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TheoryModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название раздела')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('icon', models.CharField(default='fas fa-book', max_length=50, verbose_name='Иконка')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Раздел теории', 'verbose_name_plural': 'Разделы теории', 'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='TheoryLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название урока')),
                ('content', models.TextField(verbose_name='Содержание (HTML)')),
                ('code_example', models.TextField(blank=True, verbose_name='Пример кода')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('estimated_minutes', models.PositiveIntegerField(default=10, verbose_name='Время (мин)')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='works.theorymodule', verbose_name='Раздел')),
            ],
            options={'verbose_name': 'Урок теории', 'verbose_name_plural': 'Уроки теории', 'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='LessonProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='works.theorylesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Прогресс по уроку', 'verbose_name_plural': 'Прогресс по урокам', 'unique_together': {('user', 'lesson')}},
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название теста')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('pass_score', models.PositiveIntegerField(default=70, verbose_name='Проходной балл (%)')),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizzes', to='works.theorymodule', verbose_name='Раздел теории')),
            ],
            options={'verbose_name': 'Тест', 'verbose_name_plural': 'Тесты', 'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст вопроса')),
                ('code_snippet', models.TextField(blank=True, verbose_name='Код')),
                ('q_type', models.CharField(choices=[('single', 'Один правильный ответ'), ('multiple', 'Несколько правильных ответов'), ('code', 'Вопрос по коду')], default='single', max_length=10, verbose_name='Тип вопроса')),
                ('order', models.PositiveIntegerField(default=0)),
                ('explanation', models.TextField(blank=True, verbose_name='Пояснение к ответу')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='works.quiz', verbose_name='Тест')),
            ],
            options={'ordering': ['order'], 'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
        migrations.CreateModel(
            name='AnswerChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Текст варианта')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильный')),
                ('order', models.PositiveIntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='works.question', verbose_name='Вопрос')),
            ],
            options={'ordering': ['order'], 'verbose_name': 'Вариант ответа', 'verbose_name_plural': 'Варианты ответов'},
        ),
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0, verbose_name='Баллы (%)')),
                ('passed', models.BooleanField(default=False, verbose_name='Пройден')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answers', models.JSONField(default=dict, verbose_name='Ответы пользователя')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='works.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Попытка теста', 'verbose_name_plural': 'Попытки тестов', 'ordering': ['-created_at']},
        ),
    ]
