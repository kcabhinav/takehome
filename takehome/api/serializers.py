# serializers.py in your 'accounts' app
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Referral, CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'name',
            'email',
            'mobile_number',
            'city',
            'password',
            'referral_code'
        ]

    def validate(self, data):
        validation_map = {
            'name': 'Name cannot be empty',
            'email': 'Email cannot be empty',
            'mobile_number': 'Mobile number cannot be empty',
            'city': 'City cannot be empty',
            'password': 'Password cannot be empty',
        }
        for field, message in validation_map.items():
            if not data.get(field):
                raise serializers.ValidationError(message)
        return data

    def create(self, validated_data):
        """
        Create an object of data coming in the request. If the request contains a referral code, map the owner of the referral code as 
        the referred_by field. If the request does not contain a referral code, set the referred_by field to null. If invalid referral code
        return an error.
        """
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password'])
        if 'referral_code' in validated_data:
            try:
                referrer = CustomUser.objects.get(
                    referral_code=validated_data['referral_code'])
                validated_data['referred_by'] = referrer
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(
                    {'referral_code': 'Invalid referral code.'})
        else:
            validated_data['referred_by'] = None
        return CustomUser.objects.create(**validated_data)

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, data):
        validation_map = {
            'name': 'Name cannot be empty',
            'email': 'Email cannot be empty',
            'mobile_number': 'Mobile number cannot be empty',
            'city': 'City cannot be empty',
            'password': 'Password cannot be empty',
        }
        for field, message in validation_map.items():
            if not data.get(field):
                raise serializers.ValidationError(message)
        return data
