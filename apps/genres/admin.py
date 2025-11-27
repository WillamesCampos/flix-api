from django.contrib import admin

from apps.genres.models import Genre

# Register your models here.


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')
