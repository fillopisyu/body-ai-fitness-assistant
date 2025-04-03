# profiles/views.py
from django.shortcuts import render

# Ana sayfa görünümü
def home_view(request):
    # Bu view fonksiyonu şimdilik sadece ilgili HTML şablonunu render etmekle görevli.
    # İleride buraya veritabanından veri çekip şablona gönderme gibi işlemler ekleyebiliriz.
    # Örneğin, giriş yapmış kullanıcının ismini almak gibi:
    # context = {'user': request.user} if request.user.is_authenticated else {}
    return render(request, 'profiles/home.html') # context'i şimdilik boş bırakabiliriz