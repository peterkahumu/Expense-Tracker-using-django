from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.
class UsernameValidation(View):
    def post(self, request):
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            username = data['username']
            
            # Check if username contains only alphanumeric characters
            if not str(username).isalnum():
                return JsonResponse(
                    {'username_error': 'Username should only contain alphanumeric characters'},
                    status=400
                )
            
            # Check if username already exists
            # if User.objects.filter(username = username).exists():
            #     return JsonResponse({"username_error": "Sorry, this username is already taken."}, status = 409)
            
            
            return JsonResponse({'username_valid': True})

        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON format'},
                status=400
            )


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')