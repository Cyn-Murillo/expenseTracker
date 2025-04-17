import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm
from .forms import ExpenseForm
from .models import Expense


def index(request):
    return HttpResponse("Welcome to the Expense Tracker App!")


def dashboard(request):
    return render(request, 'dashboard.html')


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.uploaded_by = request.user
            expense.save()
            return HttpResponse("Expense added successfully!")
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})


def expense_list(request):
    if request.GET.get('clear_messages'):
        storage = messages.get_messages(request)
        list(storage)  # Force message storage to clear

    expenses = Expense.objects.all()
    preview_data = request.session.pop('expense_preview', None)

    return render(request, 'expense_list.html', {
        'expenses': expenses,
        'expense_preview': preview_data
    })

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            if not excel_file:
                messages.error(request, "No file was uploaded.")
                return render(request, 'upload_file.html', {'form': form})

            try:
                data = pd.read_excel(excel_file)

                required_columns = {'id', 'title', 'distribution_expense', 'published_date'}
                if not required_columns.issubset(data.columns):
                    messages.error(request, "Invalid file format. Required columns: id, title, distribution_expense, published_date")
                    return render(request, 'upload_file.html', {'form': form})

                # Track seen IDs and skipped entries
                seen_ids = set()
                rows_added = 0
                skipped_duplicates = []
                skipped_formatting = []

                for _, row in data.iterrows():
                    try:
                        if pd.isna(row['id']) or pd.isna(row['title']) or pd.isna(row['distribution_expense']) or pd.isna(row['published_date']):
                            raise ValueError("Missing required fields.")

                        original_id = str(row['id'])
                        new_id = original_id
                        suffix = 1

                        # Ensure unique ID by checking both in-file and database
                        while new_id in seen_ids or Expense.objects.filter(id=new_id).exists():
                            new_id = f"{original_id}-{suffix}"
                            suffix += 1

                        seen_ids.add(new_id)

                        # Attempt to clean the date
                        row['published_date'] = pd.to_datetime(row['published_date'], errors='coerce').date()
                        if pd.isna(row['published_date']):
                            raise ValueError("Invalid date format.")

                        Expense.objects.create(
                            id=new_id,
                            title=row['title'],
                            distribution_expense=row['distribution_expense'],
                            published_date=row['published_date'],
                            notes=row.get('notes', ''),
                            uploaded_by=request.user if request.user.is_authenticated else None
                        )
                        rows_added += 1

                    except ValueError as ve:
                        skipped_formatting.append(f"{row['id']} - {ve}")
                    except Exception as e:
                        skipped_formatting.append(f"{row.get('id', 'Unknown')} - Unexpected error: {e}")

                # Success message
                message = f"File uploaded! {rows_added} new expense(s) added."

                if skipped_duplicates:
                    message += (
                        "\nSome rows were skipped (duplicates in file): " +
                        (", ".join(skipped_duplicates[:5]) + "..." if len(skipped_duplicates) > 5 else ", ".join(skipped_duplicates))
                    )

                if skipped_formatting:
                    message += (
                        "\nSome rows were skipped due to formatting issues: " +
                        (", ".join(skipped_formatting[:5]) + "..." if len(skipped_formatting) > 5 else ", ".join(skipped_formatting))
                    )

                preview_data = Expense.objects.order_by('-published_date')[:5]
                request.session['expense_preview'] = [
                {'title': e.title, 'amount': float(e.distribution_expense), 'date': str(e.published_date)}
                for e in preview_data
                ]
                messages.success(request, message)
                response = redirect('expense_list')
                response['Location'] += '?clear_messages=true'
                return response

            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
                return render(request, 'upload_file.html', {'form': form})

    else:
        form = UploadFileForm()

    return render(request, 'upload_file.html', {'form': form})

@csrf_exempt
def update_note(request):
    if request.method == "POST":
        expense_id = request.POST.get("id")
        new_note = request.POST.get("note")
        try:
            expense = Expense.objects.get(id=expense_id)
            expense.notes = new_note
            expense.save()
            return JsonResponse({"success": True})
        except Expense.DoesNotExist:
            return JsonResponse({"success": False, "error": "Expense not found"})
    return JsonResponse({"success": False, "error": "Invalid request method"})