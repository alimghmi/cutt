from django.db import models
from django.contrib.auth.models import User


class Visitor(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    visited_at = models.DateTimeField(auto_now_add=True)
    

class Viewer(models.Model):
    visitor = models.ForeignKey(Visitor, related_name='views', on_delete=models.CASCADE)
    link = models.ForeignKey('Link', related_name='views', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)


class Link(models.Model):
    user = models.ForeignKey(User, related_name='links', on_delete=models.CASCADE)
    origin = models.URLField(max_length=256)
    slug = models.CharField(max_length=16, unique=True, blank=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)



