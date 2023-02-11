from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator


# User = get_user_model()

message = ('Username содержит недопустимые символы {value}')


class UsernameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(
            RegexValidator(r'^[\w.@+-]+$', message)
        )


class User(AbstractUser):
    """Модель пользователя."""

    ADMIN = 'admin'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True, max_length=settings.EMAIL
    )
    username = UsernameField(
        verbose_name='Имя пользователя',
        help_text='Только буквы, цифры, @, +, -, _',
        max_length=settings.USERNAME,
        null=True,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max((len(role[1]) for role in ROLES)),
        choices=ROLES,
        default=USER
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username_is_not_me'
            )
        ]

    def __str__(self):
        return f'{self.username}({self.email})'


class News(models.Model):
    text = models.TextField(verbose_name='Текст новости',
                            help_text='Введите текст новости')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='news')
    image = models.ImageField('Картинка', upload_to='news/', blank=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    news = models.ForeignKey(News, verbose_name='Новость',
                             on_delete=models.CASCADE, blank=True,
                             null=True, related_name='comments',
                             help_text='Ссылка на новость, к которой оставлен '
                                       'комментарий')
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE, blank=True,
                               null=True, related_name='comments',
                               help_text='Ссылка на автора комментария')
    text = models.TextField(verbose_name='Текст комментария',
                            help_text='Введите текст комментария')
    created = models.DateTimeField(verbose_name='Дата публикации комментария',
                                   auto_now_add=True)

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


class Answer(models.Model):
    """Ответы к комментариям. Ответ привязан к определённому комментарию."""

    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE,
        max_length=settings.MAX_LEN,
        blank=True, null=True)

    text = models.TextField(verbose_name='Текст ответа',
                            help_text='Введите текст ответа')

    class Meta:
        default_related_name = 'answers'
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(verbose_name='Описание канала', blank=True,
                                   null=True)
    image = models.ImageField('Аватарка', upload_to='user/', blank=True,
                              null=True)

    def __str__(self):
        return f'{self.author.username}( {self.description[:15]})'
