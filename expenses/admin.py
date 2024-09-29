from django.contrib import admin
from .models import *

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'description', 'date', 'category', 'owner']
    search_fields = ['amount', 'description', 'date', 'category']
    
    list_per_page = 5
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
