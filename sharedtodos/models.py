from django.db import models
from account.models import User
from todos.models import TasksList
# Create your models here.
class SharedTasksList(models.Model):
    sharedtaskslist=models.ForeignKey(TasksList, on_delete=models.CASCADE)
    withuser=models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.sharedtaskslist.id)+':'+self.sharedtaskslist.list_name+':'+self.withuser.name