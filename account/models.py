from django.db import models

# Create your models here.

class User(models.Model):
    user_name=models.CharField(max_length=100, unique=True, null=False, default="username")
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    email=models.EmailField(max_length=70, unique=True, null=False, default="example@gmail.com")
    
    def __str__(self):
        return self.user_name+':'+self.name+':'+self.password+':'+self.email