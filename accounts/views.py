from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import Post
from django.contrib.auth.decorators import login_required



def UserRegister(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                                            username=cd['username'],
                                            email=cd['email'],
                                            password=cd['password1']
                                            )
            messages.success(request, f'Your account created successfully', 'success')
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterationForm
    return render(request, 'accounts/register.html', {'form':form})


def UserLogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'], password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request, f'You logged in successfully', 'success')
                return redirect('index')
            else:
                messages.error(request, f'username or password is wrong', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form':form})

@login_required(redirect_field_name='login')
def UserLogout(request):
    logout(request)
    messages.success(request, f'You logged out successfully', 'success')
    return redirect('index')

@login_required(redirect_field_name='login')
def UserProfile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    self_profile = False
    if request.user == user:
        self_profile = True
    context = {'user':user, 'posts':posts, 'self_profile':self_profile}
    return render(request, 'accounts/profile.html', context)
