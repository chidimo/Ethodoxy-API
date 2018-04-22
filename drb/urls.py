"""Urls"""

from django.urls import path
from . import views

app_name = 'bible'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('book/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('chapter/<int:pk>/', views.ChapterDetail.as_view(), name='chapter-detail'),
    path('verse/<int:pk>/', views.VerseDetail.as_view(), name='verse-detail'),
]

urlpatterns += [
    path('commentaries/', views.CommentaryByChapter.as_view(), name='commentaries'),
    path('commentary/challoner/<slug:slug>/', views.CommentaryTextDetail.as_view(), name='commentary_detail'),
]
