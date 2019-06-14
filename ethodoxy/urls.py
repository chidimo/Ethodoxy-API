from django.urls import include, path, re_path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from router.urls import urlpatterns

schema_view = get_schema_view(
   openapi.Info(
      title="Ethodoxy API",
      default_version='v1',
      description="Catholic scriptures.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="orjichidi95@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('siteuser/', include('siteuser.urls')),
    path('api/v1/', include(urlpatterns)),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
]

urlpatterns += [
   re_path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path("__debug__/", include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
