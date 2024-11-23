from .serializers import (
    UserRegistrationSerializer,
    UserViewSerializer,
    # UserLoginSerializer,
    # ReferralCodeSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Referral, CustomUser


@api_view(['GET'])
def viewUsers(request):
    querySet = CustomUser.objects.all()
    serializer = UserViewSerializer(instance=querySet, many=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    # Use the UserRegistrationSerializer to validate input data
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        # Check if referral code exists and is valid
        referral_code = request.data.get('referral_code')
        if referral_code:
            try:
                referrer = CustomUser.objects.get(referral_code=referral_code)
                user = serializer.save(referred_by=referrer)  # referrer
                Referral.objects.create(referrer=referrer, referee=user)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "Invalid referral code."},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.save()  # No referral code, just save user

        return Response({
            "message": "User registered successfully.",
            "user_id": user.id,
            "email": user.email,
            "referral_code": user.referral_code
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def login(request):
#     serializer = UserLoginSerializer(data=request.data)
#
#     if serializer.is_valid():
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)
#
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['POST'])
# def verify_referral(request):
#     # Use the ReferralCodeSerializer to validate the referral code
#     serializer = ReferralCodeSerializer(data=request.data)
#
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return Response(serializer.data, status=status.HTTP_200_OK)
