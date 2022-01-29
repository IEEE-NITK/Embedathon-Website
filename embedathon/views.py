from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth import login
from django.urls import reverse

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
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'embedathon/register.html')
