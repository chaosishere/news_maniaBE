from django.db import models
from django.contrib.auth.models import User

class NewsHistory(models.Model):
    keyword = models.CharField(max_length=255)
    category = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=10, null=True, blank=True)
    source = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True) 
    urlToImage = models.URLField(null=True, blank=True)
    publishedAt = models.DateTimeField()
    content = models.TextField(null=True, blank=True)
    fetched_at = models.DateTimeField()