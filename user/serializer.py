from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['email']


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        if email and otp:
            try:
                user = User.objects.get(email=email)
                if user.otp != otp:
                    raise serializers.ValidationError("Invalid OTP")
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist")
        else:
            raise serializers.ValidationError("Must include 'email' and 'otp'")

        data['user'] = user
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'is_verified', 'first_name', 'last_name', 'otp', 'phone', 
            'Address', 'pan_number', 'Adhar_number', 'photo'
        ]
        extra_kwargs = {
            'email': {'read_only': True},  # Make email read-only to prevent changes
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
