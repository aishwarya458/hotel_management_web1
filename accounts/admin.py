from django.contrib import admin

from .models import *

admin.site.register(Hotel)

admin.site.register(HotelImages)

admin.site.register(HotelManager)

admin.site.register(HotelUser)

admin.site.register(HotelVendor)
admin.site.register(Ameneties)
admin.site.register(HotelBooking)