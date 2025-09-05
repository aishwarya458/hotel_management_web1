from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('<slug:slug>/hotel-details/', views.hotel_details, name='hotel_details'),
   
]

