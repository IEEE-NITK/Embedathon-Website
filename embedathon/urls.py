from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.team_home, name="homepage"),
    path('register-team/', views.register_team, name="register-team"),
    path('join-team/', views.join_team, name="join-team"),
    path('leave-team/', views.leave_team, name="leave-team"),
    path('team-profile/', views.team_profile, name="team-profile"),
    path('update-address/', views.update_address, name="update-address"),
    path('update-teamname/', views.update_teamname, name="update-teamname"),
    path('user-profile/', views.user_profile, name="user-profile"),
    path('update-details/', views.update_details, name="update-details"),
    path('update-password/', views.update_password, name="update-password"),
    path('task/<int:task_id>/', views.task_view, name="task"),

    path('update-max-task/', views.update_max_task, name="update-max-task"),
]
