from rest_framework import serializers
from django.db import transaction

from .models import Profile

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class ProfileCreateSerializer(serializers.Serializer):
    """Create user and profile attached to a client."""
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(
        validators=[Profile.phone_regex]
    )
    hobbies = serializers.CharField(max_length=255, required=False)

    def validate_email(self, email):
        """Check if email is unique."""
        if Profile.objects.filter(user__email=email).exists():
            raise serializers.ValidationError(
                'Email already exists'
            )
        return email

    def validate_phone_number(self, phone):
        """Check if phone number is unique."""
        if Profile.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                'Phone number already exists'
            )
        return phone
    
    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'])
            profile = Profile.objects.create(
                user=user,
                phone=validated_data['phone'],
                hobbies=validated_data.get('hobbies', None)
            )
            return profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Profile
        fields = [
            'pk',
            'user',
            'phone',
            'hobbies',
            'phone_validated',
            'email_validated'
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()
    
    class Meta:
        model = Profile
        fields = [
            'user',
            'phone',
            'hobbies'
        ]
        
    def validate(self, attrs):
        if user := attrs.get('user', None):
            if email:= user.get('email', None):
                if Profile.objects.filter(user__email=email).exists() and not self.instance.user.email == email:
                    raise serializers.ValidationError(
                        'Email already exists'
                    )
        if phone:= user.get('phone', None):
            if Profile.objects.filter(phone=phone).exists() and not self.instance.phone == phone:
                raise serializers.ValidationError(
                    'Phone number already exists'
                )
        
        return super().validate(attrs)

    def update(self, instance, validated_data, *args, **kwargs):
        if user_dyct:=validated_data.get('user', None):
            user = instance.user
            validated_data.pop('user')
            for field, value in user_dyct.items():
                if hasattr(user, field) and value != '':
                    setattr(user, field, value)
            user.save()

        for field, value in validated_data.items():
            if hasattr(instance, field) and value != '':
                setattr(instance, field, value)
        instance.save()

        return instance
