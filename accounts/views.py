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
            return redirect('login')  # Redireciona para a página de login
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_profile(request):
    return render(request, 'accounts/user_profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('user_profile')

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Evita logout
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('user_profile')
    else:
        profile_form = CustomUserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(
        request, 
        'accounts/edit_profile.html', 
        {'form': profile_form, 'password_form': password_form}
    )
