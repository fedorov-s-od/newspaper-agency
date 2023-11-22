from django.urls import path

from newspaper.models import Newspaper

from .views import index, NewspaperListView, NewspaperCreateView, NewspaperDetailView


urlpatterns = [
    path("", index, name="index"),
    path(
        "newspapers/",
        NewspaperListView.as_view(),
        name="newspaper-list",
    ),
    path(
        "newspaper/create/",
        NewspaperCreateView.as_view(),
        name="newspaper-create",
    ),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
]

app_name = "newspaper"
