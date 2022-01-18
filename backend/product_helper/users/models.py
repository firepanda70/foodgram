from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscribtion(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписки',
        on_delete=models.CASCADE,
        related_name='subsctiptions',
        help_text='Подписки пользователя'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='followers',
        help_text='Подписчики автора'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription'
                ),
        )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        res = 'Подписка {user} на {author}'
        return res.format(user=self.user.username,
                          author=self.author.username)
