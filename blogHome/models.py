import bleach
from django.db import models
from django.contrib.auth.models import User


# ALLOWED_TAGS = [
#     'p', 'br', 'b', 'i', 'u', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre',
#     'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'img', 'table', 'tr', 'td', 'th'
# ]
# ALLOWED_ATTRIBUTES = {
#     'a': ['href', 'title', 'target'],
#     'img': ['src', 'alt', 'width', 'height'],
#     'span': ['style'],
#     'div': ['style'],
#     'p': ['style']
# }
# ALLOWED_STYLES = ['color', 'font-weight', 'text-decoration']

class BlogPost(models.Model):

    sno=models.AutoField(primary_key=True)
    content=models.TextField()
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=25)
    timeStamp=models.DateTimeField(blank=True,auto_now_add=True)
    slug=models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
    # def save(self, *args, **kwargs):
    #     # Sanitize the content before saving
    #     self.content = bleach.clean(self.content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
    #     super().save(*args, **kwargs)

class Comment(models.Model):
    sno=models.AutoField(primary_key=True)
    content=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    timeStamp=models.DateTimeField(auto_now_add=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,related_name='replies',default=None,null=True)

    def __str__(self):
        return self.content[0:10]+'...'+'By'+self.user.username
    
    @property
    def is_parent(self):
        """Check if the comment is a parent (i.e., not a reply)."""
        return self.parent is None
