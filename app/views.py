
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Home Page
def home(request):
    return render(request, 'app/home.html')


# Register Page
def register(request):

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'app/register.html',
                          {'error': 'Passwords do not match!'})

        if User.objects.filter(username=username).exists():
            return render(request, 'app/register.html',
                          {'error': 'Username already exists!'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        login(request, user)

        return redirect('home')

    return render(request, 'app/register.html')


# Login Page
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:
            return render(request, 'app/login.html',
                          {'error': 'Invalid username or password!'})

    return render(request, 'app/login.html')


# Logout
def logout_view(request):

    logout(request)

    return redirect('login')
