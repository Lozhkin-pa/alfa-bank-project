# Generated by Django 4.2 on 2024-01-23 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0005_alter_task_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
