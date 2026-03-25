from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('spotify_search/', views.spotify_search, name='spotify_search'),
    path('', views.landing_page, name='landing'),
    path('feed/', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.dashboard, name='profile'), 
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_page, name='logout'),
    path('search/', views.search_users, name='search_users'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('send-request/<int:user_id>/', views.send_request, name='send_request'),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('chat/<str:username>/', views.chat_room, name='chat_room'),
    # core/urls.py mein ye line honi chahiye
    path('inbox/', views.inbox, name='inbox'),
    path('check-unread/', views.check_unread_messages, name='check_unread_messages'),
    path('create-post/', views.create_post, name='create_post'),
    path('upload-story/', views.upload_story, name='upload_story'),
    # urls.py mein add karein
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('get-friends/', views.get_friends_list, name='get_friends_list'), # <--- Ye check karein
    path('share/<int:post_id>/<str:username>/', views.share_post, name='share_post'),
    path('video-call/', views.random_video_call, name='video_call'),
    path('get-random-stranger/', views.get_random_stranger, name='get_random_stranger'),
    path('reset-call-session/', views.reset_call_session, name='reset_call_session'),
    path('cleanup-call-session/', views.cleanup_session, name='cleanup_session'),
    path('leave-call-session/', views.leave_call_session, name='leave_call_session'),

    # NEW: Like post ka URL
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)