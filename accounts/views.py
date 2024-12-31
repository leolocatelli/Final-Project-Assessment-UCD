from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserChangeForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'accounts/user_profile.html')


@login_required
def edit_profile(request):
    profile_form = CustomUserChangeForm(
        request.POST or None, 
        request.FILES or None, 
        instance=request.user
    )
    password_form = PasswordChangeForm(request.user, request.POST or None)

    if request.method == 'POST':
        profile_updated = profile_form.is_valid()
        password_updated = password_form.is_valid()

        if profile_updated:
            profile_form.save()
            messages.success(request, 'Your profile has been successfully updated!')

        if password_updated:
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Your password has been successfully updated!')

        if profile_updated or password_updated:
            return redirect('user_profile')

    return render(
        request,
        'accounts/edit_profile.html',
        {'form': profile_form, 'password_form': password_form}
    )
