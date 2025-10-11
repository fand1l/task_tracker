from django.shortcuts import render
from django.urls import reverse_lazy
from core import models
from django.views.generic import ListView, DetailView, CreateView
from core.forms import TaskForm

# Create your views here.
class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "Tasks/task_list.html"


class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "Tasks/task_detail.html"


class TaskCreateView(CreateView):
    model = models.Task
    template_name = "Tasks/task_form.html"
    form_class = TaskForm
    success_url = reverse_lazy("core:task_list")