from django.urls import path
from .import views

apiurlpatterns = [
    path('verse/', views.VerseListView.as_view(), name="verses"),
    path('verse-detail/<int:pk>/', views.VerseDetailView.as_view(), name="verse_detail"),
    path('chapters/', views.ChapterListView.as_view(), name="chapters"),
    path('commentary/', views.CommentaryTextListView.as_view(), name="commentaries"),
]
