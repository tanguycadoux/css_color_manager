from django.contrib import admin

from .models import Color, ColorFamily


admin.site.register(ColorFamily)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "mode", "values", "family", "created_datetime", "updated_datetime"]
    list_filter = ["created_datetime", "updated_datetime", "family"]
