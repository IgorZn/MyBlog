from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    # Обработчики действий со статьями.
    path('login/', UserLogin.as_view(), name='login'),
]