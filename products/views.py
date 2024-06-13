import json

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.admin:
            response_data = {"Message": "Only an admin can add products"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        many = False
        if isinstance(request.data, list):
            many = True
        serializer = ProductSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        if not request.user.admin:
            response_data = {"Message": "Only an admin can update products"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.admin:
            response_data = {"Message": "Only an admin can update products"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        product = self.get_object(pk)
        product.delete()
        response_data = {"Message": f"Succesfully deleted item with PK={pk}"}
        return Response(status=status.HTTP_204_NO_CONTENT)
