from django.db import models
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


class Ipr(models.Model):
    NOT_STARTED = 'Not started'
    IN_PROGRESS = 'In progress'
    DONE = 'Done'
    CANCELED = 'Canceled'
    NO_STATUS = 'No status'
    STATUS_CHOICES = (
        (NOT_STARTED, 'Не начат'),
        (IN_PROGRESS, 'В работе'),
        (DONE, 'Выполнен'),
        (CANCELED, 'Отменен'),
        (NO_STATUS, 'Отсутствует'),
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название ИПР',
    )
    employee = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='ipr_employee',
        verbose_name='Сотрудник'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ipr_author',
        verbose_name='Автор ИПР'
    )
    description = models.TextField(
        max_length=200,
        verbose_name='Описание ИПР',
    )
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default=NO_STATUS,
        verbose_name='Статус ИПР'
    )
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Дата создания ИПР'
    )
    end_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата завершения ИПР'
    )

    class Meta:
        verbose_name = 'ИПР'
        verbose_name_plural = 'ИПР'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'employee'],
                name='unique_title_employee_iprs'
            )
        ]

    def __str__(self):
        return self.title
