# Ecoshare/tips/admin.py

from django.contrib import admin
from .models import TipCategory, RecyclingTip, FavoriteTip

@admin.register(TipCategory)
class TipCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for TipCategory model."""
    list_display = ('name', 'slug', 'created_at')
    # Automatically generate slug from the name field
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(RecyclingTip)
class RecyclingTipAdmin(admin.ModelAdmin):
    """Admin configuration for RecyclingTip model."""
    list_display = ('title', 'author', 'category', 'is_featured', 'views', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    # Automatically generate slug from the title field
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    # Use the author field to automatically set the current user on save
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(FavoriteTip)
class FavoriteTipAdmin(admin.ModelAdmin):
    """Admin configuration for FavoriteTip model."""
    list_display = ('user', 'tip', 'created_at')
    list_filter = ('user', 'tip')
    search_fields = ('user__username', 'tip__title')