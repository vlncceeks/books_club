from django.contrib import admin
from .models import Book
from .models import Genre
from .models import UserBook

class UserBookInline(admin.TabularInline):
    model = UserBook
    extra = 0
    raw_id_fields = ('book',)
    readonly_fields = ('updated_at',)
    show_change_link = True

# Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'year')
    list_filter = ('genre', 'year')
    search_fields = ('title', 'author')
    inlines = [UserBookInline]

# UserBook
@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'reading_status', 'rating', 'updated_at')
    list_filter = ('reading_status', 'book__genre')
    search_fields = ('user__name', 'book__title')
    raw_id_fields = ('user', 'book')
    readonly_fields = ('updated_at',)
