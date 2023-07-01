from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # ex: /commentsDash/youtube ID/
    #path("video/", views.detail, name="video"),
]