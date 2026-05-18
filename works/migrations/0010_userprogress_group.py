from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('works', '0009_theory_quiz')]
    operations = [
        migrations.AddField(
            model_name='userprogress',
            name='group',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Группа'),
        ),
    ]
