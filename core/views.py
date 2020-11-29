from django.shortcuts import render, get_object_or_404
from .models import Post


def AllPosts(request):
    posts = Post.objects.all()
    return render(request, 'core/index.html', {'posts':posts})


def PostDetails(request, year, month, day, slug):
    post = get_object_or_404(Post, publish_date__year=year,
                             publish_date__month=month, publish_date__day=day, slug=slug)
    return render(request, 'core/post_datails.html', {'post':post})
