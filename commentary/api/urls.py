from django.urls import path
from . import views

commentary_api_urls = [
    path('commentary/', views.CommentaryTextListView.as_view(), name="commentaries"),
]
