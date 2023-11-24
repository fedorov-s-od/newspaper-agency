from django.urls import path, re_path

from .views import (index, NewspaperListView, NewspaperCreateView,
                    NewspaperDetailView, NewspaperDeleteView,
                    NewspaperUpdateView, pages, login_view, register_user)
from django.contrib.auth.views import LogoutView


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
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspapers/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspaper-delete"),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]

app_name = "newspaper"
