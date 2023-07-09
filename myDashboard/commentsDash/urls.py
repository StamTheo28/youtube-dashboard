from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("s<str:video_id>/", views.analysis, name='analysis')
]