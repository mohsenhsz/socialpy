from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import (UserLoginForm, UserRegisterationForm, EditProfileForm, GetPhoneNumberForm,
                    VerifyPhoneForm, ResetPasswordConfirmForm)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import Post
from accounts.models import Profile, Relation
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from kavenegar import *
from random import randint


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
        form = UserRegisterationForm()
    return render(request, 'accounts/register.html', {'form':form})


def UserLogin(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'], password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request, f'You logged in successfully', 'success')
                if next:
                    return redirect(next)
                return redirect('index')
            else:
                messages.error(request, f'username or password is wrong', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form':form})


@login_required
def UserLogout(request):
    logout(request)
    messages.success(request, f'You logged out successfully', 'success')
    return redirect('index')


@login_required
def UserProfile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    self_profile = False
    if request.user == user:
        self_profile = True
    is_following = False
    is_relation = Relation.objects.filter(from_user=request.user, to_user=user)
    if is_relation.exists():
        is_following = True
    context = {'user':user, 'posts':posts, 'self_profile':self_profile, 'is_following':is_following}
    return render(request, 'accounts/profile.html', context)


@login_required
def EditProfile(request, user_id):
    if request.user.id == user_id:
        user = get_object_or_404(User, pk=user_id)
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=user.profile)
            if form.is_valid():
                form.save()
                user.email = form.cleaned_data['email']
                user.save()
                messages.success(request, 'Your profile updated successfully', 'success')
                return redirect('profile', request.user.id)
        else:
            form = EditProfileForm(instance=user.profile, initial={'email':user.email})
        return render(request, 'accounts/edit_profile.html', {'form':form})
    else:
        return redirect('profile', request.user.id)

@login_required
def Follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following_user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=following_user)
        if relation.exists():
            return JsonResponse({'status':'exsist'})
        else:
            Relation(from_user=request.user, to_user=following_user).save()
            return JsonResponse({'status':'ok'})
@login_required
def Unfollow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        unfollowing_user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=unfollowing_user)
        if relation.exists():
            relation.delete()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'notexists'})


def PhoneLogin(request):
    if request.method == "POST":
        form = GetPhoneNumberForm(request.POST)
        if form.is_valid():
            global phone, token
            phone = f"0{form.cleaned_data['phone']}"
            profile = get_object_or_404(Profile, mobile=phone)
            user = User.objects.filter(profile__id=profile.id)
            token = randint(1000,9999)
            api = KavenegarAPI('55334B346B7049394D4C4B742F4348616733656D5165645A6669747A344B734478707257694977326763493D')
            params = { 'sender' : '1000596446', 'receptor': phone, 'message': token }
            api.sms_send(params)
            return redirect('verify_phone')
    else:
        form = GetPhoneNumberForm()
    return render(request, 'accounts/phone_login.html', {'form':form})


def VerifyPhone(request):
    if request.method == 'POST':
        form = VerifyPhoneForm(request.POST)
        if form.is_valid():
            if token == form.cleaned_data['code']:
                profile = get_object_or_404(Profile, mobile=phone)
                user = get_object_or_404(User, profile__id=profile.id)
                login(request, user)
                messages.success(request, 'You loged in successfully', 'success')
                return redirect('index')
            else:
                messages.error(request, 'Your code is wrong!', 'Warning')
    else:
        form = VerifyPhoneForm()
    return render(request, 'accounts/verify_phone.html', {'form':form})


def ResetPassword(request):
    if request.method == "POST":
        form = GetPhoneNumberForm(request.POST)
        if form.is_valid():
            global phone, token
            phone = f"0{form.cleaned_data['phone']}"
            profile = get_object_or_404(Profile, mobile=phone)
            user = User.objects.filter(profile__id=profile.id)
            token = randint(1000,9999)
            api = KavenegarAPI('55334B346B7049394D4C4B742F4348616733656D5165645A6669747A344B734478707257694977326763493D')
            params = { 'sender' : '1000596446', 'receptor': phone, 'message': token }
            api.sms_send(params)
            return redirect('reset_password_confirm')
    else:
        form = GetPhoneNumberForm()
    return render(request, 'accounts/reset_password.html', {'form':form})


def ResetPasswordConfirm(request):
    if request.method == 'POST':
        form = VerifyPhoneForm(request.POST)
        if form.is_valid():
            if token == form.cleaned_data['code']:
                return redirect('reset_password_done')
            else:
                messages.error(request, 'Your code is wrong!', 'Warning')
    else:
        form = VerifyPhoneForm()
    return render(request, 'accounts/reset_password.html', {'form':form})


def ResetPasswordDone(request):
    if request.method == 'POST':
        form = ResetPasswordConfirmForm(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, mobile=phone)
            user = get_object_or_404(User, profile__id=profile.id)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('reset_password_complete')
    else:
        form = ResetPasswordConfirmForm()
    return render(request, 'accounts/reset_password_confirm.html', {'form':form})


def ResetPasswordComplete(request):
    return render(request, 'accounts/reset_password_complete.html')
