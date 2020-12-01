from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CreatePostForm, EditPostForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

def AllPosts(request):
    posts = Post.objects.all()
    return render(request, 'core/index.html', {'posts':posts})


def PostDetails(request, year, month, day, slug):
    post = get_object_or_404(Post, publish_date__year=year,
                             publish_date__month=month, publish_date__day=day, slug=slug)
    return render(request, 'core/post_datails.html', {'post':post})

@login_required
def CreatePost(request, user_id):
    """ next is the url that the user requested before logging in  """
    if request.user.id == user_id:
        if request.method == 'POST':
            form = CreatePostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.slug = slugify(form.cleaned_data['content'][:30], allow_unicode=True)
                new_post.save()
                messages.success(request, f'post created successfully', 'success')
                return redirect('profile', user_id)
            else:
                messages.error(request, f'ops post dont save correctly. please try again!', 'danger')
        else:
            form = CreatePostForm
        return render(request, 'core/create_post.html', {'form':form})
    else:
        return redirect('index')

@login_required
def DeletePost(request, user_id, post_id):
    if request.user.id == user_id:
        post = Post.objects.filter(pk=post_id)
        post.delete()
        messages.success(request, 'Your post deleted successfully.', 'success')
        return redirect('profile', user_id)
    else:
        return redirect('profile', request.user.id)

@login_required()
def EditPost(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, pk=post_id)
        if request.method =='POST':
            form = EditPostForm(request.POST, instance=post)
            if form.is_valid():
                post.slug = slugify(form.cleaned_data['content'][:30])
                form.save()
                messages.success(request, 'Your post edited successfully', 'success')
                return redirect('post_details', post.publish_date.year, post.publish_date.month,
                                 post.publish_date.day, post.slug)
        else:
            form = EditPostForm(instance=post)
            return render(request, 'core/edit_post.html', {'form':form})
    else:
        return redirect('index')
