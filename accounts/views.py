from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from .models import Hotel,HotelImages,HotelManager,HotelUser,HotelVendor,Ameneties
from .utils import generateRandomToken,sendEmailToken,sendOTPemail,generateSlug
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
import random
# Create your views here.

    

def login_view(request):
    email=""
    if request.method=="POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        
        if not email or not password:
            messages.warning(request,"Please fill all the fields.")
            return redirect('/accounts/login/')
        
        hotel_user=HotelUser.objects.filter(email=email).first()
        if not hotel_user: 
            messages.warning(request,"User does not exist.")
            return redirect('/accounts/login/')

        if  not hotel_user.is_verified:
            messages.warning(request,"Please verify your account first.")
            return redirect('/accounts/login/')
        
        hotel_user=authenticate(request,
            username=hotel_user.username,
            password=password
        )
        if hotel_user:
            login(request,hotel_user)
            messages.success(request,"You are logged in successfully.")
            return redirect('/')
        else:
            messages.warning(request,"Invalid credentials.")
            return redirect('/accounts/login/')
    return render(request,'login.html',{'email':email})

def register(request):
    if request.method == "POST":
        firstname=request.POST.get('first_name')
        lastname=request.POST.get('last_name')
        email=request.POST.get('email')
        phn_no=request.POST.get('phn_no')
        password=request.POST.get('password')

        hotel_user=HotelUser.objects.filter(
            Q(email=email) | Q(phn_no=phn_no)
        )

        if hotel_user.exists():
            messages.warning(request,"User Already Exists.")
            return redirect('/accounts/register/')

        hotel_user=HotelUser.objects.create(
            first_name=firstname,
            last_name=lastname,
            username=firstname+" "+lastname,
            email=email,
            phn_no=phn_no,
            email_token=generateRandomToken()[:191]

        )
        hotel_user.set_password(password)
        hotel_user.save()
      

        sendEmailToken(email,hotel_user.email_token,hotel_user.first_name,verify_url='verify-user-account')
        messages.success(request,"An email is sent to you please verify.")
        return redirect('/accounts/register/')

    return render(request,'register.html')


def verify_user_account(request,token):
    hotel_user=HotelUser.objects.filter(email_token=token).first()
    if hotel_user:
        hotel_user.is_verified=True
        hotel_user.save()
        messages.success(request,"Your account is verified successfully.")
        return redirect('/accounts/login/')
    else:
        messages.error(request,"Invalid token or account already verified.")

        return redirect('/accounts/register/')

def verify_vendor_account(request,token):
    hotel_user=HotelVendor.objects.filter(email_token=token).first()
    if hotel_user:
        hotel_user.is_verified=True
        hotel_user.save()
        messages.success(request,"Your account is verified successfully.")
        return redirect('/accounts/vendor-login/')
    else:
        messages.error(request,"Invalid token or account already verified.")

        return redirect('/accounts/vendor-register/')


def user_logout_view(request):
    logout(request)
    hotel_user = HotelUser.objects.filter(id=request.user.id).first()
    if hotel_user:
        hotel_user.otp = None   
        hotel_user.is_verified = False
        hotel_user.save()
    messages.success(request,"You are logged out successfully.")
    return redirect('/accounts/login/')


def vendor_logout_view(request):
    logout(request)
    hotel_user = HotelVendor.objects.filter(id=request.user.id).first()
    if hotel_user:
        hotel_user.otp = None   
        hotel_user.is_verified = False
        hotel_user.save()
    messages.success(request,"You are logged out successfully.")
    return redirect('/accounts/vendor-login/')

def sendOTP(request,email):
    hotel_user=HotelUser.objects.filter(email=email).first()
    if hotel_user:
        hotel_user.otp=random.randint(100000,999999)
        hotel_user.save()
        sendOTPemail(email,hotel_user.otp,hotel_user.first_name)
        messages.success(request,"An OTP is sent to your email.")
        return redirect('verify_otp',email=email)
    else:
        messages.warning(request,"User does not exist.")
        return redirect('/accounts/login/')

def verify_otp(request, email):     
    if request.method == "POST":
        otp = request.POST.get("otp", "").strip()
        hotel_user = HotelUser.objects.filter(email=email).first()
        if hotel_user and hotel_user.otp == int(otp):
            hotel_user.is_verified = True
            hotel_user.save()
            messages.success(request, "Your account is verified successfully with otp.")

            return redirect('/')
        else:
            messages.warning(request, "Invalid OTP.")
            return redirect('verify_otp', email=email)
    return render(request, 'verify_otp.html')

def vendor_login(request):
    email=""
    if request.method=="POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        
        if not email or not password:
            messages.warning(request,"Please fill all the fields.")
            return redirect('vendor_login')
        
        hotel_user=HotelVendor.objects.filter(email=email).first()
        if not hotel_user: 
            messages.warning(request,"User does not exist.")
            return redirect('vendor_login')

        if  not hotel_user.is_verified:
            messages.warning(request,"Please verify your account first.")
            return redirect('vendor_login')
        
        hotel_user=authenticate(request,
            username=hotel_user.username,
            password=password
        )
        if hotel_user:
            login(request,hotel_user)
            messages.success(request,"You are logged in successfully.")
            return redirect('vendor_dashboard'
                            )
        else:
            messages.warning(request,"Invalid credentials.")
            return redirect('vendor_login')
    return render(request,'vendor/vendor_login.html',{'email':email})

