from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json


# Create your views here.
@login_required(login_url = '/authentication/login')
def index(request):
    sources = Source.objects.all()
    user = request.user
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

@login_required(login_url='/authentication/login')
def add_income(request):
    user = request.user
    sources = Source.objects.all()
    values = request.POST
    context = {
        'sources': sources,
        'values': values,   
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        
        # validation.
        if not amount:
            messages.error(request, 'Amount required.')
            return render(request, 'income/add_income.html', context)
        
        if not description:
            messages.error(request, 'Description required.')
            return render(request, 'income/add_income.html', context)
        
        if not source:
            messages.error(request, 'Source required.')
            return render(request, 'income/add_income.html', context)
        
        if not date:
            messages.error(request, 'Date required.')
            return render(request, 'income/add_income.html', context)
        
        if UserIncome.objects.create(amount=amount, description=description, source=source, date=date, owner=user):
            messages.success(request, 'Income created successfully.')
            return redirect('income')
        else:
            messages.error(request, "Error creating the expense. If the error persists, please try again later.", context)
            return render(request, 'income/add_income.html', context)
    return render(request, 'income/add_income.html', context = context)

@login_required(login_url='/authentication/login')
def edit_income(request, id):
    user = request.user
    income = get_object_or_404(UserIncome, pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'sources': sources,
    }
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        
        # validation.
        if not amount:
            messages.error(request, 'Amount required.')
            return render(request, 'income/edit_income.html', context)
        
        if not description:
            messages.error(request, 'Description required.')
            return render(request, 'income/edit_income.html', context)
        
        if not source:
            messages.error(request, 'Source required.')
            return render(request, 'income/edit_income.html', context)
        
        if not date:
            messages.error(request, 'Date required.')
            return render(request, 'income/edit_income.html', context)
        
        
        income.amount = amount
        income.description = description
        income.source = source
        income.date = date
        
        try:
            income.save()
            messages.success(request, 'income updated successfully')
            return redirect('income')
        except Exception as e:
            messages.error(request, "An error occured while updating the expense. Please try again. If the error persists, please try again later. ", e)
            return render(request, 'income/edit_income.html', context)
    return render(request, 'income/edit_income.html', context)

@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = get_object_or_404(UserIncome, pk=id)
    
    try:
        income.delete()
        messages.success(request, 'Income has been deleted successfully.')
        return redirect('income')
    except Exception as e:
        messages.error(request, f"There was an error deleting the expense. {e}")
        return render(request, 'income/index.html')
    
@login_required(login_url='/authentication/login')
def searchIncome(request):
    import logging
    logger = logging.getLogger(__name__)
    
    user = request.user
    searchString = json.loads(request.body).get('searchValue').strip()  # Ensure no extra spaces

    logger.debug(f'Searching for: {searchString}')
    # If search string is empty, return all results or handle appropriately
   
    # Perform search based on different fields
    income = UserIncome.objects.filter(
        amount__istartswith=searchString, owner=user
    ) | UserIncome.objects.filter(description__icontains=searchString, owner=user) | UserIncome.objects.filter(source__icontains=searchString, owner=user) | UserIncome.objects.filter(date__icontains=searchString, owner=user)
        
    logger.debug(f"Results: {list(income.values())}")

    # Prepare data for the response
    data = income.values()

    return JsonResponse(list(data), safe=False)