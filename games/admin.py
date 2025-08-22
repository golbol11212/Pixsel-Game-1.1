from django.contrib import admin
from .models import GameScore, GameComment

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'game_name', 'score', 'level', 'achieved_at']
    list_filter = ['game_name', 'achieved_at']
    search_fields = ['user__username', 'game_name']
    readonly_fields = ['achieved_at']
    ordering = ['-score']

@admin.register(GameComment)
class GameCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'game_name', 'content', 'created_at']
    list_filter = ['game_name', 'created_at']
    search_fields = ['user__username', 'content']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
