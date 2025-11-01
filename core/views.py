from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from core.forms import TaskForm, TaskFilterForm, CommentForm
from core.models import Task, Comment
from core.mixins import UserIsOwnerMixin


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "Tasks/task_list.html"

    def get_queryset(self):
        queryset = Task.objects.all()

        # Фільтр
        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            status = form.cleaned_data.get("status")
            priority = form.cleaned_data.get("priority")
            deadline = form.cleaned_data.get("deadline")

            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)
            if deadline:
                queryset = queryset.filter(deadline__date=deadline)

        # Пошук
        query = self.request.GET.get("q", "")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = TaskFilterForm(self.request.GET or None)

        context["is_filtered"] = any(
            self.request.GET.get(param)
            for param in ("q", "status", "priority", "deadline")
        )
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "Tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all().order_by("-created_at")
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = self.object
            comment.save()
            messages.success(request, "Коментар опубліковано")
        else:
            messages.error(request, "Не вдалося додати коментар")
        return redirect("core:task_detail", pk=self.object.pk)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "Tasks/task_form.html"
    form_class = TaskForm
    success_url = reverse_lazy("core:task_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "Tasks/task_form.html"
    success_url = reverse_lazy("core:task_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            task = form.save()
            messages.success(self.request, f"Задача '{task.name}' успішно оновлена")
            return redirect(self.success_url)
        else:
            messages.error(self.request, "Не вдалося оновити задачу")
            return self.render_to_response(self.get_context_data(form=form))


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "Tasks/task_confirm_delete.html"
    success_url = reverse_lazy("core:task_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_title = self.object.name
        self.object.delete()
        messages.success(request, f"Завдання '{task_title}' було успішно видалено!")
        return redirect(self.success_url)


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "Tasks/comment_form.html"

    def get_success_url(self):
        messages.success(self.request, "Коментар оновлено!")
        return reverse_lazy("core:task_detail", kwargs={"pk": self.object.task.pk})

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            messages.error(request, "Ви можете редагувати лише власні коментарі")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "Tasks/comment_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Коментар видалено!")
        return reverse_lazy("core:task_detail", kwargs={"pk": self.object.task.pk})

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            messages.error(request, "Ви можете видаляти лише власні коментарі!")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("core:task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response