from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('add/', views.add_expense, name='add_expense'),
    path('list/', views.expense_list, name='expense_list'),
    path('upload/', views.upload_file, name='upload_file')
=======
    path('upload/', views.upload_file, name='upload_file'),
    path('list/', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense')
>>>>>>> d3d3efd (Fixed embedded repo issue and removed unnecessary Git tracking)
]