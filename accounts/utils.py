import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import *

def generateRandomToken():
    return str(uuid.uuid4())

def sendEmailToken(email,token,first_name,verify_url):
    
  
    subject=f"Hi {first_name} ,Please verify your email address."
    message= f"""Hi Please verify you email account by clicking this link 
    http://127.0.0.1:8000/accounts/{verify_url}/{token}
    """
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)
    

def sendOTPemail(email, otp, first_name):
    subject = f"Hi {first_name}, Your OTP for login."
    message = f"Your OTP for login is {otp}. Please use this to complete your login."
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def generateSlug(hotel_name):
    if not hotel_name:
        return None
    slug = f"{slugify(hotel_name)}-" + str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug = slug).exists():
        return generateSlug(hotel_name)
    return slug
  