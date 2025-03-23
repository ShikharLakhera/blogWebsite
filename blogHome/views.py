from django.shortcuts import get_object_or_404, render
from django.shortcuts import HttpResponse , redirect
from django.urls import reverse_lazy
from .models import BlogPost , Comment
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
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
