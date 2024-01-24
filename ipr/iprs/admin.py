from django.contrib import admin
from .models import Ipr


@admin.register(Ipr)
class IprAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'employee',
        'author',
        'description',
        'status',
        'created_date',
        'end_date',
        # 'tasks'
    )
    search_fields = ('title', 'employee', 'author',)
    list_filter = ('id', 'title', 'employee', 'author')
    empty_value_display = '-пусто-'
