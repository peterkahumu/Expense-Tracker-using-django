from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse

# Create your views here.
class usernameValidation(View):
    def post(self, request):
       data = json.loads(request.body)
       username = data['username']
       
       # check if username is valid
       if not str(username).isalnum():
           return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'})
       return JsonResponse ({'username_valid': True})
       

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')