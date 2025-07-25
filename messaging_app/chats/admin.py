from django.contrib import admin
from .models import Conversation, Message
from django.contrib.auth import get_user_model

# Register your models here.
User = get_user_model()

admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Message)