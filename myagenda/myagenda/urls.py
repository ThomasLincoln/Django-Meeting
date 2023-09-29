from django.contrib import admin
from django.urls import path, include 
from django.views.generic.base import TemplateView
from accounts.views import dashboard

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),  
    path("dashboard/", dashboard, name='dashboard'),  
    path("dashboard/compromisso/", include('accounts.urls'))
]
