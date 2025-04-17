from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('upload/', views.upload_file, name='upload_file'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('update-note/', views.update_note, name='update_note'),
]