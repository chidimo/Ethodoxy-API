"""doc"""


from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from drb.api.urls import apiurlpatterns

from .import views

api_urls = 'drb.api.urls'

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('douay-rheims', include('drb.urls')),
    path("members/", include('siteuser.urls')),
    path('api/', include((apiurlpatterns , 'drb-api'))),
]

urlpatterns += [
    path('social/', include('social_django.urls', namespace='social')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path("__debug__/", include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
