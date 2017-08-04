from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Create your models here.



class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField('title',max_length=200,default='')
    text = models.TextField('text')
    file_url = models.CharField('file_url',max_length=200,default='/')
    school_year = models.IntegerField('school_year',default=0)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def vakidate_school(school_year):
        if school_year > 7:
            raise ValidationError(
                _('%(value)s is not an even number'),
                params={'value': school_year},
            )
