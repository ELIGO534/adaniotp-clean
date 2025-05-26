from django.conf import settings
from django.http import JsonResponse
from twilio.rest import Client

def send_otp(request):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_PHONE_NUMBER
    client = Client(account_sid, auth_token)

    # Example phone number and OTP message
    to_number = '+917989709833'  # Replace or get from form/request
    otp = '54321'  # Generate dynamically in real cases
    message_body = f'Your OTP is {otp}'

    message = client.messages.create(
        from_=twilio_number,
        to=to_number,
        body=message_body
    )
    return JsonResponse({'status': 'success', 'sid': message.sid})

