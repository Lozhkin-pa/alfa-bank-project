# Generated by Django 4.2 on 2024-02-02 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iprs', '0008_ipr_start_date_alter_ipr_end_date_alter_ipr_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply',
        ),
    ]
