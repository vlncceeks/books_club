from django.contrib import admin

from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'book', 'organizer', 'registered_count', 'free_places')
    list_filter = ('book__genre',)
    search_fields = ('title', 'book__title', 'organizer__username')
    raw_id_fields = ('book', 'organizer')
    filter_horizontal = ("participants",)
    date_hierarchy = 'event_date'

    @admin.display(description="Записано")
    def registered_count(self, obj):
        return obj.registered_count

    @admin.display(description="Свободно")
    def free_places(self, obj):
        return obj.free_places    


