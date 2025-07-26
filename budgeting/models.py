from django.db import models
from django.contrib.auth.models import User

class WorkEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=7, decimal_places=2)

    @property
    def total_earnings(self):
        return self.hours_worked * self.hourly_rate

class BudgetAllocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField()

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=100, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount}"