
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib.auth.models import User
from .models import Profile,RelationShip
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
    user=request.user
    profile=Profile.objects.get(username_id=id)
    posts=Post.objects.filter(author=profile.username)
    logged_user_profile = Profile.objects.get(username=user)
    context={
        'profile':profile,
        'logged_user_profile':logged_user_profile,
        'posts':posts
    }
    return render(request,'profile/view_friends_profile.html',context)

def Friends(request):
    user=request.user
    context={}
    people_you_may_know=[]
    # getting all available user profile
    users=Profile.objects.exclude(username_id=user.id)

    #checking is relationship between profiles and user exists or not related to friend requests if relationship doesnot exists the the logged in user
    #can send friend request
    for u in users:
        if not (RelationShip.objects.filter(sender=user.id,receiver=u.username_id) or RelationShip.objects.filter(sender=u.username_id,receiver=user.id)) :
            people_you_may_know.append(u)
    context['people_you_may_know']=people_you_may_know

    #gettin logged in user profile
    logged_user_profile = Profile.objects.get(username=user)

    #getting friend request for logged in user
    if RelationShip.objects.filter(receiver=user.id):
        friend_request=RelationShip.objects.filter(receiver=user.id,status="send")
        context['friend_requests']=friend_request

    context['logged_user_profile']=logged_user_profile
    return render(request,'friends.html',context)

def AddFriend(request):
    user=request.user
    if request.method=='POST':
        receiver_id=request.POST.get('receiver_id')
        receiver=User.objects.get(id=receiver_id)
        relationship=RelationShip()
        relationship.sender=user
        relationship.receiver=receiver
        relationship.save()
    return redirect("/friends")

def AcceptFriendRequest(request):
    user=request.user
    if request.method=="POST":
        sender_id=request.POST.get('sender_id')
        relationship=RelationShip.objects.get(sender=sender_id,receiver=user.id)
        relationship.status="accepted"
        relationship.save()
    return redirect("/friends")





