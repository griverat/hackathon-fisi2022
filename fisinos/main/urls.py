from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("topics/", views.topics, name="topics"),
    path("profile/", views.update_profile, name="profile"),
]
