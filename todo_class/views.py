from django.shortcuts import render, redirect
from todo_class.models import Task
from django.views import View
from todo_class.forms import *
from django.http import HttpResponse

# Create your views here.
class ErrorPageView(View):
    def get(self, request):
        return render(request, 'errors/403.html', status=403)

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
            task = Task.objects.get(id=pk, user=request.user.id)
        except Task.DoesNotExist:
            return redirect('forbidden')

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
            task = Task.objects.get(id=pk, user=request.user.id)
        except Task.DoesNotExist:
            error_page_view = ErrorPageView.as_view()
            return redirect('forbidden')

        task = Task.objects.get(id=pk, user=request.user.id)
        context = {'task':task}   
        return render(request, 'todo_delete.html', context)

    def post(self, request, pk):
        task = Task.objects.get(id=pk, user=request.user.id)
        task.delete()
        return redirect('todos')