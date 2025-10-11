from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("task_create/", views.TaskCreateView.as_view(), name="task_create")
]