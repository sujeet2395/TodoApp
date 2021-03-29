from django.db import models
from account.models import User
# Create your models here.
class TasksList(models.Model):
    list_name=models.CharField(max_length=30)
    descriptions=models.CharField(max_length=200)
    status=models.CharField(max_length=20)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.list_name+': '+self.descriptions+': created by '+str(self.user.id)+':'+self.user.name+': now status is '+self.status

class Task(models.Model):
    title=models.CharField(max_length=30)
    descriptions=models.CharField(max_length=200)
    status=models.CharField(max_length=20)
    created=models.DateTimeField()
    taskslist=models.ForeignKey(TasksList,on_delete=(models.CASCADE))
    
    def __str__(self):
        return self.title+':'+self.descriptions+':'+str(self.created)+':'+self.status+':'+self.taskslist.list_name