from django.db import models
from django.contrib.auth.models import User

class Information(models.Model):
    PERIOD_CHOICES = [
        ('month', 'Month'),
        ('year', 'Year'),
    ]
    
    CARD_CHOICES = [
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('diamond', 'Diamond'),
    ]

    number_of_cctvs = models.IntegerField(default=1)
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_hours = models.IntegerField(editable=False, blank=True, null=True)
    period = models.CharField(max_length=5, choices=PERIOD_CHOICES, default='month')
    card_choice = models.CharField(max_length=7, choices=CARD_CHOICES)
    final_price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=200,blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='pending') 
    info =models.ForeignKey(Information, on_delete=models.CASCADE, default=None)
