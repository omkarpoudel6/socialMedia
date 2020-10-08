
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib.auth.models import User

from .forms import UserLoginForm,UserRegisterForm

# Create your views here.

def login_view(request):
    next=request.GET.get('next')
    # form=UserLoginForm(request.POST or None)
    if request.method=="POST":
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            login(request,user)
            if next:
                return redirect(next)
            else:
                return redirect('/')
    else:
        return redirect("/")
    # context={
    #     'form':form
    # }
    # return render(request,'login.html',context)

def register_view(request):
    next=request.GET.get('next')
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        # username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        # user=authenticate(username=username,password=password)
        user.set_password(password)
        user.save()
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


def Home(request):
    # user=request.user
    # print(user)
    # if user.is_authenticated():
    #     return render(request,'home.html')
    # else:
    #     return render(request,'login.html')
    user=request.user
    user_obj=User.objects.filter(username=user)
    if user_obj:
        return render(request, 'home.html')
    else:
        form=UserLoginForm
        context={
            'form':form
        }
        return render(request, 'login.html',context)


def Logout(request):
    logout(request)
    return redirect('/login')

def Profile(request):
    return render(request,'profile/userprofile.html')

