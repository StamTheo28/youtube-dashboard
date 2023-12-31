from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video_id/<str:video_id>/', views.analysis, name='analysis'),
]
