from django.urls import path
from . import views

bible_api_urls = [
    path('verse/', views.VerseListView.as_view(), name="verses"),
    path('verse-detail/<int:pk>/', views.VerseDetailView.as_view(), name="verse_detail"),
    path('chapters/', views.ChapterListView.as_view(), name="chapters"),
]
