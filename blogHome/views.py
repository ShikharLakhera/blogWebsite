from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.shortcuts import HttpResponse , redirect
from django.urls import reverse_lazy
from django.views import View
from .models import BlogPost , Comment
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .forms import BlogForm
# Create your views here.

def blogHome(request):
    allBlogs=BlogPost.objects.all()
    return render(request, 'blogHome/bloghome.html',{'blogs':allBlogs})

def blogPage(request,slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    comments=Comment.objects.filter(post=blog)
    #blog.content=mark_safe(blog.content)
    return render(request, 'blogHome/blogpage.html',{'blog':blog,'comments':comments})

@login_required
def commentHandler(request, post_id):
    # Fetch the blog post
    post = get_object_or_404(BlogPost, sno=post_id)
    print(f"Post: {post}")  # Debugging: Print the post

    if request.method == 'POST':
        # Get the content and parent_id from the form
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        print(f"Content: {content}")  # Debugging: Print the content
        print(f"Parent ID: {parent_id}")  # Debugging: Print the parent_id

        if content:
            parent_comment = None
            if parent_id:  # If parent_id is provided, fetch the parent comment
                try:
                    parent_comment = Comment.objects.get(sno=int(parent_id))  # Convert parent_id to integer
                    #print(f"Parent Comment: {parent_comment}")  # Debugging: Print the parent comment
                except (Comment.DoesNotExist, ValueError):
                    # Handle invalid parent_id (e.g., log the error or show a message)
                    print(f"Invalid parent_id: {parent_id}")

            # Create the comment
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                content=content,
                parent=parent_comment
            )
            print(f"Comment Created: {comment}")  # Debugging: Print the created comment

    # Redirect to the blog page using the post's slug
    return redirect(reverse_lazy("blogHome:blogPage", args=[post.slug]))

class editView(View):
    def get(self, request, slug):
        print('get')
        blog = get_object_or_404(BlogPost, slug=slug)
        
        if request.user != blog.author:
            return HttpResponseForbidden()
        
        form = BlogForm(instance=blog)
        
        return render(request, 'blogHome/blogedit.html', {
            'form': form,
            'blog': blog,
            'slug': blog.slug,
            'sno': blog.sno
        })
    
    def post(self, request, slug):
        print('post')
        blog = get_object_or_404(BlogPost, slug=slug)
        
        if request.user != blog.author:
            return HttpResponseForbidden()
        
        form = BlogForm(request.POST, instance=blog)
        
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('blogHome:blogPage', kwargs={'slug': blog.slug}))
        else:
            # Form is invalid, render template with form errors and submitted data
            return render(request, 'blogHome/blogedit.html', {
                'form': form,  # This contains the submitted data and errors
                'blog': blog,
                'slug': blog.slug,
                'sno': blog.sno
            })