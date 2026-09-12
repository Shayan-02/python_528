from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# # Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RB', 'Rejected'

    title = models.CharField(max_length=255)
    content = models.TextField()
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    slug = models.SlugField(max_length=255, unique=True)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=Status.choices, default=Status.DRAFT, max_length=2)


    class Meta:
        ordering = ('-published_at',)
        indexes = [models.Index(fields=['title'])]

    def __str__(self):
        return self.title