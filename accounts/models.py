from django.db import models 
from django.contrib.auth.models import User 

class HotelUser(User): 
    profile_picture=models.ImageField(upload_to='profile') 
    phn_no=models.CharField(max_length=10,unique=True) 
    email_token = models.CharField(max_length=100, unique=True, null=True, blank=True) 
    otp=models.IntegerField(null=True,blank=True) 
    is_verified=models.BooleanField(default=False) 

    class Meta: 
        db_table = 'hotel_user' 

class HotelVendor(User): 
    profile_picture=models.ImageField(upload_to='profile') 
    business_name=models.CharField(max_length=191,default="None",null=True,blank=True) 
    phn_no=models.CharField(max_length=10,unique=True)
    email_token=models.CharField(max_length=191,unique=True,null=True,blank=True) 
    otp=models.IntegerField(unique=True,null=True,blank=True) 
    is_verified=models.BooleanField(default=False) 

    class Meta: 
        db_table = 'hotel_vendor' 
    def __str__(self): 
        return self.username
    
class Ameneties(models.Model): 
    amenite_name=models.CharField(max_length=191) 
    icon=models.ImageField(upload_to='hotels') 
    
    def __str__(self): 
        return self.amenite_name 

class Hotel(models.Model): 
    hotel_name=models.CharField(max_length=191) 
    hotel_description=models.TextField() 
    hotel_owner=models.ForeignKey(HotelVendor,on_delete=models.CASCADE) 
    hotel_price=models.FloatField() 
    hotel_offer_price=models.FloatField() 
    hotel_location=models.TextField() 
    amenities=models.ManyToManyField(Ameneties) 
    hotel_slug=models.SlugField(max_length=191,unique=True) 
    is_active=models.BooleanField(default=True) 
    business_name=models.CharField(max_length=191,default="None",null=True,blank=True) 

    def __str__(self):
        return self.hotel_name

class HotelImages(models.Model): 
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE , related_name = "hotel_images") 
    image = models.ImageField(upload_to="hotels") 

    def __str__(self):
        return f"Image for {self.hotel.hotel_name}-{self.id}"
    
class HotelManager(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE , related_name = "hotel_managers") 
    manager_name = models.CharField(max_length = 100) 
    manager_contact = models.CharField(max_length = 100)

class HotelBooking(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    user=models.ForeignKey(HotelUser,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    total_price=models.FloatField()
    checked_in=models.BooleanField(default=False)
    checked_out=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hotel.hotel_name} is booked"