from django.urls import path

from .views import *

app_name = 'authentication'

urlpatterns = [
    path('authentication/login/', login_page, name='login-view'),
    path('authentication/logout/', logout_page, name='logout-view'),
    path('authentication/register/', register_page, name='register-view'),
]
