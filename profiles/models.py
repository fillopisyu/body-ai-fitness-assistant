# profiles/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Yaş")
    weight_kg = models.FloatField(null=True, blank=True, verbose_name="Kilo (kg)")
    height_cm = models.FloatField(null=True, blank=True, verbose_name="Boy (cm)")
    GOAL_CHOICES = [
        ('WL', 'Kilo Verme'),
        ('MG', 'Kas Geliştirme'),
        ('FT', 'Genel Fitness'),
        ('SP', 'Spesifik Performans'),
    ]
    goal = models.CharField(max_length=2, choices=GOAL_CHOICES, null=True, blank=True, verbose_name="Hedef")
    def __str__(self): return f"{self.user.username}'s Profile"
    class Meta: verbose_name, verbose_name_plural = "Kullanıcı Profili", "Kullanıcı Profilleri"



class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Konuşma: {self.user.username} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
    class Meta: ordering, verbose_name, verbose_name_plural = ['-created_at'], "Konuşma Geçmişi", "Konuşma Geçmişleri"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    ROLE_CHOICES = [('user', 'Kullanıcı'), ('model', 'Yapay Zeka')]
    role = models.CharField(max_length=5, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.get_role_display()}: {self.content[:50]}..."
    class Meta: ordering, verbose_name, verbose_name_plural = ['timestamp'], "Mesaj", "Mesajlar"

class SavedProgram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_programs')
    content_html = models.TextField(verbose_name="Program İçeriği (HTML)")
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Program Başlığı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kaydedilme Tarihi")
    # *** YENİ EKLENEN ALAN ***
    completed = models.BooleanField(default=False, verbose_name="Tamamlandı mı?")
    exercise_list = models.TextField(blank=True, null=True, verbose_name="Egzersiz Listesi (Tahmini)") # YENİ ALAN

    def __str__(self):
        status = "[Tamamlandı]" if self.completed else ""
        return f"{self.user.username} - {self.title or 'Başlıksız Program'} {status} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kaydedilen Program"
        verbose_name_plural = "Kaydedilen Programlar"

