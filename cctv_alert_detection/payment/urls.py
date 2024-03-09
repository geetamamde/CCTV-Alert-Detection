from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.take_info),
    path('checkout-session/<str:id>/', views.create_checkout_session, name='checkout_session'), 
    path('payment-successful',views.payment_successful, name='payment_success'),
    path('payment-cancelled',views.payment_cancelled, name='payment_failure'), 

]