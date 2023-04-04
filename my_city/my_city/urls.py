from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL

schema_view = get_schema_view(
    openapi.Info(
        title="my_city_api",
        default_version='v1',
        description="documentation my_city",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/users/', include('user_app.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('knox.urls')),
    path('api/questapp/', include('quest_app.urls')),
]
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

if DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
