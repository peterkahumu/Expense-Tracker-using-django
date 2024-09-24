from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url = '/authentication/login')
def index(request):
    sources = SourceModel.objects.all()
    income = UserIncome.objects.filter(owner = request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except UserPreferences.DoesNotExist:
        currency = 'Not set'
    
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    
    return render(request, 'income/index.html', context=context)

def add_income(request):
    return render(request, 'income/add_income.html')