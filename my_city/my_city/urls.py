from django.contrib import admin
from django.urls import include, path

from .settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns