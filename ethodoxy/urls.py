"""doc"""


from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from bible.api.urls import bible_api_urls
from commentary.api.urls import commentary_api_urls

from .import views

api_urls = 'drb.api.urls'

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('bible/', include('bible.urls')),
    path('commentary/', include('commentary.urls')),
    path("members/", include('siteuser.urls')),
    path('bible/api/', include((bible_api_urls , 'bible-api'))),
    path('commentary/api/', include((commentary_api_urls , 'commentary-api'))),
]

urlpatterns += [
    path('social/', include('social_django.urls', namespace='social')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path("__debug__/", include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