def vendor_register(request):
    if request.method == "POST":
        firstname=request.POST.get('first_name')
        lastname=request.POST.get('last_name')
        email=request.POST.get('email')
        phn_no=request.POST.get('phn_no')
        password=request.POST.get('password')
        business_name=request.POST.get('business_name')

        if HotelVendor.objects.filter(
            Q(email=email) | Q(phn_no=phn_no)
        ).exists():
            messages.warning(request,"User Already Exists.")
            return redirect('vendor_register')
        

        hotel_vendor_obj=HotelVendor.objects.create(
            first_name=firstname,
            last_name=lastname,
            username=email,
            email=email,
            phn_no=phn_no,
            business_name=business_name,
            email_token=generateRandomToken()

        )
        hotel_vendor_obj.set_password(password)
        hotel_vendor_obj.save()
      

        sendEmailToken(email,
                       hotel_vendor_obj.email_token,
                       hotel_vendor_obj.first_name,
                       verify_url='verify-vendor-account',)
        messages.success(request,"An email is sent to you please verify.")
        return redirect('vendor_register')

    return render(request,'vendor/vendor_register.html')



@login_required(login_url='/accounts/vendor-login/')

def vendor_dashboard(request):
    if not hasattr(request.user, 'hotelvendor'):
        messages.error(request, "You must be logged in as a vendor.")
        return redirect('vendor_login')
    
    hotel_vendor_obj = HotelVendor.objects.filter(id=request.user.id).first()
    hotel = Hotel.objects.filter(hotel_owner=hotel_vendor_obj)
    context={'hotels':hotel,'request':request}
    
    return render(request,'vendor/vendor_dashboard.html',context)


@login_required(login_url='/accounts/vendor-login/')
def add_hotel(request):
    
    if request.method=="POST":
    
        hotel_vendor_obj=HotelVendor.objects.filter(id=request.user.id).first()
        if not hotel_vendor_obj:
            messages.error(request, "You must be a vendor to add a hotel.")
            return redirect("add_hotel")
        
        hotel_name=request.POST.get('hotel_name')      
        hotel_description=request.POST.get('hotel_description') 
        hotel_amenities=request.POST.getlist('amenities[]') 
        hotel_price=request.POST.get('hotel_price') 
        hotel_offer_price=request.POST.get('hotel_offer_price') 
        hotel_location=request.POST.get('hotel_location') 
        hotel_slug=generateSlug(hotel_name) or "no-slug"
        if hotel_name=='' or hotel_description=='' or hotel_price=='' or hotel_offer_price=='' or hotel_location=='':
            messages.warning(request,"Please fill all the fields.")
            return redirect('add_hotel')
        if Hotel.objects.filter(hotel_name=hotel_name).first():
            messages.warning(request,"Hotel with this name already exists.")
            return redirect('add_hotel')
        
        hotel_obj=Hotel.objects.create(
            hotel_name=hotel_name,
            hotel_description=hotel_description,
            hotel_price=hotel_price,
            hotel_offer_price=hotel_offer_price,
            hotel_location=hotel_location,
            hotel_owner=hotel_vendor_obj,
            hotel_slug=hotel_slug
        )

        # print(hotel_name)
      
        hotel_obj.amenities.set(hotel_amenities)
        
        messages.success(request,"Hotel added successfully.")
        hotel_obj.save()
        return redirect('vendor_dashboard') 
    
    amenities=Ameneties.objects.all()


    return render(request,'vendor/add_hotel.html',context={'amenities':amenities})

def upload_images(request,slug):
    hotel_obj=Hotel.objects.filter(hotel_slug=slug).first()

    if request.method=="POST":
        image=request.FILES.get('image')
        if not image:
            messages.warning(request,"Please select an image to upload.")
            return redirect('upload_images', slug=slug)
        HotelImages.objects.create(
            hotel=hotel_obj,
            image=image
        )
        
        return HttpResponseRedirect(request.path_info)

    return render(request,'vendor/upload_images.html',context={'slug':slug,'images':hotel_obj.hotel_images.all()})


@login_required(login_url='/accounts/vendor-login/')
def delete_images(request,id):
    
    image_obj=HotelImages.objects.get(id=id)
    if not image_obj:
        messages.error(request,"Image does not exist.")
        return HttpResponseRedirect(request.path_info)
    image_obj.delete()
    image_obj.image.delete(save=False)
    messages.success(request,"Image deleted successfully")
    return redirect('upload_images', slug=image_obj.hotel.hotel_slug)
    
def edit_hotel(request,slug):

    hotel_obj=Hotel.objects.filter(hotel_slug=slug).first()
    if not hotel_obj:
        messages.error(request,"Hotel does not exist.")
        return redirect('vendor_dashboard')
    if request.method=='POST':
        hotel_name=request.POST.get('hotel_name')      
        hotel_description=request.POST.get('hotel_description') 
        hotel_amenities=request.POST.getlist('amenities[]') 
        hotel_price=request.POST.get('hotel_price') 
        hotel_offer_price=request.POST.get('hotel_offer_price') 
        hotel_location=request.POST.get('hotel_location')

        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description         
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.amenities.set(hotel_amenities)    
        hotel_obj.save()
        messages.success(request,"Hotel updated sucessfully.")
        return redirect('vendor_dashboard')
    amenities=Ameneties.objects.all()

    return render(request,'vendor/edit_hotel.html',context={'slug':slug,'amenities':amenities,'hotel':hotel_obj})

