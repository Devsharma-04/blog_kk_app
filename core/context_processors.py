from .models import Message

def unread_messages_notifier(request):
    if request.user.is_authenticated:
        # Check karein ki user ke liye koi unread message hai
        unread_exists = Message.objects.filter(receiver=request.user, is_read=False).exists()
        return {'has_unread_messages': unread_exists}
    return {'has_unread_messages': False}