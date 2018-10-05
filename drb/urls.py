"""Urls"""

from django.urls import path
from . import views

app_name = 'douay-rheims'

urlpatterns = [
    path('', views.Index.as_view(), name='bible_index'),
    path('book/<slug:slug>/<int:pk>/', views.BookChapters.as_view(), name='book_detail'),
    path('<str:book_name>-<int:number>/<int:pk>/', views.ChapterDetail.as_view(), name='chapter_detail'),
    path('verse/<int:pk>/', views.VerseDetail.as_view(), name='verse_detail'),
]

urlpatterns += [
    path('commentaries/', views.CommentaryByChapter.as_view(), name='commentaries'),
    path('commentary/challoner/<slug:slug>/', views.CommentaryTextDetail.as_view(), name='commentary_detail'),
]
