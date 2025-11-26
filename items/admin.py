from django.contrib import admin
from .models import Category, Item, ItemImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'condition', 'owner', 'is_free', 'created_at')
    list_filter = ('status', 'condition', 'category', 'is_free')
    search_fields = ('title', 'description', 'location', 'owner__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ItemImageInline]

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary',)