from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from vp_splk import settings
from vp_splk.views import page_not_found

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('title.urls')),
    path('users/', include('users.urls')),
    path('main/', include('main.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'ВП СПЛК'
