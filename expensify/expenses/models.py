from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):

    CATEGORY_CHOICES = (
        ('Travel', 'travel'),
        ('Electricity', 'electricity'),
        ('Hotels booking', 'hotel booking'),
        ('Airtime & Data', 'airtime & data')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.user.username


class Budget(models.Model):
    CATEGORY_CHOICES = (
        ('Travel', 'travel'),
        ('Electricity', 'electricity'),
        ('Hotels booking', 'hotel booking'),
        ('Airtime & Data', 'airtime & data')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username
    