from rest_framework import serializers
from .models import ProductsModel,usersmodel
import re
from django.contrib.auth.hashers import make_password

class productserializer(serializers.ModelSerializer):
    class Meta:
        model=ProductsModel
        fields='__all__'

class usersserializer(serializers.ModelSerializer):
    confirmpassword = serializers.CharField(write_only=True)
    
    class Meta:
        model = usersmodel
        fields = ['username', 'email', 'password', 'address', 'orders', 'confirmpassword']  # Explicitly list fields
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirmpassword = data.get('confirmpassword')
        # instance = getattr(self, 'instance', None)

        # Validation for username
        if len(username) <= 3:
            raise serializers.ValidationError( 'Username must be greater than 3 characters')
        elif re.search(r'[^a-zA-Z]', username) or ' ' in username:
            raise serializers.ValidationError( 'Username must contain only alphabets')
        elif usersmodel.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')
        elif usersmodel.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        elif not all(re.search(pattern, password) for pattern in [r'[a-z]', r'[A-Z]', r'[0-9]', r'[^a-zA-Z0-9\s]']):
            raise serializers.ValidationError('Password must be minimum 8 characters in format (ex: Abcd@#12)')
        elif ' ' in password or len(password) < 8:
            raise serializers.ValidationError('Password must be minimum 8 characters in format (ex: Abcd@#12)')
        elif password != confirmpassword:
            raise serializers.ValidationError('Passwords mismatch')
        
        return data

    def create(self, validated_data):
        confirmpassword = validated_data.pop('confirmpassword', None)
        password = validated_data.pop('password', None)

        if password:
            validated_data['password'] = make_password(password)
        
        return super().create(validated_data)