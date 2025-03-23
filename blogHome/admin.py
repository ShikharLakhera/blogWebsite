from django.contrib import admin
from .models import BlogPost , Comment
# Register your models here.

admin.site.register(Comment)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    class Media:
        js=('blogHome/js/tinymce.js',)
