from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'expenses'),
    path('add_expense', views.addExpense, name = 'add-expense'),
    path('edit-expense/<id>', views.editExpense, name = 'edit-expense'),
    path('delete-expense/<id>', views.addExpense, name = 'delete-expense'),
]