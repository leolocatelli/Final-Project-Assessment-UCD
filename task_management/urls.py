
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from . import views  
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

def home_view(request):
    return HttpResponse("<h1>Bem-vindo à Task Management App</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home_view, name='home'),
    path('tasks/', include('tasks.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)