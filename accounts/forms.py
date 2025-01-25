from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# Custom form for user registration
class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user account, including fields for username,
    email, first name, last name, and an optional profile picture.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')  #  'profile_picture'


# Custom form for updating user information
class CustomUserChangeForm(UserChangeForm):
    """
    Form for editing existing user account details. This includes the ability
    to update the username, email, first name, last name, and profile picture.
    A password field is included for optional password updates.
    """
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password (optional)'}),
        label="Password"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')  # 'profile_picture'

    def save(self, commit=True):
        """
        Save method override to handle password updates.
        - If a password is provided, it updates the user's password.
        - If no password is provided, only other fields are updated.
        """
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')  # Retrieve the entered password
        if password:  # If password field is not empty
            user.set_password(password)  # Set the new password
        if commit:  # Save the user instance to the database
            user.save()
        return user
