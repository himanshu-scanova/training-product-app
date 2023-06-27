from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from product.api.models import ProductModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            "password": {'write_only': True},
            "last_login": {'write_only': True},
            "is_superuser": {'write_only': True},
            "is_staff": {'write_only': True},
            "is_active": {'write_only': True},
            "date_joined": {'write_only': True},
            "groups": {'write_only': True},
            "user_permissions": {'write_only': True}
        }


class TokenModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'
