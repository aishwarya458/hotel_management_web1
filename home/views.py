from django.shortcuts import render
from accounts .models import Hotel,HotelBooking,HotelUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime

def index(request):
    hotels=Hotel.objects.all()
    if request.GET.get('search',''):
        hotels=hotels.filter(hotel_name__icontains=request.GET.get('search'))
    if request.GET.get('sort_by'):
        sort_by=request.GET.get('sort_by')
        if sort_by=='sort_low':
            hotels=hotels.order_by('hotel_offer_price')
        elif sort_by=='sort_high':
            hotels=hotels.order_by('-hotel_offer_price')
    context={'hotels':hotels}
    return render(request, 'index.html', context=context)

@login_required(login_url='login')
def hotel_details(request,slug):
    hotel_obj=Hotel.objects.filter(hotel_slug=slug).first()
    if not hotel_obj:
        messages.warning(request,'Hotel not found',status=404)

    days_count=0
    if request.method=='POST':
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        if start_date=='' or end_date=='':
            messages.warning(request,'Please select the dates')
            return HttpResponseRedirect(request.path_info)
        start_date = datetime.strptime(start_date , '%Y-%m-%d')
        end_date = datetime.strptime(end_date , '%Y-%m-%d')
        
        days_count = (end_date - start_date).days
        if days_count <= 0:
            messages.warning(request,'Please select valid dates')
            return HttpResponseRedirect(request.path_info)
        HotelBooking.objects.create(
            hotel=hotel_obj,
            user=HotelUser.objects.get(id=request.user.id),
            start_date=start_date,
            end_date=end_date,
            total_price=hotel_obj.hotel_offer_price*days_count
        )
        messages.success(request,'Hotel booked successfully for '+str(days_count)+' days')
        return HttpResponseRedirect(request.path_info)
    context={'hotel':hotel_obj}
    return render(request,'hotel_details.html',context=context)