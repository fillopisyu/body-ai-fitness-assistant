# profiles/admin.py
from django.contrib import admin
from .models import UserProfile # Bir önceki adımda oluşturduğumuz UserProfile modelini import ediyoruz

# UserProfile modelini admin paneline kaydediyoruz ki orada görünsün ve yönetilebilsin
admin.site.register(UserProfile)

# Not: Daha karmaşık yönetim arayüzleri için admin.ModelAdmin sınıfları kullanılır,
# ancak şimdilik bu basit kayıt işlemi yeterlidir. İleride bunu geliştirebiliriz.