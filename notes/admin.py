from django.contrib import admin
from notes.models import *

# Register your models here.

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title","updated_at","content")
    search_fields = ("title", "content", "user__username")
    list_filter = ("updated_at",)
