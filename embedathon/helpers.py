def team_check(user):
    return hasattr(user, 'team_leader') or hasattr(user, 'team_member')
