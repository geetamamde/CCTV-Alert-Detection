from django.shortcuts import render, redirect , HttpResponse
from .models import Information,Payment
from django.conf import settings
from django.http import JsonResponse
import stripe
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

stripe.api_key = settings.STRIPE_SECRET_KEY

def calculate_total_hours(start_time, end_time):
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))
    
    total_hours = end_hour - start_hour
    if end_minute > start_minute:
        total_hours += 1
    elif end_minute < start_minute:
        total_hours -= 1
    
    return total_hours




def take_info(request):
    if request.method == "GET":
     return render (request,"take_info.html",{})
    else:
        number_of_cctvs = request.POST['number_of_cctvs']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        period = request.POST['period']
        card_choice = request.POST['card_choice']

        total_hours = calculate_total_hours(start_time, end_time)
        
        if period == 'month':
            final_price = int(number_of_cctvs) * (total_hours * 10) * 30
        elif period == 'year':
            final_price = int(number_of_cctvs) * (total_hours * 10) * 300

        if card_choice == 'gold':
            final_price -= 50
        elif card_choice == 'diamond':
            final_price -= 100

        info = Information(
            number_of_cctvs=number_of_cctvs,
            start_time=start_time,
            end_time=end_time,
            total_hours=total_hours,
            period=period,
            final_price=final_price,
            card_choice=card_choice,
            user=request.user)
        info.save()

        return render(request,"show_info.html",{'info':info})


def create_checkout_session(request, id):
    try:
        info = Information.objects.get(id=id)
        amount = info.final_price * 100  

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Payment for {info.number_of_cctvs} CCTVs',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',

            success_url= 'http://127.0.0.1:8000/payment-successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url= 'http://127.0.0.1:8000/payment-cancelled',
            metadata={'info_id': str(info.id)},
        )
        
        return redirect(session.url, code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)})


def payment_successful(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponse("Session ID not provided", status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        info_id = session.metadata.get('info_id')  
        info = Information.objects.get(id=info_id)
        
      
        
        payment = Payment.objects.create(
            user=request.user,
            stripe_payment_id=session.payment_intent,
            info=info,
            payment_status='succeeded'  # Set the payment status as succeeded
        )
        payment.save()

        return HttpResponse("Payment successful")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=400)



def payment_cancelled(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponse("Session ID not provided", status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        info_id = session.metadata['info_id']  # Retrieve the info_id from the session metadata
        info = get_object_or_404(Information, id=info_id)
        
        payment, created = Payment.objects.get_or_create(
            stripe_payment_id=session.payment_intent,
            defaults={
                'user': request.user,
                'info': info,
                'payment_status': 'pending'  # Assuming 'pending' is a default status
            }
        )
        
        payment.payment_status = 'failed'
        payment.save()

        return HttpResponse("Payment failed and status updated")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=400)













































