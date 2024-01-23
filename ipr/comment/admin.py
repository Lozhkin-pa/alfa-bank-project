from django.contrib import admin

from comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'created_date',
        'text',
    )


admin.site.register(Comment, CommentAdmin)
