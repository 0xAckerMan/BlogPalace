from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
'''
class User(models.Model):
    first = models.CharField(max_length = 64)
    last = models.CharField(max_length = 64)

    def __str__(self):
        return f'User {self.id} {self.first} {self.last}'
'''

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published')
    )

    title = models.CharField(max_length = 64)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_id')
    body = models.TextField()
    slug = models.SlugField(max_length = 64, unique_for_date = 'publish')

    published = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')
    
    class meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
