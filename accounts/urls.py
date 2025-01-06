from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# URL patterns for the accounts app
urlpatterns = [
    # Login and Logout
    path(
        'login/', 
        auth_views.LoginView.as_view(template_name='registration/login.html', next_page='task_list'), 
        name='login'
    ),
    path(
        'logout/', 
        auth_views.LogoutView.as_view(next_page='home'), 
        name='logout'
    ),
    
    # User registration and profile management
    path('register/', views.register, name='register'),  # User registration
    path('profile/', views.user_profile, name='user_profile'),  # View user profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit user profile

    # Password change functionality
    path(
        'password_change/', 
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'
    ),
    path(
        'password_change_done/', 
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'
    ),
    
    # Password reset functionality
    path(
        'password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
        name='password_reset'
    ),
    path(
        'password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
]
