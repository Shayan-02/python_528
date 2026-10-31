from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "What needs doing?", "autofocus": True}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Notes (optional)"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
