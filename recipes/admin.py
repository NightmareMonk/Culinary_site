from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'difficulty', 'cooking_time', 'created_at')
    list_filter = ('category', 'difficulty', 'created_at', 'author')
    search_fields = ('title', 'description', 'ingredients')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'author')
        }),
        ('Детали рецепта', {
            'fields': ('ingredients', 'instructions', 'cooking_time', 'servings', 'difficulty', 'category')
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
