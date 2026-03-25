import base64
import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

# Forms aur Models imports
from .forms import UserUpdateForm, ProfileUpdateForm, PostForm, StoryUploadForm
from .models import Profile, Post, FriendRequest, Message, Notification, Story, Comment, CallSession

# ==========================================
# 1. SPOTIFY SETUP
# ==========================================
CLIENT_ID = '7bdd68304de54dab8d3886eb26ec4c7f'
CLIENT_SECRET = '8fa73ac5fcf641b5a7a5ed9c158f8c65'

def get_spotify_client():
    try:
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        print(f"Spotify Setup Error: {e}")
        return None

# -----------------------------
# Landing Page
# -----------------------------
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')

# -----------------------------
# Home page (feed + Stories)
# -----------------------------
@login_required
def home(request):
    time_threshold = timezone.now() - timedelta(hours=24)
    active_stories = Story.objects.filter(created_at__gte=time_threshold).order_by('-created_at')
    posts = Post.objects.all().order_by("-created_at")
    
    context = {
        "posts": posts,
        "stories": active_stories 
    }
    return render(request, "home.html", context)

# -----------------------------
# Spotify Search
# -----------------------------
@login_required
def spotify_search(request):
    query = request.GET.get('q', '').lower()
    if len(query) < 2:
        return JsonResponse({'results': []})

    mock_tracks = [
        {'name': 'Stay', 'artist': 'Justin Bieber', 'image': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300&h=300&fit=crop', 'preview_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'},
        {'name': 'Peaches', 'artist': 'Justin Bieber', 'image': 'https://images.unsplash.com/photo-1493225255756-d9584f8606e9?w=300&h=300&fit=crop', 'preview_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'},
        {'name': 'Baby', 'artist': 'Justin Bieber', 'image': 'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=300&h=300&fit=crop', 'preview_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3'},
        {'name': 'Starboy', 'artist': 'The Weeknd', 'image': 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=300&h=300&fit=crop', 'preview_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3'}
    ]

    results = [t for t in mock_tracks if query in t['name'].lower() or query in t['artist'].lower()]
    return JsonResponse({'results': results})

@login_required
def upload_story(request):
    if request.method == 'POST':
        form = StoryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.music_url = request.POST.get('selected_music_url')
            story.save()
            return redirect('home')
    else:
        form = StoryUploadForm()
    return render(request, 'upload_story.html', {'form': form})

# -----------------------------
# Friend System & Profiles
# -----------------------------
@login_required
def search_users(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = User.objects.filter(Q(username__icontains=query)).exclude(id=request.user.id)
    return render(request, 'search_results.html', {'results': results, 'query': query})

@login_required
def user_profile(request, username):
    user_to_view = get_object_or_404(User, username=username)
    profile_obj, _ = Profile.objects.get_or_create(user=user_to_view)
    posts = Post.objects.filter(user=user_to_view).order_by('-created_at')
    
    is_friend = FriendRequest.objects.filter(
        (Q(from_user=request.user, to_user=user_to_view) | Q(from_user=user_to_view, to_user=request.user)),
        status='accepted'
    ).exists()

    context = {
        'view_user': user_to_view,
        'view_profile': profile_obj,
        'posts': posts,
        'is_friend': is_friend,
    }
    return render(request, 'user_profile.html', context)

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def share_post(request, post_id, username):
    post_obj = get_object_or_404(Post, id=post_id) 
    receiver = get_object_or_404(User, username=username)
    post_url = f"http://127.0.0.1:8000/post/{post_obj.pk}/"
    share_msg = f"Shared a post: {post_url}"
    Message.objects.create(sender=request.user, receiver=receiver, content=share_msg)
    return JsonResponse({'status': 'success', 'message': f'Post shared with {username}'})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CallSession

from django.views.decorators.csrf import csrf_exempt

@login_required
def random_video_call(request):
    return render(request, 'video_chat.html')

@login_required
def get_random_stranger(request):
    my_peer_id = request.GET.get('peer_id')
    if not my_peer_id:
        return JsonResponse({'status': 'waiting'})

    # 1. Update current user's peer_id, is_available=True, is_busy=False
    session, created = CallSession.objects.get_or_create(user=request.user)
    if session.peer_id != my_peer_id or not session.is_busy:
        session.peer_id = my_peer_id
        session.is_available = True
        session.is_busy = False
        session.save()

    # If already matched securely, wait for the incoming call
    if session.is_busy:
        return JsonResponse({'status': 'waiting'})

    # 2. Find a random stranger who is is_available=True, is_busy=False, has a peer_id
    stranger = CallSession.objects.filter(
        is_available=True, 
        is_busy=False,
        peer_id__isnull=False
    ).exclude(user=request.user).order_by('?').first()

    if stranger:
        # Mark both as busy so no one else interrupts
        session.is_busy = True
        session.save()
        stranger.is_busy = True
        stranger.save()

        # Return stranger's peer_id and caller role
        return JsonResponse({
            'status': 'found', 
            'stranger_peer_id': stranger.peer_id,
            'stranger_name': stranger.user.username,
            'role': 'caller'
        })
    
    return JsonResponse({'status': 'waiting'})

@login_required
def reset_call_session(request):
    CallSession.objects.filter(user=request.user).update(is_available=True, is_busy=False)
    return JsonResponse({'status': 'ok'})

@csrf_exempt
@login_required
def cleanup_session(request):
    if request.method == "POST":
        CallSession.objects.filter(user=request.user).update(is_available=False, is_busy=False)
    return JsonResponse({'status': 'ok'})

@csrf_exempt
@login_required
def leave_call_session(request):
    if request.method == "POST":
        CallSession.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'ok'})

@login_required
def get_friends_list(request):
    friends = User.objects.filter(
        (Q(received_requests__from_user=request.user, received_requests__status='accepted') | 
         Q(sent_requests__to_user=request.user, sent_requests__status='accepted'))
    ).distinct().exclude(id=request.user.id)
    
    friends_data = []
    for f in friends:
        pic_url = f.profile.profile_pic.url if hasattr(f, 'profile') and f.profile.profile_pic else '/static/images/default.png'
        friends_data.append({'username': f.username, 'profile_pic': pic_url})
    return JsonResponse({'friends': friends_data})

# -----------------------------
# Dashboard & Chat
# -----------------------------
@login_required(login_url="login")
def dashboard(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    pending_reqs = FriendRequest.objects.filter(to_user=request.user, status='pending')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    context = {
        "profile": profile_obj,
        "pending_requests": pending_reqs,
        "notifications": notifications,
    }
    if request.user.is_superuser:
        context["users"] = User.objects.all()
        context["total_users"] = User.objects.count()
    return render(request, "dashboard.html", context)

@login_required
def chat_room(request, username):
    other_user = get_object_or_404(User, username=username)
    Message.objects.filter(receiver=request.user, sender=other_user, is_read=False).update(is_read=True)
    is_friend = FriendRequest.objects.filter(
        (Q(from_user=request.user, to_user=other_user) | Q(from_user=other_user, to_user=request.user)),
        status='accepted'
    ).exists()

    if not is_friend: return redirect('home')

    if request.method == "POST":
        content = request.POST.get('message')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat_room', username=username)

    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp')
    return render(request, 'chat.html', {'other_user': other_user, 'messages': messages})

@login_required
def inbox(request):
    friends = User.objects.filter(
        (Q(received_requests__from_user=request.user, received_requests__status='accepted') | 
         Q(sent_requests__to_user=request.user, sent_requests__status='accepted'))
    ).distinct().exclude(id=request.user.id)
    return render(request, 'inbox.html', {'friends': friends})

@login_required
def check_unread_messages(request):
    unread_exists = Message.objects.filter(receiver=request.user, is_read=False).exists()
    return JsonResponse({'has_unread': unread_exists})

# -----------------------------
# Friend Request Actions
# -----------------------------
@login_required
def send_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if to_user != request.user:
        FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def accept_request(request, request_id):
    friend_req = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_req.status = 'accepted'
    friend_req.save()
    profile_sent, _ = Profile.objects.get_or_create(user=friend_req.from_user)
    profile_accepted, _ = Profile.objects.get_or_create(user=friend_req.to_user)
    profile_sent.followers.add(friend_req.to_user)
    profile_accepted.followers.add(friend_req.from_user)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect('dashboard')

# -----------------------------
# Profile & Post Edit
# -----------------------------
@login_required
def edit_profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile_obj)
        cropped_data = request.POST.get('profile_pic_data') 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save() 
            if cropped_data and ';base64,' in cropped_data:
                format, imgstr = cropped_data.split(';base64,') 
                ext = format.split('/')[-1] 
                data = ContentFile(base64.b64decode(imgstr), name=f'user_{request.user.id}.{ext}')
                profile_obj.profile_pic.save(data.name, data, save=True)
            return redirect("dashboard") 
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)
    return render(request, "edit_profile.html", {"u_form": u_form, "p_form": p_form, "profile": profile_obj})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all(): 
        post.likes.remove(request.user)
        liked = False
    else: 
        post.likes.add(request.user)
        liked = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'liked': liked, 'total_likes': post.likes.count()})
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("home")
    return render(request, "create_post.html", {"form": PostForm()})

# -----------------------------
# Auth Views
# -----------------------------
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("dashboard")
    return render(request, "register.html", {"form": UserCreationForm()})

def login_page(request):
    if request.method == "POST":
        u, p = request.POST.get("username"), request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect("login")