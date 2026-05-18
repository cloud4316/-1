from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("works", "0011_notification_teachercomment")]
    operations = [
        migrations.AlterField(
            model_name="solution",
            name="status",
            field=models.CharField(db_index=True, default="submitted", max_length=20),
        ),
        migrations.AlterField(
            model_name="solution",
            name="submitted_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
