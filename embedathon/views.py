from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

import string
import random

from .models import *
from .helpers import team_check

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
            return render(request, 'embedathon/register.html', {
                'error': 'Username already exists!'
            }, status=400)

        login(request, user)
        return HttpResponseRedirect(reverse('register-team'))

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
@user_passes_test(team_check, login_url='/register-team/')
def team_home(request):
    user = request.user

    team = Team.objects.get(Q(leader=user) | Q(member=user))
    return render(request, 'embedathon/homepage.html', {
        "team": team
    })


@login_required
def register_team(request):
    if hasattr(request.user, 'team_leader') or hasattr(request.user, 'team_member'):
        return HttpResponseRedirect(reverse('homepage'))

    if request.method == 'POST':
        teamname = request.POST['teamname']
        leader = request.user

        isUniquePasscode = False
        passcode = ''
        while not isUniquePasscode:
            passcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if passcode not in list(Team.objects.values_list('passcode', flat=True)):
                isUniquePasscode = True

        try:
            team = Team.objects.create(teamname=teamname, leader=leader, passcode=passcode)

            team.save()
        except IntegrityError:
            return render(request, 'embedathon/choose-team.html', {
                'error': 'Team name already exists!'
            }, status=400)

        return HttpResponseRedirect(reverse('homepage'))

    return render(request, 'embedathon/choose-team.html')

@login_required
def join_team(request):
    if request.method == "POST":
        if hasattr(request.user, 'team_leader') or hasattr(request.user, 'team_member'):
            return HttpResponseRedirect(reverse('homepage'))

        passcode = request.POST['passcode'].upper()
        user = request.user
        try:
            team = Team.objects.get(passcode=passcode)
            team.member = user
            team.save()
        except Team.DoesNotExist:
            return render(request, 'embedathon/choose-team.html', {
                'error': 'Invalid passcode!'
            }, status=400)
        return HttpResponseRedirect(reverse('homepage'))

    return HttpResponseRedirect(reverse('homepage'))

@staff_member_required
def update_max_task(request):
    tasks = Task.objects.all()
    if request.method == "POST":
        try:
            task = Task.objects.get(pk=request.POST['task-id'])
            teams = Team.objects.all()

            for team in teams:
                if not team.disqualified:
                    team.max_task_visible = task
                    team.save()

            return render(request, 'embedathon/update-max-task.html', {
                'tasks': tasks,
                'message': 'Successfully updated max task!'
                })
        except:
            render(request, 'embedathon/update-max-task.html', {
                'tasks': tasks,
                'error': 'Invalid task id!'
                })



    return render(request, 'embedathon/update-max-task.html', {
        "tasks": tasks
        })
