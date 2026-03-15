from django.contrib import admin
from .models import Role
from .models import User
from books.models import UserBook

class UserBookInline(admin.TabularInline):
    model = UserBook
    extra = 0
    raw_id_fields = ('book',)
    readonly_fields = ('updated_at',)
    show_change_link = True

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'status', 'date_joined', 'user_events')
    list_filter = ('role', 'status')
    search_fields = ('username', 'email')
    list_display_links = ('username', 'email')
    inlines = [UserBookInline]
    readonly_fields = ('date_joined', )
    
    @admin.display(description="Мероприятия")
    def user_events(self, obj):
        return ", ".join([e.title for e in obj.events.all()])    