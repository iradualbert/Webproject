# Generated by Django 3.0.2 on 2020-03-22 21:57

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_auto_20200322_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 22, 21, 57, 26, 45236)),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 22, 21, 57, 26, 46234, tzinfo=utc)),
        ),
    ]
