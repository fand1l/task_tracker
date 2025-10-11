from django.contrib import admin
from .models import Task, Comment

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "status", "priority", "deadline")
    list_filter = ("status", "deadline", "priority")
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "author", "content")
    list_filter = ("created_at",)
    search_fields = ("content",)
    readonly_fields = ("created_at",)