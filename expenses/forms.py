from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['id', 'title', 'distribution_expense', 'published_date', 'notes']

        

class UploadFileForm(forms.Form):
    file = forms.FileField()
    

class UploadFileForm(forms.Form):
    file = forms.FileField()
    
    