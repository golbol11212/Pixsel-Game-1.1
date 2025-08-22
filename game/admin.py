from django.contrib import admin
from .models import Header, MenuItem

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['site_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'header', 'order', 'is_active']
    list_filter = ['is_active', 'header']
    search_fields = ['title', 'url']
    list_editable = ['order', 'is_active']
    ordering = ['header', 'order']
