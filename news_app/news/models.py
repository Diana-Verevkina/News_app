from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes',
                             on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class News(models.Model):
    text = models.TextField(verbose_name='Текст новости',
                            help_text='Введите текст новости')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='news')
    # image = models.TextField('Картинка', blank=True)
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    likes = GenericRelation(Like)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.text[:15]

    @property
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    news = models.ForeignKey(News, verbose_name='Новость',
                             on_delete=models.CASCADE, blank=True,
                             null=True, related_name='comments',
                             help_text='Ссылка на новость, к которой оставлен '
                                       'комментарий')
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE, blank=True,
                               null=True, related_name='comments_author',
                               help_text='Ссылка на автора комментария')
    text = models.TextField(verbose_name='Текст комментария',
                            help_text='Введите текст комментария')
    created = models.DateTimeField(verbose_name='Дата публикации комментария',
                               auto_now_add=True)
    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               on_delete=models.CASCADE,
                               related_name='children',
                               verbose_name='parent_comment')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE, blank=True,
                             null=True, related_name='follower',
                             help_text='Ссылка на объект пользователя, '
                                       'который подписывается')
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE, blank=True,
                               null=True, related_name='following',
                               help_text='Ссылка на объект пользователя, '
                                         'на которого подписываются')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.author.username


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, verbose_name='Имя',
                                  blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия',
                                 blank=True, null=True)
    birth_year = models.PositiveSmallIntegerField(verbose_name='Год рождения',
                                                  db_index=True, blank=True,
                                                  null=True)
    description = models.TextField(verbose_name='Описание канала', blank=True,
                                   null=True)
    image = models.ImageField(upload_to='users/', null=True, blank=True)

    def __str__(self):
        return f'{self.author.username}( {self.description[:15]})'
