from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

import string
import random

from .models import *
from .helpers import team_check

# Create your views here.
def index(request):
    '''
    Landing page view. Accepts only GET requests.
    '''
    return render(request, 'embedathon/index.html')

def register_user(request):
    '''
    View to register a single user. Accepts GET and POST requests.
    '''
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
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

        # Try to create a user with the given credentials
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.save()
        # If DB encounters an IntegrityError, return webpage with error message
        except IntegrityError:
            return render(request, 'embedathon/register.html', {
                'error': 'Username already exists!'
            }, status=400)

        # Log the user in
        login(request, user)
        return HttpResponseRedirect(reverse('register-team'))

    return render(request, 'embedathon/register.html')

def login_user(request):
    '''
    Login Page view. Accepts GET and POST requests.
    '''
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
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
def user_profile(request):
    '''
    TEMP VIEW.
    '''
    user = request.user
    return HttpResponse(user.username)

@login_required
@user_passes_test(team_check, login_url='/register-team/')
def team_home(request):
    '''
    Home page view for a team. Accepts GET requests.
    User must be logged in and be a member of a team.
    '''
    user = request.user
    team = Team.objects.get(Q(leader=user) | Q(member=user))
    tasks = []
    if team.max_task_visible is not None:
        tasks = Task.objects.filter(id__lte=team.max_task_visible.id).order_by('id')

    if settings.HACKATHON_START:
        return render(request, 'embedathon/dashboard.html', {
            "team": team,
            "tasks": tasks
        })
    return render(request, 'embedathon/homepage.html', {
        "team": team,
        "tasks": tasks
    })

@login_required
@user_passes_test(team_check, login_url='/register-team/')
def team_profile(request):
    '''
    TEMP VIEW.
    '''
    return HttpResponse("Team Profile")

@login_required
@user_passes_test(team_check, login_url='/register-team/')
def task_view(request, task_id):
    '''
    Task view. Accepts GET requests.
    User must be logged in and be a member of a team.
    Takes task_id as a parameter.
    '''
    # Render a 404 page if requested task does not exist
    task = get_object_or_404(Task, pk=task_id)
    team = Team.objects.get(Q(leader=request.user) | Q(member=request.user))
    tasks = []
    if team.max_task_visible is not None:
        tasks = Task.objects.filter(id__lte=team.max_task_visible.id).order_by('id')

    # Render a 404 page if requested task is not visible to the team
    if team.max_task_visible is None or team.max_task_visible.id < task.id:
        raise Http404()
    return render(request, "embedathon/task.html", {
        "task": task,
        "tasks": tasks
        })

@login_required
def register_team(request):
    '''
    View to register a team. Accepts GET and POST requests.
    '''
    # If user is already part of a team, redirect to homepage
    if hasattr(request.user, 'team_leader') or hasattr(request.user, 'team_member'):
        return HttpResponseRedirect(reverse('homepage'))

    if request.method == 'POST':
        teamname = request.POST['teamname']
        leader = request.user

        # Generate a unique 6 character team code
        isUniquePasscode = False
        passcode = ''
        while not isUniquePasscode:
            passcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if passcode not in list(Team.objects.values_list('passcode', flat=True)):
                isUniquePasscode = True

        # Try to create a team with the given credentials
        try:
            team = Team.objects.create(teamname=teamname, leader=leader, passcode=passcode)
            team.save()
        # If DB encounters an IntegrityError, return webpage with error message
        except IntegrityError:
            return render(request, 'embedathon/choose-team.html', {
                'error': 'Team name already exists!'
            }, status=400)

        return HttpResponseRedirect(reverse('homepage'))

    return render(request, 'embedathon/choose-team.html')

@login_required
def join_team(request):
    '''
    View to join a team. Accepts POST requests.
    '''
    if request.method == "POST":
        # If user is already part of a team, redirect to homepage
        if hasattr(request.user, 'team_leader') or hasattr(request.user, 'team_member'):
            return HttpResponseRedirect(reverse('homepage'))

        passcode = request.POST['passcode'].upper()
        user = request.user
        try:
            team = Team.objects.get(passcode=passcode)

            # Ensure that team is not already full
            if team.member is not None:
                raise Exception("Team is full")
            team.member = user
            team.save()
        except:
            return render(request, 'embedathon/choose-team.html', {
                'error': 'Invalid passcode!'
            }, status=400)

    return HttpResponseRedirect(reverse('homepage'))

@login_required
@user_passes_test(team_check, login_url='/register-team/')
def leave_team(request):
    '''
    View for user to join a new team. Accepts GET and POST requests.
    User must be logged in and be a member of a team.
    '''
    user = request.user
    team = Team.objects.get(Q(leader=user) | Q(member=user))

    if request.method == "POST":
        passcode = request.POST['passcode'].upper()
        # Check if passcode is valid
        try:
            newTeam = Team.objects.get(passcode=passcode)
        except:
            return render(request, 'embedathon/leave-team.html', {
                "team": team,
                "error": "Invalid passcode!"
                })
        # Check if team is empty
        if newTeam.member != None:
            return render(request, 'embedathon/leave-team.html', {
                "team": team,
                "error": "Team is full!"
                })
        # If user is second teammate, just remove them
        if user == team.member:
            team.member = None
            team.save()
        # If user is leader and second teammate does not exist, delete the team
        elif team.member == None:
            team.delete()
        # User is leader and second teammate exists, promote second teammate to leader
        else:
            team.leader = team.member
            team.member = None
            team.save()

        newTeam.member = user
        newTeam.save()

        return HttpResponseRedirect(reverse('homepage'))

    return render(request, 'embedathon/leave-team.html', {
        "team": team
        })

@staff_member_required
def update_max_task(request):
    '''
    View to update max task for all non-disqualified candidates.
    User must be logged in and be a staff member.
    '''
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
