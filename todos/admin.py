from django.contrib import admin
from .models import Task, TasksList

# Register your models here.
admin.site.register(Task)
admin.site.register(TasksList)