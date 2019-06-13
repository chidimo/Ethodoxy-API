from __future__ import unicode_literals
from django.urls import path

from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('commentary', views.CommentaryTextViewSet)

app_name = 'commentary'

urlpatterns = [
    path('', include(router.urls)),
]
