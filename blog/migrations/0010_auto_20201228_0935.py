# Generated by Django 3.1.4 on 2020-12-28 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20201228_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlhit',
            name='daily_hits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='urlhit',
            name='url',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
