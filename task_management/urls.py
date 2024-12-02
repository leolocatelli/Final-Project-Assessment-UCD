
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from . import views  
from django.contrib.auth.views import LogoutView

def home_view(request):
    return HttpResponse("<h1>Bem-vindo à Task Management App</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.hello_world, name='hello_world'),
    path('accounts/', include('accounts.urls')),  # Rota para a página inicial
    path('', home_view, name='home'),
    path('tasks/', include('tasks.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]

