from django.contrib.auth import get_user_model
from django.db import models

from task.models import Task

CustomUser = get_user_model()


class Comment(models.Model):
    """Модель комментариев"""
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    reply = models.ForeignKey(
        'self',
        related_name=('replies'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ('id',)

    def __str__(self):
        return self.text
