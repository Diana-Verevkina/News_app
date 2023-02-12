# Generated by Django 3.2.17 on 2023-02-12 16:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата публикации комментария'),
        ),
        migrations.AlterField(
            model_name='news',
            name='pub_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата публикации'),
        ),
    ]
