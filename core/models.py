from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    '''Task model'''

    class Status(models.TextChoices):
        TO_DO = "to_do", "To do"                    # Ще не почато
        IN_PROGRESS = "in_progress", "In progress"  # В процесі
        DONE = "done", "Done"                       # Виконано
        ON_HOLD = "on_hold", "On hold"              # Затримано / Відкладено
        CANCELED = "canceled", "Canceled"           # Скасовано
        EXPIRED = "expired", "Expired"              # Вийшов термін

    class Priority(models.TextChoices):
        R = "R", "First Priority"   # R - Red
        O = "O", "Second Priority"  # O - Orange
        Y = "Y", "Third Priority"   # Y - Yellow
        G = "G", "Fourth Priority"  # G - Green
        B = "B", "Fifth Priority"   # B - Blue
        N = "N", "None"             # N - None

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default="to_do"
    )
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default="N"
    )
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} [{self.status}]"

    @property
    def is_expired(self) -> bool:
        return self.deadline and self.deadline < timezone.now() # True, якщо дедлайн заданий і вже минув


class Comment(models.Model):
    '''Comment models'''

    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,  # видалити всі коментарі, якщо видалити задачу
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,  # якщо користувач видалений, коментар залишиться, author = NULL
        null=True,
        blank=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task.name}"