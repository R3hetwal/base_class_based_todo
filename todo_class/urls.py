from todo_class import views
from django.urls import path
from todo_class.views import *
# from django.views.generic import TemplateView

urlpatterns = [
    path('forbidden/', ForbiddenPageView.as_view(), name='forbidden'),
    path('pagenotfound/', PageNotFoundView.as_view(), name='pagenotfound'),
    path('tasks/', views.TaskList.as_view(), name = 'todos'),
    # path("todo-list/", views.TaskList.as_view(), name = 'todo-list'), # To display in home url
    path("todo-create/", views.TaskCreate.as_view(), name = 'todo-create'),
    # path('todo/<int:pk>/', views.TaskDetail.as_view(), name='todo'),
    path("todo-delete/<int:pk>/", views.TaskDelete.as_view(), name = 'todo-delete'),
    path("todo-update/<int:pk>/", views.TaskUpdate.as_view(), name = 'todo-update'),

]