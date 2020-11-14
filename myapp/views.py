from rest_framework.views import APIView, Response
from .serializers import EmailAddSerializer, OTPVerifySerializer
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.core.cache import cache


# Create your views here.


class EmailInput(APIView):
    serializer_class = EmailAddSerializer
    def post(self, request, *args, **kwargs):
        try:
            otp = get_random_string(length=6, allowed_chars='1234567890')
            email = request.POST.get('email')
            send_mail(
                'Email Verification OTP',
                otp,
                'sharshil07@gmail.com',
                [email],
                fail_silently=True,
            )
            cache.set(email, int(otp), 120)
            return Response({'response':'otp sent successfully'}, status= 201)
        except Exception as ex:
            print(ex)
            return Response(status=500, exception=True, data={'error':'internal server error'})
        # return super(EmailAddSerializer, self).create(validated_data)

class OTPVerify(APIView):
        serializer_class = OTPVerifySerializer
        
        def post(self, request, *args, **kwargs):
            try:
                email = request.POST.get('email')
                user_otp = request.POST.get('otp')
                system_otp = cache.get(email)
                if system_otp == None:
                    return Response({'response':'OTP Expired'}, status=404)
                elif system_otp == int(user_otp):
                    return Response({'response':'Email Is Verified'}, status=202)
                else:
                    return Response({'response':'Invalid OTP'}, status=400)
            except Exception as ex:
                print(ex)
                return Response(status=500, exception=True, data={'error':'internal server error'})