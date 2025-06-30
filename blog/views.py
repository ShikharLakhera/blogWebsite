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
from django.contrib.auth.mixins import LoginRequiredMixin
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

        from django.conf import settings
        print(">>> Active DEFAULT_FILE_STORAGE:", settings.DEFAULT_FILE_STORAGE)

        from django.core.files.storage import default_storage
        print(default_storage.__class__)
        # Should show: cloudinary_storage.storage.MediaCloudinaryStorage

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

from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
from django.conf import settings
from PIL import Image
import os
import uuid
from .models import Profile  # Adjust import based on your app structure

#this is for development
@method_decorator(csrf_protect, name='dispatch')
# class updateProfilePic(LoginRequiredMixin, View):
#     """
#     Class-based view for handling profile picture updates
#     """
    
#     def post(self, request, *args, **kwargs):
#         try:
#             # Check if file was uploaded
#             if 'profile_picture' not in request.FILES:
#                 return JsonResponse({
#                     'status': 'error',
#                     'message': 'No file uploaded'
#                 }, status=400)
            
#             uploaded_file = request.FILES['profile_picture']
            
#             # Validate file type
#             if not uploaded_file.content_type.startswith('image/'):
#                 return JsonResponse({
#                     'status': 'error',
#                     'message': 'Invalid file type. Please upload an image.'
#                 }, status=400)
            
#             # Validate file size (5MB limit)
#             if uploaded_file.size > 5 * 1024 * 1024:
#                 return JsonResponse({
#                     'status': 'error',
#                     'message': 'File size too large. Maximum size is 5MB.'
#                 }, status=400)
            
#             # Get user profile (should exist since user is logged in)
#             try:
#                 profile = Profile.objects.get(user=request.user)
#             except Profile.DoesNotExist:
#                 # Create profile if it doesn't exist
#                 profile = Profile.objects.create(user=request.user)
            
#             # Delete old profile picture if it exists and isn't the default
#             if profile.profile_pic and hasattr(profile.profile_pic, 'path'):
#                 try:
#                     # Check if it's not the default image before deleting
#                     if profile.profile_pic.name != 'profile_pic/defpic.png':
#                         default_storage.delete(profile.profile_pic.name)
#                 except Exception as e:
#                     # Log the error but don't fail the upload
#                     print(f"Error deleting old profile picture: {e}")
            
#             # Process and save the new image
#             processed_file = self.process_image(uploaded_file)
            
#             # Generate unique filename
#             file_extension = os.path.splitext(uploaded_file.name)[1].lower()
#             if not file_extension:
#                 file_extension = '.jpg'
            
#             filename = f"profile_pic/{request.user.id}_{uuid.uuid4().hex}{file_extension}"
            
#             # Save the processed image
#             saved_path = default_storage.save(filename, processed_file)
            
#             # Update profile
#             profile.profile_pic = saved_path
#             profile.save()
            
#             # Return success response with new image URL
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Profile picture updated successfully',
#                 'new_image_url': profile.profile_pic.url
#             })
            
#         except Profile.DoesNotExist:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': 'Profile not found'
#             }, status=404)
            
#         except Exception as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': f'An error occurred: {str(e)}'
#             }, status=500)
    
#     def process_image(self, uploaded_file):
#         """
#         Process the uploaded image - resize and optimize
#         """
#         try:
#             # Open the image
#             image = Image.open(uploaded_file)
            
#             # Convert to RGB if necessary (handles RGBA, P mode images)
#             if image.mode in ('RGBA', 'P', 'LA'):
#                 # Create a white background
#                 background = Image.new('RGB', image.size, (255, 255, 255))
#                 if image.mode == 'P':
#                     image = image.convert('RGBA')
#                 background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
#                 image = background
#             elif image.mode != 'RGB':
#                 image = image.convert('RGB')
            
#             # Resize image to a reasonable size (e.g., 400x400)
#             max_size = (400, 400)
#             image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
#             # Create a square image by cropping from center
#             width, height = image.size
#             size = min(width, height)
#             left = (width - size) // 2
#             top = (height - size) // 2
#             right = left + size
#             bottom = top + size
            
#             image = image.crop((left, top, right, bottom))
            
#             # Save processed image to a BytesIO object
#             from io import BytesIO
#             output = BytesIO()
#             image.save(output, format='JPEG', quality=85, optimize=True)
#             output.seek(0)
            
#             # Create a Django File object
#             from django.core.files.base import ContentFile
#             return ContentFile(output.getvalue())
            
#         except Exception as e:
#             # If processing fails, return original file
#             uploaded_file.seek(0)
#             return uploaded_file
    
#     def is_default_image(self, image_name):
#         """
#         Check if the image is the default image
#         """
#         return image_name == 'profile_pic/defpic.png'
    
#     def get(self, request, *args, **kwargs):
#         """
#         Handle GET requests - return method not allowed
#         """
#         return JsonResponse({
#             'status': 'error',
#             'message': 'Method not allowed'
#         }, status=405)

#this is for production
@method_decorator(csrf_protect, name='dispatch')
class updateProfilePic(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            # Debug: Check what storage is being used
            from django.conf import settings
            from django.core.files.storage import default_storage
            print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
            print(f"Default storage class: {default_storage.__class__}")
            print(f"Cloudinary config exists: {'cloudinary' in dir()}")
            
            if 'profile_picture' not in request.FILES:
                return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)
            
            # Debug: Check environment variables
            import os
            print(f"CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET')}")
            print(f"CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY', 'NOT SET')}")
            print(f"CLOUDINARY_API_SECRET: {'SET' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET'}")
            
            uploaded_file = request.FILES['profile_picture']
            
            # Validate file type
            if not uploaded_file.content_type.startswith('image/'):
                return JsonResponse({'status': 'error', 'message': 'Invalid file type. Please upload an image.'}, status=400)
            
            # Validate file size (5MB max)
            if uploaded_file.size > 5 * 1024 * 1024:
                return JsonResponse({'status': 'error', 'message': 'File size too large. Max is 5MB.'}, status=400)
            
            # Get or create profile
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            # Delete old image if it exists and is not the default
            if profile.profile_pic and 'defpic.png' not in profile.profile_pic.name:
                try:
                    profile.profile_pic.delete(save=False)
                except Exception as e:
                    print(f"Error deleting old image: {e}")
            
            # Save new image directly to Cloudinary
            profile.profile_pic.save(uploaded_file.name, uploaded_file, save=True)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Profile picture updated successfully',
                'new_image_url': profile.profile_pic.url
            })
            
        except Exception as e:
            print(f"Profile picture update error: {e}")
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=500)