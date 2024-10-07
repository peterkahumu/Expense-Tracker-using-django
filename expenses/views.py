from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse, FileResponse
from userpreferences.models import UserPreferences
import datetime
import csv
import xlwt
from django.conf import settings
import os

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, SimpleDocTemplate, Image, PageBreak
from reportlab.lib.units import inch

# Create your views here.
@login_required(login_url='login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    
    # Pagination
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')   
    # construct the page object.
    page_obj = paginator.get_page(page_number)
    
    try:
        currency = UserPreferences.objects.get(user=request.user)
        currency_value = currency.currency
    except UserPreferences.DoesNotExist:
        currency_value = "Not Set"
        
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency_value,
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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
 
@login_required(login_url='login')   
def deleteExpense(request, id):
    expense  = get_object_or_404(Expense, pk=id)
    
    try:
        expense.delete()
        messages.success(request, "Expense deleted successfully")
        return redirect('expenses')
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the expense. Please try again later. {e}")
        return redirect('expenses')


class SearchExpense(View):
    def post(self, request):
        search_str = json.loads(request.body).get('data')
        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(description__icontains = search_str, owner=request.user) | Expense.objects.filter(date__icontains = search_str, owner=request.user) | Expense.objects.filter(category__icontains = search_str, owner=request.user)
        
        data = expenses.values()
        
        return JsonResponse(list(data), safe = False)

class ExpenseSummary(View):
    def get(self, request):
        today = datetime.date.today()
        six_months_ago = today - datetime.timedelta(days =  30 * 6) # get the date of six months ago.
        expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte = today)
        
        final_data = {}
        
        def get_category(expense):
            return expense.category
        
        category_list = list(set(map(get_category, expenses))) # set function removes duplicate categories.
        
        def get_category_amount(category):
            amount = 0
            filtered_by_category = expenses.filter(category=category)
            
            for item in filtered_by_category:
                amount += item.amount
             
            return amount
            
        
        for expense in expenses:
            for category in category_list:
                final_data[category] = get_category_amount(category)
        
        return JsonResponse({'Expense_category': final_data}, safe=False)
   
@login_required(login_url='login') 
def stats_view(request):
    return render(request, 'expenses/stats.html')

@login_required(login_url='login')
def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expense' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow([f'EXPENSE DATA FOR {request.user.username}'])
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner = request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response

@login_required(login_url='login')
def export_excel(request):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(f"{request.user.username}'s Expenses")

    ws.write(0, 0, 'Amount')
    ws.write(0, 1, 'Description')
    ws.write(0, 2, 'Category')
    ws.write(0, 3, 'Date')

    expenses = Expense.objects.filter(owner=request.user)

    for row_number, expense in enumerate(expenses):
        ws.write(row_number + 1, 0, expense.amount)
        ws.write(row_number + 1, 1, expense.description)
        ws.write(row_number + 1, 2, expense.category)
        ws.write(row_number + 1, 3, expense.date)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Expenses'+str(datetime.datetime.now())+'.xls'
    wb.save(response)
    
    return response


@login_required(login_url='login')
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    expenses = Expense.objects.filter(owner=request.user)

    elements = []

    logo_path = os.path.join(settings.BASE_DIR, 'expensesWebsite', 'static', 'img', 'logo.jpg')
    heading_text = f"{request.user.username}'s Expenses from {expenses.order_by('date').first().date if expenses.exists() else 'N/A'} to {datetime.date.today()}"

    heading_logo_table = Table(
        [[Image(logo_path, width=1.5*inch, height=1*inch), Paragraph(heading_text, getSampleStyleSheet()['Heading1'])]],
        colWidths=[2 * inch, 4 * inch],
        hAlign='LEFT'
    )
    heading_logo_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('VALIGN', (1, 0), (1, 0), 'TOP')
    ]))

    elements.append(heading_logo_table)
    elements.append(Spacer(1, 0.5 * inch))

    col_widths = [1.5 * inch, 3.5 * inch, 1.5 * inch, 1.5 * inch]
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.blue),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('WORDWRAP', (1, 1), (1, -1), 'CJK')
    ])

    rows_per_page = 25
    expense_data = [['Amount', 'Description', 'Category', 'Date']]
    for expense in expenses:
        expense_data.append([expense.amount, Paragraph(expense.description, getSampleStyleSheet()['BodyText']), expense.category, expense.date])

    pages = [expense_data[i:i + rows_per_page] for i in range(0, len(expense_data), rows_per_page)]
    num_pages = len(pages)

    def footer(canvas, doc, page_num, num_pages):
        canvas.saveState()
        canvas.setFont('Helvetica', 10)
        footer_text = f"Page {page_num} of {num_pages}"
        width, height = A4
        canvas.drawRightString(width - 1 * inch, 0.75 * inch, footer_text)
        canvas.restoreState()

    for page_num, page_data in enumerate(pages, start=1):
        table = Table(page_data, colWidths=col_widths)
        table.setStyle(table_style)
        elements.append(table)

        if page_num < num_pages:
            elements.append(PageBreak())

    doc.build(elements, onFirstPage=lambda c, d: footer(c, d, 1, num_pages), onLaterPages=lambda c, d: footer(c, d, d.page, num_pages))
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
