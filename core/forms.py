from django import forms
from core.models import Task, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "priority", "deadline"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "deadline": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }


class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[("", "All")] + list(Task.Status.choices),
        required=False,
        label="Статус",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    priority = forms.ChoiceField(
        choices=[("", "All")] + list(Task.Priority.choices),
        required=False,
        label="Пріоритет",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    deadline = forms.DateField(
        required=False,
        label="Дата дедлайну",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Напишіть коментар", "class": "form-control"}
            ),
        }