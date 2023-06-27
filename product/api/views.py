from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from product.api.serializers import \
    UserSerializer, GroupSerializer, UserModelSerializer, ProductModelSerializer
from product.api.models import ProductModel
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from django.shortcuts import render


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterUser(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            password=make_password(self.request.data.get("password"))
        )


class Products(generics.ListCreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [permissions.IsAuthenticated]


def product_html(request, pk):
    product = ProductModel.objects.get(pk=pk)
    product = ProductModelSerializer(product)
    return render(request, 'product.html', product.data)
