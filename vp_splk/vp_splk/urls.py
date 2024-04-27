from django.contrib import admin
from django.urls import path, include

from vp_splk.views import page_not_found

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('title.urls')),
    path('users/', include('users.urls')),
    path('main/', include('main.urls')),
]


handler404 = page_not_found
