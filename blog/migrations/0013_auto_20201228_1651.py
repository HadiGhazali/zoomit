# Generated by Django 3.1.4 on 2020-12-28 16:51

import ckeditor.fields
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20201228_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 12, 28, 16, 51, 4, 543181, tzinfo=utc), verbose_name='Publish at'),
        ),
    ]
