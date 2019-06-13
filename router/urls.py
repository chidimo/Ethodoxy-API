from __future__ import unicode_literals

from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from bible import views as bibleviews
from commentary import views as commentaryviews

router = routers.DefaultRouter()
router.register('versions', bibleviews.VersionViewSet)
router.register('books', bibleviews.BooksViewSet)
router.register('chapters', bibleviews.ChaptersViewSet)
router.register('verses', bibleviews.VersesViewSet)
router.register('commentary', commentaryviews.CommentaryTextViewSet)

urlpatterns = router.urls
