from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mission.urls')),
    path('', include('user.urls')),
    path('', include('exp.urls')),
    path('', include('thanks.urls')),
]
