from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
# Create your views here.
@login_required(login_url='login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    
    context = {
        'categories': categories,
        'expenses': expenses,
    }
    return render(request, 'expenses/index.html', context)

def addExpense(request):
    categories = Category.objects.all()
    owner = request.user
    context = {
        'categories': categories,
        'values': request.POST,
    }
    
    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['date']
        description = request.POST['description']
        
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/add_expenses.html', context)
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/add_expenses.html', context)
        
        if not category:
            messages.error(request, "Category is required")
            return render(request, 'expenses/add_expenses.html', context)
        
        if not date:
            messages.error(request, "Date is required")
            return render(request, 'expenses/add_expenses.html', context)
        
        
        if Expense.objects.create(amount=amount, category=category, date=date, description=description, owner=owner):
            messages.success(request, "Expense added successfully")
            return redirect('expenses')
        else:
            messages.error(request, "An error occurred while adding the expense")
            return render(request, 'expenses/add_expenses.html', context)
        
    return render(request, 'expenses/add_expenses.html', context)

def editExpense(request):
    pass

def deleteExpense(request):
    pass

