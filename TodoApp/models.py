from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Title = models.CharField(max_length=255,null=False,blank=False)
    Description  = models.TextField(null=True,blank=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    CompletionDate = models.DateTimeField()
    completionStatus  = models.BooleanField(default=False)
    IsDelete = models.BooleanField(default=False)