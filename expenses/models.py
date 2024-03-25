from django.db import models
from django.contrib.auth.models import User


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username
    

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Budget, related_name='expenses', on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.user.username


