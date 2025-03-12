from django.db import models

<<<<<<< HEAD
class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    
    def __str__(self):
        return self.name
=======

class Expense(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255)
    distribution_expense = models.FloatField()
    published_date = models.DateField()
    
    
    def __str__(self):
        return self.title
>>>>>>> d3d3efd (Fixed embedded repo issue and removed unnecessary Git tracking)
