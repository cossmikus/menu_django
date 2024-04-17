from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    search_fields = ['name']

admin.site.register(MenuItem, MenuItemAdmin)