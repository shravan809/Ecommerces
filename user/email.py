from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User


def send_otp_via_email(email):
    try:
        subject = 'Your account verification mail'
        otp = random.randint(1000, 9999)
        message = f'Your OTP is {otp}'
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, [email], fail_silently=False)
        
        user_obj = User.objects.get(email=email)
        user_obj.otp = otp
        user_obj.save()
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        raise