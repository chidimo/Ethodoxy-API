"""doc"""

from django.contrib import admin
from django.urls import path, include

from drb.api.urls import apiurlpatterns

api_urls = 'drb.api.urls'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('drb.urls')),
    path('api/', include((apiurlpatterns , 'drb-api'))),
]
