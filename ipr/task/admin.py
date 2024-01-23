from django.contrib import admin

from task.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'created_date',
        'deadline',
        'status'
    )


admin.site.register(Task, TaskAdmin)
