from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_page(request):

    # अगर user पहले से login है
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "dashboard.html")


def logout_page(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "base.html")