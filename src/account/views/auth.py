from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from account.models import User


@csrf_protect
@never_cache
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request,
                                 username=username,
                                 password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login success")
            return redirect("todo-home")

        messages.warning(request, "Invalid login")
        return redirect('login')

    form = AuthenticationForm(request=request)
    return render(request, "auth/login.html",
                  context={
                      request: request,
                      form: form
                  })


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        if User.objects.filter(email=username).exists():
            messages.warning(request, 'User already exists')
            return redirect('register')

        user = User.objects.create_user(
            email=username,
            password=password,
        )
        user.save()
        return redirect('login')

    return render(request, 'auth/register.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('login')
