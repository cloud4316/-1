from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('works', '0010_userprogress_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('n_type', models.CharField(choices=[('approved','Регистрация одобрена'),('graded','Работа проверена'),('commented','Новый комментарий'),('deadline','Скоро дедлайн'),('info','Информация')], default='info', max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField(blank=True)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('link', models.CharField(blank=True, max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at'], 'verbose_name': 'Уведомление'},
        ),
        migrations.CreateModel(
            name='TeacherComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('score', models.PositiveIntegerField(blank=True, null=True, verbose_name='Оценка (0-100)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_comments', to='works.solution')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at'], 'verbose_name': 'Комментарий преподавателя'},
        ),
    ]
