from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from core import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from core.forms import TaskForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.views.generic import DetailView

# Create your views here.

class TaskListView(ListView):
   model = models.Task
   context_object_name = "tasks"
   template_name = "Tasks/task_list.html"


   def get_queryset(self):
       queryset = super().get_queryset()
       status = self.request.GET.get("status", "")
       if status:
           queryset = queryset.filter(status=status)
       return queryset


   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context["form"] = TaskFilterForm(self.request.GET)
       return context




class TaskDetailView(LoginRequiredMixin, DetailView):
   model = models.Task
   context_object_name = "task"
   template_name = 'Tasks/task_detail.html'


   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['comment_form'] = CommentForm()  # Додаємо порожню форму коментаря в контекст
       return context


   def post(self, request, *args, **kwargs):
       comment_form = CommentForm(request.POST, request.FILES)
       if comment_form.is_valid():
           comment = comment_form.save(commit=False)
           comment.author = request.user
           comment.task = self.get_object()
           comment.save()
           return redirect('core:task-detail', pk=comment.task.pk)
       else:
           # Тут можна обробити випадок з невалідною формою
           pass




class TaskCreateView(LoginRequiredMixin, CreateView):
   model = models.Task
   template_name = "Tasks/task_form.html"
   form_class = TaskForm
   success_url = reverse_lazy("core:task-list")


   def form_valid(self, form):
       form.instance.creator = self.request.user
       return super().form_valid(form)




class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
   def post(self, request, *args, **kwargs):
       task = self.get_object()
       task.status = "done"
       task.save()
       return HttpResponseRedirect(reverse_lazy("core:task-list"))


   def get_object(self):
       task_id = self.kwargs.get("pk")
       return get_object_or_404(models.Task, pk=task_id)




class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
   model = models.Task
   form_class = TaskForm
   template_name = "Tasks/task_update_form.html"
   success_url = reverse_lazy("core:task-list")




class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
   model = models.Task
   success_url = reverse_lazy("core:task-list")
   template_name = "Tasks/task_delete_confirmation.html"




class CommentUpdateView(LoginRequiredMixin, UpdateView):
   model = models.Comment
   fields = ['content']
   template_name = 'Tasks/edit_comment.html'


   def form_valid(self, form):
       comment = self.get_object()
       if comment.author != self.request.user:
           raise PermissionDenied("Ви не можете редагувати цей коментар.")
       return super().form_valid(form)


   def get_success_url(self):
       return reverse_lazy('core:task_detail', kwargs={'pk': self.object.task.pk})




class CommentDeleteView(LoginRequiredMixin, DeleteView):
   model = models.Comment
   template_name = 'Tasks/delete_comment.html'


   def get_queryset(self):
       queryset = super().get_queryset()
       return queryset.filter(author=self.request.user)


   def get_success_url(self):
       return reverse_lazy('core:task_detail', kwargs={'pk': self.object.task.pk})




class CommentLikeToggle(LoginRequiredMixin, View):
   def post(self, request, *args, **kwargs):
       comment = get_object_or_404(models.Comment, pk=self.kwargs.get('pk'))
       like_qs = models.Like.objects.filter(comment=comment, user=request.user)
       if like_qs.exists():
           like_qs.delete()
       else:
           models.Like.objects.create(comment=comment, user=request.user)
       return HttpResponseRedirect(comment.get_absolute_url())




class CustomLoginView(LoginView):
   template_name = "Tasks/login.html"
   redirect_authenticated_user = True




class CustomLogoutView(LogoutView):
   next_page = "core:login"




class RegisterView(CreateView):
   template_name = "Tasks/register.html"
   form_class = UserCreationFormcore

   def form_valid(self, form):
       user = form.save()
       login(self.request, user)
       return redirect(reverse_lazy("core:login"))



# class TaskListView(ListView):
#     model = models.Task
#     context_object_name = "tasks"
#     template_name = "Tasks/task_list.html"


# class TaskDetailView(DetailView):
#     model = models.Task
#     context_object_name = "task"
#     template_name = "Tasks/task_detail.html"


# class TaskCreateView(CreateView):
#     model = models.Task
#     template_name = "Tasks/task_form.html"
#     form_class = TaskForm
#     success_url = reverse_lazy("core:task_list")


# class RegisterView():
#     class Meta():
#         model = User()


# class TaskUpdateView(UpdateView):
#     model = models.Task


# class TaskDeleteView(DeleteView):
#     model = models.Task