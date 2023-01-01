from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
'''
class User(models.Model):
    first = models.CharField(max_length = 64)
    last = models.CharField(max_length = 64)

    def __str__(self):
        return f'User {self.id} {self.first} {self.last}'
'''

#model manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

        @property
        def all(self):
            return self.get_queryset()


# The post model
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published')
    )

    title = models.CharField(max_length = 64)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_id')
    body = models.TextField()
    slug = models.SlugField(max_length = 64, unique_for_date = 'publish')
    #using pillow to upload the featured images
    image = models.ImageField(upload_to = 'featured_image/%Y/%m/%d/')
    
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')

    body = RichTextUploadingField() #for ckeditor


    class meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects = models.Manager() # default manager
    published = PublishedManager() #my custom

    def get_absolute_url(self):
        return reverse ('blog:post_detail', args = [self.slug])

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

# comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    parent = models.ForeignKey('self', null=True, blank = True, on_delete = models.CASCADE)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default = True)

    class meta:
        ordering = ('created',)

    def __str__(self):
        return self.body

    def get_comments(self):
        return Comments.objects.filter(parent=self).filter(active=True)