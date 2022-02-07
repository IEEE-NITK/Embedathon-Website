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

    path('update-max-task/', views.update_max_task, name="update-max-task"),
]
