from django.urls import path
from . import views
urlpatterns=[

    path('login/',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    path('user-logout/',views.user_logout_view,name='user_logout_view'),
    path('vendor-logout/',views.vendor_logout_view,name='vendor_logout_view'),
    path('vendor-login/', views.vendor_login, name='vendor_login'),
    path('vendor-register/', views.vendor_register, name='vendor_register'),
    path('send-otp/<str:email>/', views.sendOTP, name='send_otp'),
    path('verify-otp/<str:email>/', views.verify_otp, name='verify_otp'),
    path('verify-user-account/<str:token>',views.verify_user_account,name='verify_user_account'),
    path('verify-vendor-account/<str:token>',views.verify_vendor_account,name='verify_vendor_account'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('add-hotel/', views.add_hotel, name='add_hotel'),
    path('delete-images/<int:id>/',views.delete_images, name='delete_images'),
    path('<slug:slug>/edit-hotel/', views.edit_hotel, name='edit_hotel'),
    path('<slug>/upload-images/',views.upload_images, name='upload_images'),
    
]