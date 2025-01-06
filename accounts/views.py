from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserChangeForm

# User Registration View
def register(request):
    """
    Handles user registration.
    - Displays a registration form.
    - Saves the user data upon successful form submission.
    - Redirects to login page with a success message.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# User Profile View
@login_required
def user_profile(request):
    """
    Displays the user profile.
    - Requires the user to be logged in.
    - Renders the `user_profile.html` template.
    """
    return render(request, 'accounts/user_profile.html')


# Edit Profile View
@login_required
def edit_profile(request):
    """
    Handles editing of user profile and password.
    - Displays forms for profile and password updates.
    - Processes and validates submitted forms.
    - Provides success messages upon successful updates.
    - Redirects to the user profile page after updates.
    """
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
            update_session_auth_hash(request, password_form.user)  # Prevents logout after password change
            messages.success(request, 'Your password has been successfully updated!')

        if profile_updated or password_updated:
            return redirect('user_profile')

    return render(
        request,
        'accounts/edit_profile.html',
        {'form': profile_form, 'password_form': password_form}
    )
