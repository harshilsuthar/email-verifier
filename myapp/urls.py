from django.urls import path
from .views import EmailInput, OTPVerify
urlpatterns = [
    path('generate_otp',EmailInput.as_view(),name='EmailInput'),
    path('verify_otp', OTPVerify.as_view(), name='OTPVerify')
]