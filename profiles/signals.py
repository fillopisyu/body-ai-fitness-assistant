# profiles/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Yeni bir User oluşturulduğunda otomatik olarak ilişkili UserProfile'ı oluşturur,
    User güncellendiğinde ise profile'ı kaydeder (opsiyonel).
    """
    if created:
        # Eğer User objesi YENİ oluşturulduysa (kayıt olma işlemi)
        UserProfile.objects.create(user=instance)
    # Eğer User objesi güncellendiyse (yeni oluşturulmadıysa)
    # instance.profile.save() # İlişkili profilin de kaydedilmesini sağlayabiliriz (Şimdilik yoruma aldık)