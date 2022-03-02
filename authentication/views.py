from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MyUserCreationForm

def register_page(request):
    form = MyUserCreationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("/")

    return render(request, 'authentication/register.html', {'form':form})

def login_page(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password =  request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("authentication/login/")
    return render(request, "authentication/login.html", {'form':form})

def logout_page(request):
    logout(request)
    return redirect('/')