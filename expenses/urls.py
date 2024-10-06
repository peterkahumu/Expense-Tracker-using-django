from django.urls import path
from . import views
from .views import SearchExpense, ExpenseSummary
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name = 'expenses'),
    path('add_expense', views.addExpense, name = 'add-expense'),
    path('edit-expense/<int:id>', views.editExpense, name = 'edit-expense'),
    path('delete-expense/<int:id>', views.deleteExpense, name = 'delete-expense'),
    path('search', csrf_exempt(SearchExpense.as_view()), name = 'search' ),
    path('expense-summary', ExpenseSummary.as_view(), name = 'expense-summary'),
    path('expenses_stats', views.stats_view, name = 'expenses-stats'),
    path('export-csv', views.export_csv, name = 'export-csv'),
    path('export-excel', views.export_excel, name='export-excel'),
    path('export-pdf', views.export_pdf, name='export-pdf')
]