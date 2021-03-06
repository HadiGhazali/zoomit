# Generated by Django 3.1.4 on 2020-12-30 11:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20201230_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='color',
        ),
        migrations.AddField(
            model_name='category',
            name='main_category',
            field=models.CharField(blank=True, choices=[('تکنولوژی', 'تکنولوژی'), ('خودرو', 'خودرو'), ('علمی', 'علمی')], max_length=10, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 12, 30, 11, 14, 49, 206543, tzinfo=utc), verbose_name='Publish at'),
        ),
    ]
