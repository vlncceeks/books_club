from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'text')
    list_filter = ('created_at', 'book__genre')
    search_fields = ('user__username', 'book__title', 'event__title')
    raw_id_fields = ('user', 'book', 'event')
    readonly_fields = ('created_at',)

    @admin.display(description="Объект")
    def get_target(self, obj):
        if obj.book:
            return obj.book.title
        if obj.event:
            return obj.event.title
        return "-"

