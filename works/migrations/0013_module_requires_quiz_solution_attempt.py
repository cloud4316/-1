from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("works", "0012_solution_indexes")]
    operations = [
        migrations.AddField(
            model_name="theorymodule",
            name="requires_quiz_pass",
            field=models.BooleanField(default=False, verbose_name="Требует сдачи предыдущего теста"),
        ),
        migrations.AddField(
            model_name="solution",
            name="attempt_number",
            field=models.PositiveIntegerField(default=1, verbose_name="Номер попытки"),
        ),
    ]
