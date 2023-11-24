from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField()
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    publishers = models.ManyToManyField('Redactor', related_name='newspapers')

    @cached_property
    def publishers_to_str(self):
        return ", ".join(publisher.username for publisher in self.publishers.all())

    @cached_property
    def content_to_html(self):
        return "<br />".join(self.content.split("\\n"))

    def __str__(self):
        return f"{self.title} ({self.published_date})"


class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(default=0)
