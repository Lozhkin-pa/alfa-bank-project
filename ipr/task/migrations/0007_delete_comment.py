# Generated by Django 4.2 on 2024-01-23 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_alter_task_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
