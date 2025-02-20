from django.shortcuts import render
from django.shortcuts import HttpResponse , redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm
from .models import Contact
from blogHome.models import BlogPost
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login

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

class handleSignup(View):
    def get(self, request):
        return render(request, 'blog/signup.html')
    
    def post(self, request):
        fname=request.POST.get('first_name')
        lname=request.POST.get('last_name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if(password1!=password2):
            messages.error(request, 'Passwords do not match')
            return render(request, "signup.html", {
                "first": fname,
                "last": lname,
                "email": email
            })
        elif ( User.objects.filter(username=email).exists()):
            messages.error(request, 'email already in use .')
            return render(request, "signup.html", {
                "first": fname,
                "last": lname,
                "email": email
            })
        else :
            myuser=User.objects.create_user(username=email,email=email,password=password1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            messages.success(request, 'User created successfully')
            return redirect(reverse_lazy('blog:signup'))  # Redirect to homepage if user created successfully

        return render(request, 'blog/indexpage/index.html')

class loginhandle(View):
    def get(self,request):
        return render(request, 'blog/login.html')
    
    def post(self,request):

        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(username=email,password=password)

        if user is not None:
            login(request,user)
            messages.success(request, 'You are now logged in')
            return redirect(reverse_lazy('blog:home'))  # Redirect to homepage if user logged in successfully
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, "blog/login.html",{'email': email})