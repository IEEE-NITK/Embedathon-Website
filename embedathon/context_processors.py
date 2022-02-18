from django.conf import settings
from django.db.models import Q

from .models import Team

def general(request):
    userInTeam = False
    if request.user.is_authenticated:
        try:
            team = Team.objects.get(Q(leader=request.user) | Q(member=request.user))
            if team is not None:
                userInTeam = True
        except:
            pass
    return {
        'hackathon_start': settings.HACKATHON_START,
        'user_in_team': userInTeam
    }
