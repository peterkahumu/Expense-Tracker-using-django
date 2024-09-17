from .views import *
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('validate-username', csrf_exempt(UsernameValidation.as_view()), name = 'validate-username'),
    path('validate-email', csrf_exempt(emailValidation.as_view()), name = 'validate_email'),
    path('activate/<uidb64>/<token>', Verification.as_view(), name = 'activate'),
]

