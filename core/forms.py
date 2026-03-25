from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post, Story

# -----------------------------
# 1. User Info Update Form
# -----------------------------
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']


# -----------------------------
# 2. Profile Info Update Form
# -----------------------------
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3, 
            'placeholder': 'Apne baare mein kuch likhein...'
        })
    )

    class Meta:
        model = Profile
        fields = ['bio']


# -----------------------------
# 3. Post Creation Form
# -----------------------------
class PostForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    caption = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 2, 
            'placeholder': 'Write a caption...'
        })
    )

    class Meta:
        model = Post
        fields = ['image', 'caption']


# -----------------------------
# 4. Story Upload Form (Updated)
# -----------------------------
class StoryUploadForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    music = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'audio/*'})
    )
    caption = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Story caption (Optional)...'
        })
    )

    class Meta:
        model = Story
        fields = ['image', 'music', 'caption']