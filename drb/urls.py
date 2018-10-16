"""Urls"""

from django.urls import path
from . import views

app_name = 'douay-rheims'

urlpatterns = [    
    path('', views.douay_rheims_bible, name='douay_rheims_bible'),
    path('chapter/<int:pk>/', views.get_chapter, name='get_chapter'),
]

urlpatterns += [
    path('challoner/', views.CommentaryByChapter.as_view(), name='commentaries'),
]


# <h3 class='float-left'>The Complete Douay-Rheims bible<span class="current-book"> >>  ${ book_name }$</span><span class="current-chapter"> >> ${ book_chapter }$</span></h3>