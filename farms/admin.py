from django.contrib import admin

from .models import Farm, Flock, House


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm_type', 'location', 'is_active')


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm', 'capacity')
    list_filter = ('farm',)


@admin.register(Flock)
class FlockAdmin(admin.ModelAdmin):
    list_display = ('code', 'house', 'breed', 'initial_quantity', 'status')
    list_filter = ('status', 'house__farm')