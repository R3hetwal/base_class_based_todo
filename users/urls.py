# from django import views
from django.urls import path, include
from todo_class import views
from users.views import login_view, signup_view, logout_view
from todo_class.views import *

urlpatterns = [ 
    # path('pagenotfound/', error_404_view, name='pagenotfound'),
    path('', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path("tasks/", include("todo_class.urls")),
    path("logout/", logout_view, name='logout'),
]

