import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .forms import UploadFileForm
from .forms import ExpenseForm
from .models import Expense


def index(request):
    return HttpResponse("Welcome to the Expense Tracker App!")


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Expense added successfully!")
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})


def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            excel_file = request.FILES['file']
            
            if not excel_file:
                messages.error(request, "No file was uploaded.")
                return render(request, 'upload_file.html', {'form': form})
            
            try:
                # Reads the Excel file
                data = pd.read_excel(excel_file)

                required_columns = {'Name', 'Amount', 'Date'}
                if not required_columns.issubset(data.columns):
                    messages.error(request, "Invalid file format. Required columns: Name, Amount, Date.")
                    return render(request, 'upload_file.html', {'form': form})
                
                # Save rows from file into the database
                for _, row in data.iterrows():
                    if pd.isna(row['Name']) or pd.isna(row['Amount']) or pd.isna(row['Date']):
                        messages.warning(request, f"Skipping row with missing values: {row.to_dict()}")
                        continue  # Skips rows with missing values                 
                    
                    
                    Expense.objects.create(
                        name=row['Name'],
                        amount=row['Amount'],
                        date=row['Date']                    
                    )
                    
                messages.success(request, "File uploaded successfully! Expenses added.")
                return render(request, 'upload_success.html')
            
            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
                return render(request, 'upload_file.html', {'form': form})

    else:
        form = UploadFileForm()
        
    return render(request, 'upload_file.html', {'form': form})