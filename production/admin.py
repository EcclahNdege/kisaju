from django.contrib import admin

from .models import DailyLog


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'flock', 'deaths', 'culls', 'feed_used_kg', 'eggs_collected')
    list_filter = ('flock__house__farm', 'date')
    readonly_fields = ('recorded_by',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)