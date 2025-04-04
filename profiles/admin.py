# profiles/admin.py
from django.contrib import admin
from .models import UserProfile, Conversation, Message, SavedProgram

admin.site.register(UserProfile)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(SavedProgram)