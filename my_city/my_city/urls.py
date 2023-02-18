from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static


from .settings import DEBUG, STATIC_ROOT, STATIC_URL

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(STATIC_URL, document_root=STATIC_ROOT)


if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns