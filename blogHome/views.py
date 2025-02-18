from django.shortcuts import get_object_or_404, render
from django.shortcuts import HttpResponse
from .models import BlogPost
# Create your views here.

def blogHome(request):
    allBlogs=BlogPost.objects.all()
    return render(request, 'blogHome/bloghome.html',{'blogs':allBlogs})

def blogPage(request,slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blogHome/blogpage.html',{'blog':blog})
