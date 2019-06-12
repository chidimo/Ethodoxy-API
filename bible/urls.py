"""Urls"""

from django.urls import path
from . import views

app_name = 'bible'

urlpatterns = [    
    path('', views.bible_index, name='bible_index'),
    path('chapter/<int:pk>/', views.get_chapter, name='get_chapter'),
]

# <h3 class='float-left'>The Complete Douay-Rheims bible<span class="current-book"> >>  ${ book_name }$</span><span class="current-chapter"> >> ${ book_chapter }$</span></h3>