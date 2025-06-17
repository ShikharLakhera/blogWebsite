from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    content=models.TextField()
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name + "["+str(self.timeStamp)+"]"

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.CharField(max_length=200 , null=True,blank=True)
    profile_pic=models.ImageField(upload_to='profile_pic/', default='profile_pic/defpic.png',)

    def __str__(self):
        return self.user.username