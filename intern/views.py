from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        print(uname)
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        new_user = User.objects.create_user(
            username=uname, first_name=fname, last_name=lname, email=email, password=password)
        new_user.save()
        return redirect('home')

    else:
        return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.INFO, "Login Successfull")
            return render(request, 'home.html', {'username': username})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def contact(request):
    return render(request, 'contact.html')
