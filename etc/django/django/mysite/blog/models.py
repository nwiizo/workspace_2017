from django.db import models
from django.utils import timezone

# Create your models here.



class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField('title',max_length=200)
    text = models.TextField('text')
    file_url = models.CharField('file_url',max_length=200,default='/')
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
