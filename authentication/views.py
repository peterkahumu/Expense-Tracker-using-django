from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str,   DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading

# Create your views here.

class EmailThread(threading.Thread):
    # speed up the sending of the email and response back to the user.
    
    def __init__(self, email):
       self.email = email
       threading.Thread.__init__(self)
       
    def run(self):
        self.email.send(fail_silently = False)
        
class UsernameValidation(View):
   def post(self, request):
       data = json.loads(request.body)
       username = data['username']
       
       if not str(username).isalnum():
           return JsonResponse({'username_error': 'Invalid username. Use alphanumeric characters only.'}, status = 409)
       if User.objects.filter(username=username).exists():
           return JsonResponse({'username_error': 'Username already exists. Please choose another one.'}, status = 409)
       return JsonResponse({'username_valid': True})

class emailValidation(View):
    def post(self, request):
       data = json.loads(request.body)
       email = data['email']
       
       if not validate_email(email):
           return JsonResponse({'email_error': 'Invalid Email Address'}, status =  400)
       if User.objects.filter(email=email).exists():
           return JsonResponse({'email_error': 'Email is already taken. Please try another email of login instead'}, status = 409)
       return JsonResponse({'email_valid': True})
            
    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
       # get the user data.
       # validate the data.
       # create the user account.
       
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       
       context = {
           'fieldValues': request.POST
       }
       
       if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short. Please use 8 characters or more.")
                    return render(request, 'authentication/register.html', context)
                 
                user = User.objects.create_user(username = username, email = email)
                user.set_password(password)
                user.is_active = False # will not be able to login until the email is verified.
                user.save()
                
                # - path to the view.
                # - get the domain we the user is on.
                # - relative url verification.
                # - encode the uid.
                # - get the token the user can use to verify
                # - ensure the token can only be used once.
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs = {
                    'uidb64': uidb64,
                    'token': token
                })
                activate_url = f'http://{domain}{link}'
                email_subject = 'Activate your account'
                email_body  = f'Hi {user.username}! Please use this link to activate your account\n{activate_url}' 
                email = EmailMessage(
                    email_subject,
                    email_body, 
                    "noreply@semycolon.com",
                    [email],
               )
                
                EmailThread(email).start() # send the email using threading capabilities.
                
                messages.success(request, "Congratulations ! Account created successfully. Please check your email to activate your account.")
                return render(request, 'authentication/register.html')

class Verification(View):
    def get(self, request, uidb64, token):
       try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user  = User.objects.get(pk=id)
            
            if not token_generator.check_token(user, token):
                messages.info(request, 'Account already activated')
                return redirect('login')
            
            if user.is_active:
                return redirect('login')
            user.is_active= True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')
       except Exception as e:
            messages.error(request, e)
            return redirect('register')

class Login(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        data = request.POST
        username = data['username']
        password = data['password']
        
        if username and password:
            
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome {user.username}.')
                    return redirect('expenses')

                messages.error(request, 'Account inactive. Please activate using the link sent to you email.')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'authentication/login.html')
        messages.error(request, "Please fill all the fields before trying to log in.")
        return render(request, 'authentication/login.html')
    
class Logout(View):
    def post(self, request):
        
        if request.user.is_authenticated:
            auth.logout(request)
            messages.success(request, 'You have been logged out.')
            return redirect('login')
        
        messages.error(request, "You are not logged in. Please login first.")
        return redirect('login')
    
class ResetPassword(View):
    def get(self, request):
        return render(request, 'authentication/reset_password.html')
    
    def post(self, request):
        email = request .POST['email']
        context= {
            "Values": request.POST
        }
        if not validate_email(email):
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'authentication/reset_password.html', context)
        
        user = User.objects.filter(email=email)
        if not user.exists():
            messages.error(request, 'The email does not exist. Please try creating a new account or check the email and try again.')
            return render(request, 'authentication/reset_password.html')
        
        uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
        token = PasswordResetTokenGenerator().make_token(user[0])
        domain = get_current_site(request).domain
        link = reverse('set-new-password', kwargs = {
            'uidb64': uidb64, 
            'token': token
        })
        reset_url = f'http://{domain}{link}'
        email_subject = 'Reset your password'
        email_body  = f'Hi {user[0].username}! Please use this link to reset the password to your account.\n{reset_url}' 
        email = EmailMessage(
            email_subject,
            email_body, 
            "noreply@semycolon.com",
            [email],
        )
        
        EmailThread(email).start()
        messages.success(request, "An email has been sent successfully. Please check your email.")
        return render(request, 'authentication/reset_password.html')
    
class SetNewPassword(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        return render(request, 'authentication/set_new_password.html', context)
    
    def post(self, request, uidb64, token):
        
        context = {
            'uidb64': uidb64,
            'token': token,
            'fieldValues': request.POST,
        }
        
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        
        if len(password) < 6:
            messages.error(request, 'The password is too short. Please use more than 6 characters.')
            return render(request, 'authentication/set_new_password.html', context)
        
        if password != confirmpassword:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'authentication/set_new_password.html', context)
        
        try:
            userId = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=userId)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully. Please login with the new password.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Something went wrong. Please try again later. {e}')
            return render(request, 'authentication/set_new_password.html', context)
        
