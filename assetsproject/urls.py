from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('assets_auth.urls', namespace='assets_auth')),
    path('assets/', include('assets.urls', namespace='assets')),
]
