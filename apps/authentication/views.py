from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'authentication/home.html')

@login_required
def userPage(request):
    return render(request, 'authentication/userpage.html')

def signUpUser(request):
    if request.method == "POST":
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                user = User.objects.create_user(username=request.POST.get('username'),
                                                password=request.POST.get('password1'),
                                                first_name=request.POST.get('first_name'),
                                                last_name=request.POST.get('last_name'))
                user.save()
                login(request, user)
                return redirect('userPage')
            except IntegrityError:
                return render(request, 'authentication/signup.html', {'error':'That username has been already taken'})
        else:
            return render(request, 'authentication/signup.html', {'error':'Passwords do not match'})
    else:
        return render(request, 'authentication/signup.html')

@login_required
def logOutUser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

def logInUser(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get('username'),
                                     password=request.POST.get('password'))
        if user is None:
            return render(request, 'authentication/login.html', {'error':'Username and password do not match'})
        else:
            login(request, user)
            return redirect('userPage')
    else:
        return render(request, 'authentication/login.html')
