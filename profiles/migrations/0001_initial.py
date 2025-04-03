# Generated by Django 5.2 on 2025-04-03 21:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='Yaş')),
                ('weight_kg', models.FloatField(blank=True, null=True, verbose_name='Kilo (kg)')),
                ('height_cm', models.FloatField(blank=True, null=True, verbose_name='Boy (cm)')),
                ('goal', models.CharField(blank=True, choices=[('WL', 'Kilo Verme'), ('MG', 'Kas Geliştirme'), ('FT', 'Genel Fitness'), ('SP', 'Spesifik Performans')], max_length=2, null=True, verbose_name='Hedef')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Kullanıcı Profili',
                'verbose_name_plural': 'Kullanıcı Profilleri',
            },
        ),
    ]
