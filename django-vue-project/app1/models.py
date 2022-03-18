from django.db import models

# Create your models here.
class Todo(models.Model):
    todo = models.TextField()
    is_done = models.BooleanField()