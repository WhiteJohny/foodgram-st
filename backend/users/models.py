from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    EMAIL_MAX_LENGTH = 254
    INFO_MAX_LENGTH = 40

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        help_text='Укажите ваш email'
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=INFO_MAX_LENGTH,
        unique=True,
        help_text='Укажите ваш username пользователя'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=INFO_MAX_LENGTH,
        blank=False,
        help_text='Укажите ваше имя'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=INFO_MAX_LENGTH,
        blank=False,
        help_text='Укажите вашу фамилию'
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='avatars/',
        default='',
        help_text='Загрузите ваш аватар'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return self.email


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'author'
                ],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='no_self_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user} → {self.author}'
