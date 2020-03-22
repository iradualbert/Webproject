import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Notification

def register(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home_page')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def account(request):
    if request.method == 'GET':
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    elif request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account information has been saved!')
            return redirect('account')
        else:
            messages.debug(request, f'Sorry, There was an error!')

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/account.html', context)


@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def notification(request):
    notifications = Notification.objects.filter(to=request.user)
    return render(request, 'users/notifications.html', {"notifications": notifications})
