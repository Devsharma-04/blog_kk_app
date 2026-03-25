from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Notification, FriendRequest, Message, Profile, CallSession
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# ==========================================
# 1. USER ASSETS (Profile & CallSession)
# ==========================================

@receiver(post_save, sender=User)
def manage_user_assets(sender, instance, created, **kwargs):
    """
    Jab naya user register ho toh uski Profile aur CallSession create karein.
    Purane users ke liye data update karein.
    """
    if created:
        Profile.objects.get_or_create(user=instance)
        CallSession.objects.get_or_create(user=instance)
    else:
        # Profile save karein (safely check karke)
        if hasattr(instance, 'profile'):
            instance.profile.save()
        # CallSession save karein (safely check karke)
        if hasattr(instance, 'call_session'):
            instance.call_session.save()


# ==========================================
# 2. REAL-TIME NOTIFICATIONS (WebSockets)
# ==========================================

# --- Like Notification ---
@receiver(m2m_changed, sender=Post.likes.through)
def send_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        channel_layer = get_channel_layer()
        for user_id in pk_set:
            sender_user = User.objects.get(pk=user_id)
            if sender_user != instance.user:
                notification_msg = f"{sender_user.username} liked your post!"
                
                # Database mein save
                Notification.objects.create(
                    user=instance.user,
                    sender=sender_user,
                    post=instance,
                    notification_type=1, # 1 = Like
                    message=notification_msg
                )
                
                # Real-time alert
                if channel_layer:
                    async_to_sync(channel_layer.group_send)(
                        f"user_{instance.user.id}",
                        {
                            "type": "send_notification",
                            "value": {
                                "message": notification_msg,
                                "sender": sender_user.username,
                                "type": "like"
                            }
                        }
                    )

# --- Friend Request Notification ---
@receiver(post_save, sender=FriendRequest)
def friend_request_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification_msg = f"{instance.from_user.username} has sent you a friend request!"
        
        # Database mein save
        Notification.objects.create(
            user=instance.to_user,
            sender=instance.from_user,
            notification_type=2, # 2 = Friend Request
            message=notification_msg
        )
        
        # Real-time alert
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.to_user.id}",
                {
                    "type": "send_notification",
                    "value": {
                        "message": notification_msg,
                        "sender": instance.from_user.username,
                        "type": "friend_request"
                    }
                }
            )

# --- Message Notification ---
@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification_msg = f"{instance.sender.username} sent you a message!"
        
        # Chat alerts ke liye database notification optional hai, 
        # par real-time alert dena zaroori hai.
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.receiver.id}",
                {
                    "type": "send_notification",
                    "value": {
                        "message": notification_msg,
                        "sender": instance.sender.username,
                        "type": "message"
                    }
                }
            )