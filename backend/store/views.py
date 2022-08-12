from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import status
from django.db.models import Count
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer


# Create your views here.

class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return  Product.objects.select_related('collection').all()

    def get_serializer_class(self):
        return ProductSerializer

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset= Product.objects.all()
    serializer_class=ProductSerializer

    def delete(self,request,pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(f"{product.title} deleted", status=status.HTTP_204_NO_CONTENT)



# Collection API
class CollectionList(ListCreateAPIView):
    queryset=Collection.objects.annotate(
            product_count=Count('products')).all()

    serializer_class=CollectionSerializer

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset=Collection.objects.annotate(
            product_count=Count('products')).all()

    serializer_class=CollectionSerializer
    
    def delete(self,request,pk):
        collection = get_object_or_404(Collection.objects.annotate(
        product_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products'})
        collection.delete()
        return Response(f"{collection.title} is deleted", status=status.HTTP_204_NO_CONTENT)