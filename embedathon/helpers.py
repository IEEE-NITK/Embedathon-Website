def team_check(user):
    return hasattr(user, 'team_leader') or hasattr(user, 'team_member_1') or hasattr(user, 'team_member_2')
