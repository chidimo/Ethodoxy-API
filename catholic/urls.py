"""doc"""


from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from drb.api.urls import apiurlpatterns

api_urls = 'drb.api.urls'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('drb.urls')),
    path("members/", include('siteuser.urls')),
    path('api/', include((apiurlpatterns , 'drb-api'))),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path("__debug__/", include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
