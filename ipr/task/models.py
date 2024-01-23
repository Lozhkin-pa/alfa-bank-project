from django.contrib.auth import get_user_model
from django.db import models

CustomUser = get_user_model()

STATUS_CHOICE = [
        ('none', 'Отсутствует'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнен'),
        ('not_done', 'Не выполнен'),
        ('canceled', 'Отменен'),
    ]


class Task(models.Model):
    """Модель задач"""
    title = models.CharField(
        max_length=200,
        verbose_name="Название"
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default='none',
        verbose_name='Статус'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author_tasks'
    )
    # ipr = models.ForeignKey(
    #     Ipr,
    #     on_delete=models.CASCADE,
    #     verbose_name='ИПР',
    #     related_name='tasks_ipr'
    # )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    deadline = models.DateField(
        verbose_name='Дедлайн',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('-author',)

    def __str__(self):
        return self.title
