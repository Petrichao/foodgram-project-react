from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_fail'),
            models.CheckConstraint(check=~models.Q(user=models.F('author')),
                                   name="follow_to_yourrself")
        ]
        verbose_name = ('Подписку на автора')
        verbose_name_plural = ('Подписки на авторов')
        ordering = ('user',)

    def __str__(self):
        user = self.user
        return user.username