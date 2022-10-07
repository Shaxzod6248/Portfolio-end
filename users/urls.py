from django.urls import path
from .views import *


urlpatterns = [
    path("", profiles, name="profiles"),
    path("login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", logout_user, name="logout"),
    path("account/", account, name="account"),
    path("account_edit/", account_edit, name="account_edit"),
    path("profiles/<str:pk>/", profile, name="profile"),
    path('inbox/', inbox, name="inbox"),
    path('message/<str:pk>/', viewMessage, name="message"),
    path('create-message/<str:pk>/', createMessage, name="create-message"),
    path('create-skill/', createSkill, name="create-skill"),
    path('update-skill/<str:pk>/', updateSkill, name="update-skill"),
    path('delete-skill/<str:pk>/', deleteSkill, name="delete-skill"),
]