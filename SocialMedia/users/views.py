
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib.auth.models import User
from .models import Profile
from posts.models import Post

from .forms import UserLoginForm,UserRegisterForm,ProfileUpdateForm

# Create your views here.

def login_view(request):
    if request.method=="POST":
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            login(request,user)

            return redirect("/")
    else:
        return redirect("/")


def register_view(request):
    next=request.GET.get('next')
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        # profile=Profile.objects.create(username=user)
        # profile.save()
        new_user=authenticate(username=user.username,password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        else:
            return redirect('/')

    context={
        'form':form
    }
    return render(request,'register.html',context)


def Logout(request):
    logout(request)
    return redirect('/login')

def User_profile(request):
    user_name=request.user
    profile=Profile.objects.get(username=user_name)
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect("/profile")
    context={
        'form':form,
        'profile':profile
    }
    return render(request, 'profile/userprofile.html', context)

def view_friends_profile(request,id):
    profile=Profile.objects.get(id=id)
    posts=Post.objects.filter(author=id)
    print(posts)
    context={
        'profile':profile,
        'posts':posts
    }
    return render(request,'profile/view_friends_profile.html',context)




