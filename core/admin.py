from django.contrib import admin
from .models import Profile, Post, FriendRequest, Message, Notification, Story, CallSession, Comment

# Saare models ko register karein taaki wo dashboard par dikhein
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(CallSession) # <-- Ye line sabse important hai video call ke liye