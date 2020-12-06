from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Vote
from .forms import CreatePostForm, EditPostForm, AddCommentForm, ReplyCommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

def AllPosts(request):
    posts = Post.objects.all()
    return render(request, 'core/index.html', {'posts':posts})


def PostDetails(request, post_id, year, month, day, slug):
    post = get_object_or_404(Post, pk=post_id , publish_date__year=year,
                             publish_date__month=month, publish_date__day=day, slug=slug)
    comments = Comment.objects.filter(post=post, is_reply=False)
    can_like = False
    if request.user.is_authenticated:
        if post.user_can_like(request.user):
            can_like = True
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'your comment submitted successfully')
            return redirect('post_details', post_id, year, month, day, slug)
    else:
        reply_form = ReplyCommentForm()
        form = AddCommentForm()
    return render(request, 'core/post_datails.html', {'post':post, 'comments':comments, 'form':form,
                                                      'reply_form':reply_form, 'can_like':can_like})


@login_required
def CreatePost(request, user_id):
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
            form = CreatePostForm()
        return render(request, 'core/create_post.html', {'form':form})
    else:
        return redirect('profile', request.user.id)

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


@login_required
def ReplyComment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        form = ReplyCommentForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'Your comment submitted successfully', 'success')
    return redirect('post_details', post.id, post.publish_date.year, post.publish_date.month,
                        post.publish_date.day, post.slug)

@login_required
def LikePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Vote(user=request.user, post=post)
    like.save()
    messages.success(request, 'Liked successfully', 'success')
    return redirect('post_details', post.id, post.publish_date.year, post.publish_date.month,
                        post.publish_date.day, post.slug)


def DislikePost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like = Vote.objects.get(user=request.user, post=post)
    like.delete()
    messages.success(request, 'Disliked successfully', 'success')
    return redirect('post_details', post.id, post.publish_date.year, post.publish_date.month,
                        post.publish_date.day, post.slug)
