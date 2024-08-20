from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer,VerifySerializer,UserUpdateSerializer,LoginSerializer
from rest_framework import status
from .email import send_otp_via_email
from .models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class UserRegitration(APIView):
    def post(self, request):
        try:
            # import pdb;pdb.set_trace()
            data = request.data
            ser=UserSerializer(data=data)
            if ser.is_valid():
                ser.save()
                send_otp_via_email(ser.data['email'])
                return Response({
                    'status':200,
                    'massage':'regitration successfull check email',
                    'data':ser.data
                })
            
            return Response({
                    'status':400,
                    'massage':'something went worng',
                    'data':ser.errors
                })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'error': e
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class VerifiedAPI(APIView):
#     def post(self, request):
#         try:
#             #import pdb;pdb.set_trace()
#             data = request.data
#             ser=VerifySerializer(data=data)
#             if ser.is_valid():
#                 email = ser.data['email']
#                 otp = ser.data['otp']
                
#                 user = User.objects.filter(email=email)
                
#                 if not user.exists():
#                     return Response({
#                     'status':400,
#                     'massage':'something went worng',
#                     'data':'invalid email'
#                 })
                
#                 if user[0].otp != otp:
#                     return Response({
#                     'status':400,
#                     'massage':'something went worng',
#                     'data':'worng otp'
#                 })

#                 usr=user.first()
#                 usr.is_verified = True
#                 usr.save()


#                 return Response({
#                     'status':200,
#                     'massage':'Account verified',
#                     'data':ser.data
#                 })
            
#             return Response({
#                     'status':400,
#                     'massage':'something went worng',
#                     'data':{},
#                 })
#         except Exception as e:
#             print(e)
#             return Response({
#                 'status': 500,
#                 'message': 'Internal server error',
#                 'error':e
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VerifyAndLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # import pdb;pdb.set_trace()
            data = request.data
            verify_serializer = VerifySerializer(data=data)
            
            if verify_serializer.is_valid():
                email = verify_serializer.data['email']
                otp = verify_serializer.data['otp']
                
                user = User.objects.filter(email=email)
                
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'Invalid email'
                    })

                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'Wrong OTP'
                    })

                usr = user.first()
                usr.is_verified = True
                usr.save()

                # Proceed to login the user after verification
                login_serializer = LoginSerializer(data=data)
                if login_serializer.is_valid():
                    user = login_serializer.validated_data['user']
                    login(request, user)

                    # Generate a token for the user
                    token, created = Token.objects.get_or_create(user=user)

                    return Response({
                        "status": 200,
                        "message": "Account verified and logged in",
                        "token": token.key,
                        "user_id": user.pk,
                        "email": user.email
                    }, status=status.HTTP_200_OK)

            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': verify_serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


@permission_classes([IsAuthenticated])
class UserUpdateView(APIView):
    def patch(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # `partial=True` allows for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
