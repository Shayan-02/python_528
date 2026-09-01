from django.db import models

# Create your models here.
class Book(models.Model):
    b_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    page = models.IntegerField(null=True)
    isbn = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)