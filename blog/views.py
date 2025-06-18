import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import HttpResponse , redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm
from .models import Contact , Profile
from blogHome.models import BlogPost
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login ,logout 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        # fname=request.POST.get('first_name')
        # lname=request.POST.get('last_name')
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if(password1!=password2):
            messages.error(request, 'Passwords do not match')
            return render(request, "blog/signup.html", {
                "username": uname,
                "email": email
            })
        elif ( User.objects.filter(username=uname).exists()):
            messages.error(request, 'Username already in use .')
            return render(request, "blog/signup.html", {
                "username": uname,
                "email": email
            })
        elif(User.objects.filter(email=email).exists()):
            messages.error(request, 'email already in use .')
            return render(request, "blog/signup.html", {
                "username": uname,
                "email": email
            })
        else :
            myuser=User.objects.create_user(username=uname,email=email,password=password1)
            Profile.objects.create(user=myuser)
            #myprofile.save()
            myuser.save()
            messages.success(request, 'User created successfully')
            return redirect(reverse_lazy('blog:home'))  # Redirect to homepage if user created successfully


class loginhandle(View):
    def get(self,request):
        return render(request, 'blog/login.html')
    
    def post(self,request):

        uname=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=uname,password=password)

        if user is not None:
            login(request,user)
            return redirect(reverse_lazy('blog:home'))  # Redirect to homepage if user logged in successfully
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, "blog/login.html",{'email': uname})
        

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out')
    return redirect(reverse_lazy('blog:login'))  # Redirect to homepage if user logged out successfully

class profileView(View):
    def get(self, request, username):
        # Debugging print statements
        print(f"Looking for user with username: {username}")
        userobj=User.objects.filter(username=username).first()
        #userobj = get_object_or_404(User, username=username)
        print(f"Found user: {userobj}")  # Check if user exists

        profile=Profile.objects.filter(user=userobj).first()
        #profile = get_object_or_404(Profile, user=userobj)
        print(f"Found profile: {profile}") 
        blogs=BlogPost.objects.all().filter(author=userobj).order_by('-timeStamp')[:5]

        return render(request, 'blog/profile.html', {'profile': profile,'request_user': userobj ,'blogs':blogs})

class editBio(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            new_bio = data.get("bio", "").strip()
            
            if len(new_bio) > 200:
                return JsonResponse({"status": "error", "message": "Bio too long (max 200 characters)."})
            
            request.user.profile.bio = new_bio
            request.user.profile.save()
            
            return JsonResponse({"status": "success", "bio": new_bio})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

        return JsonResponse({"status": "error", "message": "Invalid request method."})
class viewAuthorProfile(View):
    def get(self,request,author):
        #author_obj=User.objects.filter(username=author)
        author_obj=get_object_or_404(User,username=author)
        blogs=BlogPost.objects.all().filter(author=author_obj).order_by('-timeStamp')[:5]
        ctx={'author':author_obj,'blogs':blogs}
        #return HttpResponse("Working")
        return render(request,'blog/authorProfile.html',ctx)
    
#creating blog with the help of api endpoint    

from .forms import CreateBlog

@method_decorator(login_required,name="dispatch")
class postBlog(View):
    def get(self, request):
        return render(request, 'blog/postingblog.html')

    
    def post(self, request):
        created_form = CreateBlog(request.POST)
    
        if created_form.is_valid():
            blog = created_form.save(commit=False)  # Don't save to DB yet
            blog.author = request.user  # Set the current user as author
            blog.save()  # Now save with author
            messages.success(request, 'Blog is posted')
            return redirect('blog:postBlog') 
        else:
            messages.error(request, "fill in data correctly!!")
            return render(request, 'blog/postingblog.html', {'form': created_form})