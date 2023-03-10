from django.contrib import admin
from rest_framework import permissions
from django.urls import include, path, re_path
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .settings import (DEBUG,
                       STATIC_ROOT,
                       STATIC_URL,
                       MEDIA_URL,
                       MEDIA_ROOT)

schema_view = get_schema_view(
   openapi.Info(
      title="redoc_my_city",
      default_version='v1',
      description="documentation my_city",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
] + (static(STATIC_URL, document_root=STATIC_ROOT)
     + static(MEDIA_URL, document_root=MEDIA_ROOT))


if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
