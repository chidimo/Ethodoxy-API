"""Urls"""

from django.urls import path
from . import views

app_name = 'commentary'
urlpatterns = []

urlpatterns += [
    path('challoner/', views.CommentaryByChapter.as_view(), name='commentaries'),
]
