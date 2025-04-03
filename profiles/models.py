# profiles/models.py
from django.db import models
from django.contrib.auth.models import User # Django'nun hazır User modelini kullanacağız

class UserProfile(models.Model):
    # Her UserProfile'ı bir Django User'ına bağlıyoruz (One-to-One)
    # User silinince ilişkili Profile da silinsin (CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # AI için gerekli olabilecek temel bilgiler (daha sonra genişletilebilir)
    # null=True: Veritabanında boş olabilir. blank=True: Formlarda boş bırakılabilir.
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Yaş")
    weight_kg = models.FloatField(null=True, blank=True, verbose_name="Kilo (kg)")
    height_cm = models.FloatField(null=True, blank=True, verbose_name="Boy (cm)")

    # Örnek bir hedef seçimi (daha karmaşık hale getirilebilir)
    GOAL_CHOICES = [
        ('WL', 'Kilo Verme'),
        ('MG', 'Kas Geliştirme'),
        ('FT', 'Genel Fitness'),
        ('SP', 'Spesifik Performans'), # Yeni seçenek eklendi
    ]
    goal = models.CharField(
        max_length=2,
        choices=GOAL_CHOICES,
        null=True,
        blank=True,
        verbose_name="Hedef"
    )

    # Fitness seviyesi, ekipman durumu, haftalık antrenman günü gibi alanlar eklenebilir

    def __str__(self):
        # Yönetim panelinde vb. okunabilir bir isim sağlar
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"