from django.shortcuts import render, redirect
from todo_class.models import Task
from django.views import View
from todo_class.forms import *
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


# Create your views here.
class ForbiddenPageView(View):
    def get(self, request):
        return render(request, 'errors/403.html', status=403)

class PageNotFoundView(View):
    def get(self, request):
        return render(request, 'errors/404.html', status=404)


class TaskList(View):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user.id)
        count = tasks.filter(complete=False).count()

        search_input = request.GET.get('search-area') or ''
        if search_input:
            tasks = tasks.filter(title__contains=search_input)

        context = {'tasks': tasks,
                    'count': count,
                    'search_input': search_input}
    
        return render(request, 'todo_list.html', context)

  
class TaskCreate(View):
    def get(self, request):
        form = CreateForm()
        return render(request, 'todo_create.html', {'form': form})

    def post(self, request):
        form = CreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('todos')

class TaskUpdate(View):
    def get(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
            try:
                if task.user != request.user:
                    raise PermissionDenied
            except PermissionDenied:
                return redirect('forbidden')
        except Task.DoesNotExist:
            return redirect('pagenotfound')

        form = UpdateForm(instance=task)
        context = {'form': form}
        return render(request, 'todo_update.html', context)

    def post(self, request, pk):
        task = Task.objects.get(id=pk, user=request.user.id)
        form = UpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todos')

class TaskDelete(View):
    def get(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
            try:
                if task.user != request.user:
                    raise PermissionDenied
            except PermissionDenied:
                return redirect('forbidden')
                
        except Task.DoesNotExist:
            return redirect('pagenotfound')

        task = Task.objects.get(id=pk, user=request.user.id)
        context = {'task':task}   
        return render(request, 'todo_delete.html', context)

    def post(self, request, pk):
        task = Task.objects.get(id=pk, user=request.user.id)
        task.delete()
        return redirect('todos')