from django.contrib import admin
from .models import *

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'description', 'date', 'category', 'owner'] # fields to display in the admin page.
    
    search_fields = ['amount', 'description', 'date', 'category']    # field to refer to during the search
    list_per_page = 5 # paginantion
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
