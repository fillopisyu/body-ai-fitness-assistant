# profiles/urls.py
from django.urls import path
from . import views # Aynı klasördeki views.py'ı import ediyoruz

urlpatterns = [
    # Uygulama seviyesindeki kök adres ('') home_view fonksiyonuna gitsin.
    # name='home' -> Bu URL'e şablonlarda {% url 'home' %} şeklinde referans vermemizi sağlar.
    path('', views.home_view, name='home'),

    # Buraya ileride profil, ayarlar, giriş, kayıt vb. URL pattern'leri eklenecek
    # path('profile/', views.profile_view, name='profile'),
    # path('login/', views.login_view, name='login'),
]