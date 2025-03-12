import pandas as pd
<<<<<<< HEAD
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .forms import UploadFileForm
from .forms import ExpenseForm
from .models import Expense


def index(request):
    return HttpResponse("Welcome to the Expense Tracker App!")


def add_expense(request):
=======
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .forms import UploadFileForm, ExpenseForm
from .models import Expense



def index(request):
    """"Homepage view"""
    return render(request, 'index.html')


def add_expense(request):
    """"Form to add a single expense"""
>>>>>>> d3d3efd (Fixed embedded repo issue and removed unnecessary Git tracking)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            return HttpResponse("Expense added successfully!")
    else:
        form = ExpenseForm()
=======
            return redirect('expense_list')
    
    else:
        form = ExpenseForm()
        
        
>>>>>>> d3d3efd (Fixed embedded repo issue and removed unnecessary Git tracking)
    return render(request, 'add_expense.html', {'form': form})


def expense_list(request):
<<<<<<< HEAD
=======
    """"Displays a list of all the expenses"""
>>>>>>> d3d3efd (Fixed embedded repo issue and removed unnecessary Git tracking)
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})


<<<<<<< HEAD
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
        
=======

def upload_file(request):
    """File Upload, validates data, and adds expenses to the database"""
    
    # Ensure messages are cleared only at the start of a new request
    storage = get_messages(request)
    list(storage)  # Accessing storage ensures messages are cleared on reload
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Validate file type
            if not uploaded_file.name.endswith('.xlsx'):
                messages.error(request, "Invalid file format. Please upload an Excel file (.xlsx).")
                return redirect('upload_file')
            
            try:
                # Read the Excel file
                data = pd.read_excel(uploaded_file)

                required_columns = {'id', 'title', 'distribution_expense', 'published_date'}
                if not required_columns.issubset(data.columns):
                    messages.error(request, "Invalid file format. Required columns: id, title, distribution_expense, published_date.")
                    return render(request, 'upload_file.html', {'form': form})
                
                
                # Check if the database is empty
                is_db_empty = not Expense.objects.exists()
                
                
                # Track skipped and added rows
                skipped_formatting = []
                skipped_duplicates = []
                rows_added = 0
                
                
                for _, row in data.iterrows():
                    try:
                        # Check for missing values
                        if pd.isna(row['id']) or pd.isna(row['title']) or pd.isna(row['distribution_expense']) or pd.isna(row['published_date']):
                            raise ValueError("Missing required fields.")            

                        # Validate date format
                        row['published_date'] = pd.to_datetime(row['published_date'], errors='coerce').date()
                        if pd.isna(row['published_date']):
                            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
                                                                    
                        if is_db_empty:
                            # If the database is empty, insert without checking for duplicates
                            Expense.objects.create(
                                id=row['id'],
                                title=row['title'],
                                distribution_expense=row['distribution_expense'],
                                published_date=row['published_date']
                            )
                            rows_added += 1
                        else:
                            # If the database has records, check for duplicates
                            obj, created = Expense.objects.update_or_create(
                                id=row['id'],
                                defaults={
                                    "title": row['title'],
                                    "distribution_expense": row['distribution_expense'],
                                    "published_date": row['published_date']
                                }
                            )
                            if not created:
                                skipped_duplicates.append(f"🟡 **{row['id']}** - '{row['title']}' already exists.")
                            else:
                                rows_added += 1

                    except ValueError as e:
                        skipped_formatting.append(f"⚠️ **{row['id']}** - Row skipped: {e}")

                # Display messages
                if rows_added > 0:
                    messages.success(request, "File uploaded successfully! Expenses added.")

                if skipped_formatting:
                    messages.warning(request, f"Some rows were skipped due to **formatting issues**:\n" + "\n".join(skipped_formatting))

                if skipped_duplicates:
                    messages.warning(request, f"Some rows were skipped because they were **already in the database**:\n" + "\n".join(skipped_duplicates))

                return redirect('expense_list')

            except Exception as e:
                messages.error(request, f"❌ Error processing file: {str(e)}")
                return redirect('upload_file')

    else:
        form = UploadFileForm()

>>>>>>> d3d3efd (Fixed embedded repo issue and removed unnecessary Git tracking)
    return render(request, 'upload_file.html', {'form': form})