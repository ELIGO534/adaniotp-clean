from django.conf import settings
from django.http import JsonResponse
from twilio.rest import Client
import logging

def send_otp(request):
    try:
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_number = settings.TWILIO_PHONE_NUMBER
        client = Client(account_sid, auth_token)

        to_number = '+917989709833'  # Replace or get from form/request
        otp = '54321'
        message_body = f'Your OTP is {otp}'

        message = client.messages.create(
            from_=twilio_number,
            to=to_number,
            body=message_body
        )
        return JsonResponse({'status': 'success', 'sid': message.sid})
    
    except Exception as e:
        logging.exception("Twilio SMS send failed")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
