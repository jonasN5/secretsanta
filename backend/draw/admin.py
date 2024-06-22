from django.contrib import admin

from draw.models import *


@admin.register(User)
class MyAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_superuser')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    readonly_fields = ('id',)


@admin.register(DrawPair)
class DrawPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'santa', 'santee', 'draw')
    readonly_fields = ('id',)


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner')
    readonly_fields = ('id',)
