from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# -----------------------------
# 1. User Profile (Fixed related_name)
# -----------------------------
class Profile(models.Model):
    # related_name='profile' add kiya taaki user.profile kaam kare
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png')
    followers = models.ManyToManyField(User, related_name='following_profiles', blank=True)

    def __str__(self):
        return self.user.username

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return Profile.objects.filter(followers=self.user).count()

# -----------------------------
# 2. User Posts
# -----------------------------
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="posts/")
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.caption[:20]}"

    def total_likes(self):
        return self.likes.count()

# -----------------------------
# 3. Interactions (Friend Request & Comments)
# -----------------------------
class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"From: {self.from_user.username} To: {self.to_user.username} ({self.status})"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): # Fix: __clstr__ ko __str__ kiya
        return f'{self.user.username} - {self.content[:20]}'

# -----------------------------
# 4. Chat System
# -----------------------------
class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['first_person', 'second_person']

    def __str__(self):
        return f"Chat between {self.first_person.username} and {self.second_person.username}"

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.sender.username} To: {self.receiver.username}"

# -----------------------------
# 5. Stories & Media
# -----------------------------
class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/')
    music_url = models.URLField(max_length=500, blank=True, null=True) 
    caption = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (timezone.now() - self.created_at).total_seconds() < 86400

    def __str__(self):
        return f"{self.user.username}'s story"

class MusicLibrary(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='library_music/')
    thumbnail = models.ImageField(upload_to='music_thumbs/', blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"

# -----------------------------
# 6. Notifications & Video Call
# -----------------------------
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Like'),
        (2, 'Friend Request'),
        (3, 'Message'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_sender")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES, default=1)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"To: {self.user.username} | From: {self.sender.username}"


class CallSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    peer_id = models.CharField(max_length=255, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_busy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.peer_id}"