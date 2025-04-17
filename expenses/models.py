from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=255)
    distribution_expense = models.DecimalField(max_digits=10, decimal_places=2)
    published_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} ({self.published_date})"
