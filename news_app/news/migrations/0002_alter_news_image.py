# Generated by Django 3.2.17 on 2023-02-11 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.TextField(blank=True, verbose_name='Картинка'),
        ),
    ]