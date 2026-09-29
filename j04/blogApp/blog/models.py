from django.conf import settings
from django.db import models
class Post(models.Model):
    title = models.CharField("عنوان", max_length=200)
    content = models.TextField("متن")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts", verbose_name="نویسنده")
    created_at = models.DateTimeField("زمان ایجاد", auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "نوشته"
        verbose_name_plural = "نوشته‌ها"
    def __str__(self):
        return self.title
