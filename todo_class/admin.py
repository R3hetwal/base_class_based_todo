from django.contrib import admin

# Register your models here.
from django.contrib import admin
from todo_class.models import Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'complete', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at', 'updated_at', 'complete')

admin.site.register(Task, TaskAdmin)