from django.db import models
from django.utils import timezone

class Notice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    posted_by = models.CharField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
