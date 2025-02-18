from django.db import models

class BlogPost(models.Model):

    sno=models.AutoField(primary_key=True)
    content=models.TextField()
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=25)
    timeStamp=models.DateTimeField(blank=True)
    slug=models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
