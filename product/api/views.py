from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from product.api.serializers import UserSerializer, GroupSerializer, UserModelSerializer, ProductModelSerializer, TokenModelSerializer
from product.api.models import ProductModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework import status, generics
from datetime import datetime
import math


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


class RegisterUser(APIView):
    permission_classes = ()
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        print(request.data)
        queryset = User.objects.filter(username=request.data.get("username"))
        user = self.serializer_class(queryset, many=True)

        if len(user.data) > 0:
            return Response('Username already registered!')

        user = {
            "username": request.data.get("username"),
            "password": make_password(request.data.get("password"))
        }

        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
            # Had some difficulty initially in creating token for only the new user
            # for user in User.objects.all():
            #     Token.objects.get_or_create(user=user)
            return Response('Successfully Registered!')
        else:
            return Response('Invalid Credentials!')


class Products(generics.GenericAPIView):
    serializer_class = ProductModelSerializer
    queryset = ProductModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        products = ProductModel.objects.all()
        total_products = products.count()
        if search_param:
            products = products.filter(name__icontains=search_param)
        serializer = self.serializer_class(products[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_products,
            "page": page_num,
            "last_page": math.ceil(total_products / limit_num),
            "notes": serializer.data
        })

    def post(self, request):
        user_from_token = Token.objects.get(key=(request.headers.get('Authorization').split())[1])
        user_from_token = TokenModelSerializer(user_from_token)
        request.data["user_id"] = user_from_token.data.get("user")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"product": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(generics.GenericAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get_product(pk):
        try:
            return ProductModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        product = self.get_product(pk=pk)
        if product is None:
            return Response({
                "status": "fail",
                "message": f"Note with Id: {pk} not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(product)
        return Response({
            "status": "success",
            "data": {
                "product": serializer.data
            }
        })

    def patch(self, request, pk):
        product = self.get_product(pk)
        if product is None:
            return Response({
                "status": "fail",
                "message": f"Note with Id: {pk} not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({
                "status": "success",
                "data": {
                    "product": serializer.data
                }
            })
        return Response({
            "status": "fail",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_product(pk)
        if product is None:
            return Response({
                "status": "fail",
                "message": f"Note with Id: {pk} not found"
            }, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({
            "status": "success",
            "data": "Deleted Successfully!"
        }, status=status.HTTP_204_NO_CONTENT)
