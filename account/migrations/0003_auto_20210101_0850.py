# Generated by Django 3.1.4 on 2021-01-01 08:50

import account.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201214_2258'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', account.models.UserManager()),
            ],
        ),
    ]
