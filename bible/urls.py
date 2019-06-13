from __future__ import unicode_literals

from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('versions', views.VersionViewSet)
router.register('books', views.BooksViewSet)
router.register('chapters', views.ChaptersViewSet)
router.register('verses', views.VersesViewSet)

app_name = 'bible'

urlpatterns = router.urls
