from django.contrib import admin

from .models import Newspaper, Topic, Redactor


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Redactor)
class RedactorAdmin(admin.ModelAdmin):
    pass
