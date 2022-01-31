from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.
def index(request):
    return render(request, 'embedathon/index.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']

        # Ensure password matches confirmation
        if password != request.POST["confirmation"]:
            return render(request, "embedathon/register.html", {
                "error": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'error': 'Username already exists'
            }, status=400)

        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))

    return render(request, 'embedathon/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, 'embedathon/login.html', {
                "error": "Invalid username or password."
            })

    return render(request, 'embedathon/login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def team_home(request):
    return render(request, 'embedathon/homepage.html')
