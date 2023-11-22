from django.db import models
from django.contrib.auth.models import AbstractUser


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField()
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    publishers = models.ManyToManyField('Redactor', related_name='newspapers')

    def __str__(self):
        return f"{self.title} ({self.published_date})"


class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(default=0)
