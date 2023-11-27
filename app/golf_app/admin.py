from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'handicap', 'contact_email')

class PlayerGameScoreInline(admin.TabularInline):
    model = PlayerGameScore
    extra = 1

admin.site.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'date')
    inlines = [PlayerGameScoreInline]

admin.site.register(PlayerGameScore)
class PlayerGameScoreAdmin(admin.ModelAdmin):
    list_display = ('player', 'game', 'score')

admin.site.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'password', 'email')
