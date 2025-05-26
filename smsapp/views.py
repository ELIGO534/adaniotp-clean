from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from twilio.rest import Client

import random
import json

@csrf_exempt
def send_otp(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        phone = data.get("phone")
        if not phone:
            return JsonResponse({"error": "Phone number is required"}, status=400)

        otp = str(random.randint(10000, 99999))
        # Store OTP in cache for 5 minutes
        cache.set(f"otp_{phone}", otp, timeout=300)

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone,
            body=f"Your OTP is {otp}"
        )
        return JsonResponse({"status": "success", "message_sid": message.sid})
    except Exception as e:
        logger.error(f"Error in send_otp: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def verify_otp(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        phone = data.get("phone")
        otp = data.get("otp")
        if not phone or not otp:
            return JsonResponse({"error": "Phone and OTP are required"}, status=400)

        cached_otp = cache.get(f"otp_{phone}")
        if cached_otp is None:
            return JsonResponse({"status": "fail", "message": "OTP expired or not found"}, status=400)

        if otp == cached_otp:
            # Optionally delete OTP from cache after successful verification
            cache.delete(f"otp_{phone}")
            return JsonResponse({"status": "success", "message": "OTP verified"})
        else:
            return JsonResponse({"status": "fail", "message": "Invalid OTP"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
