# benbodyai_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Kök adrese ('') gelen tüm istekleri profiles.urls içindeki pattern'lerle eşleştirmeyi dene:
    path('', include('profiles.urls')),
]