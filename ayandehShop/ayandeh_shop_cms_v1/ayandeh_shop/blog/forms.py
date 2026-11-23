from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام شما"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل شما"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "دیدگاه خود را بنویسید..."}),
        }
        labels = {"name": "نام", "email": "ایمیل", "body": "متن دیدگاه"}

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if not body:
            raise forms.ValidationError("متن دیدگاه نمی‌تواند خالی باشد.")
        return body
