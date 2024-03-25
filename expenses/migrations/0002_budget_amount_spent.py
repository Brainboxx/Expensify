# Generated by Django 5.0.1 on 2024-03-18 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='amount_spent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]