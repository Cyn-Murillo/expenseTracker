from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'distribution_expense', 'published_date', 'uploaded_by')
    search_fields = ('title', 'notes')
    list_filter = ('published_date', 'uploaded_by')
