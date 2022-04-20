from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import MyUserCreationForm


def register_page(request):

    if request.user.is_authenticated:
        return redirect('/')

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
    
    if request.user.is_authenticated:
        return redirect('/')

    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password =  request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")

        else:
            return redirect("authentication:login-view")
            
    context = {'form':form} 
    return render(request, "authentication/login.html", context)

def logout_page(request):
    logout(request)
    return redirect('authentication:login-view')
