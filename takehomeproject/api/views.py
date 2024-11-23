from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ReferralSerializer, UserViewSerializer


class ListUsersView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserViewSerializer(users, many=True)
        return Response(serializer.data)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'name': user.name,
            'email': user.email,
            'referral_code': user.referral_code
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data['user']
        return Response({
            'user_id': user.id,
            'email': user.email
        })


class ReferralListView(APIView):
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            referrals = user.referrals.all()
            serializer = ReferralSerializer(referrals, many=True)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

