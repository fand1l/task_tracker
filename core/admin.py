from django.contrib import admin
from .models import Task, Comment, TaskImage


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


@admin.register(TaskImage)
class TaskImageAdmin(admin.ModelAdmin):
    list_display = ("task", "image", "uploaded_at")
    list_filter = ("uploaded_at", "task")
    search_fields = ("task__name",)
    readonly_fields = ("uploaded_at",)