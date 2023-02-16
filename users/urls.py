# from django import views
from django.urls import path, include
from todo_class import views
from users.views import login_view, signup_view, logout_view, password_change_view, ForbiddenPageView, user_details_change
from todo_class.views import *

urlpatterns = [ 
    path('', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path("tasks/", include("todo_class.urls")),
    path("logout/", logout_view, name='logout'),
    path("changepassword/", password_change_view, name='changepassword'),
    path('forbidden/', ForbiddenPageView.as_view(), name='forbidden'),
    path("changeuser/", user_details_change, name='changeuser'),

]

