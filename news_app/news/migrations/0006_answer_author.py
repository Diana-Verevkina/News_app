# Generated by Django 3.2.17 on 2023-02-11 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_alter_comment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(blank=True, help_text='Ссылка на автора ответа', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
