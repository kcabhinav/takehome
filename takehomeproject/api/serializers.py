from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser
import re


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    referrer_code = serializers.CharField(max_length=8, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'mobile_number', 'city', 'password', 'referral_code', 'referrer_code', 'referred_by']

    def validate_email(self, value):
        # Email format validation
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Invalid email format")

        # Email uniqueness validation
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value.lower()

    def validate_mobile_number(self, value):
        # Simple mobile number validation (can be adjusted based on requirements)
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Mobile number must be 10 digits")
        return value

    def validate_password(self, value):
        # Password strength validation
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number")
        return

    def validate(self, data):
        # Validate referrer code if provided
        self.referrer_code = data.get('referrer_code')
        if self.referrer_code:
            try:
                CustomUser.objects.get(referral_code=self.referrer_code)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError({"referrer_code": "Invalid referral code"})

        return data

    def create(self, validated_data):
        # Remove confirm_password and referrer_code from validated_data
        referrer_code = validated_data.pop('referrer_code', None)

        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])

        # store id of referrer if provided
        if referrer_code:
            validated_data['referred_by'] = CustomUser.objects.get(referral_code=referrer_code)


        # Create and return the user
        return CustomUser.objects.create(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        # Check if user exists
        try:
            user = CustomUser.objects.get(email=data['email'].lower())
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        # Validate password
        if not check_password(data['password'], user.password):
            raise serializers.ValidationError("Invalid email or password")

        # Add user to validated data for view to use
        data['user'] = user
        return data


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'created_at']


