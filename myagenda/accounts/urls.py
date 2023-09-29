from django.urls import path

from .views import SignUpView, compromisso_detail, new, cancelar

app_name = 'compromisso'

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<int:pk>/", compromisso_detail, name='detail'),  
    path('new/', new, name='new'),
    path('compromisso/cancelar/<int:pk>/', cancelar, name='cancelar'),
    # path('compromisso/editar', editar , name='editar'),
]
