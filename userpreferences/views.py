from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
import json
from django.conf import settings
from .models import UserPreferences
import pdb
from django.contrib import messages
from django.conf import settings
# Create your views here.

@login_required(login_url='login')
def index(request):
    # get or create the user preferences of the currently loggged in user.
    user_preferences, created = UserPreferences.objects.get_or_create(user = request.user)
    
    # check if the method is GET (when the page is loaded.)
    if request.method == 'GET':
        currency_data = []
        
        # file path to get the lists of different currencies.
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        
        # open the file and read the data.
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            
            for key, value in data.items():
                currency_data.append({'name': key, 'value': value})
            
            context = {
                'currencies': currency_data,
                'user_preferences': user_preferences
            }
            
        return render(request, 'preferences/index.html', context)
    else: # method is POST
        currency = request.POST['currency']
        
        if currency:
            user_preferences.currency = currency
            user_preferences.save() # save the changes to the database.
            
            # shoe a success message. 
            messages.success(request, 'Currency updated successfully.')
        else:
            messages.error(request, 'Please select a currency.')        

        return redirect('preferences')