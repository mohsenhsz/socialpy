from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CreatePostForm
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

@login_required(redirect_field_name='login')
def CreatePost(request, user_id):
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
