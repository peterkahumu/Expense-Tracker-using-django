from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url='login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    
    # Pagination
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')   
    # construct the page object.
    page_obj = paginator.get_page(page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
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

def editExpense(request, id):
    expense = get_object_or_404(Expense, pk=id)
    categories = Category.objects.all()
    context = {
        "expense":expense,
        'categories': categories,
    }
    
    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        date = request.POST['date']
        
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/edit_expense.html', context)
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/edit_expense.html', context)
        
        if not category:
            messages.error(request, "Category is required")
            return render(request, 'expenses/edit_expense.html', context)
        
        if not date:
            messages.error(request, "Date is required")
            return render(request, 'expenses/edit_expense.html', context)
        
        expense.amount = amount
        expense.category = category
        expense.description = description
        expense.date = date
        
        try:
            expense.save()
            messages.success(request, "Expense updated successfully")
            return redirect('expenses')
        except Exception as e:
            messages.error(request, f"An error occurred while updating the expense. {e}")
            return render(request, 'expenses/edit_expense.html', context)
        
    return render(request, 'expenses/edit_expense.html', context)
    
def deleteExpense(request, id):
    expense  = get_object_or_404(Expense, pk=id)
    
    try:
        expense.delete()
        messages.success(request, "Expense deleted successfully")
        return redirect('expenses')
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the expense. Please try again later. {e}")
        return redirect('expenses')
    

