from django.shortcuts import render
from django.shortcuts import HttpResponse , redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm
from .models import Contact
from blogHome.models import BlogPost

# Create your views here.

def index(request):
    blogs=BlogPost.objects.all().order_by('-timeStamp')
    return render(request, 'blog/indexpage/index.html',{'posts':blogs})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        print(request.POST['phone'])
        if form.is_valid() and request.POST['phone'].isdigit() and len(request.POST['phone'])==10 :
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect(reverse_lazy('blog:contact'))  # Redirect to prevent duplicate submissions
        else :
            messages.error(request, "Please fill the form correctly")


    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

def about(request):
    return render(request, 'blog/about.html')

def search(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return redirect(reverse_lazy('blog:home'))  # Redirect to homepage if no query provided
    elif len(query)>80:
        #messages.error(request, "Search query is too long.")
        posts=BlogPost.objects.none()
    else:
        postsTitle=BlogPost.objects.filter(title__icontains=query)
        postBlog=BlogPost.objects.filter(content__icontains=query)
        posts=postsTitle.union(postBlog)

    return render(request, 'blog/search.html',{'results':posts,'query':query})