from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import json
from django.conf import settings
import pdb
# Create your views here.

@login_required(login_url='login')
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    # pdb.set_trace()
    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        
        for key, value in data.items():
            currency_data.append({
                'name': key,
                'value': value
            })  
        # pdb.set_trace()
        
    
    context = {'currencies': currency_data} 
    return render(request, 'preferences/index.html', context)