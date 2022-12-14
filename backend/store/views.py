from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer


# Create your views here.


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        query_set = Product.objects.select_related('collection').all()
        instance = ProductSerializer(query_set, many=True)
        return Response(instance.data)
    elif request.method == 'POST':
        instance = ProductSerializer(data=request.data)
        instance.is_valid(raise_exception=True)
        instance.save()
        return Response(instance.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        instance = ProductSerializer(product)
        return Response(instance.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        product.delete()
        return Response(f"{product.title} deleted", status=status.HTTP_204_NO_CONTENT)


# Collection API
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        query_set = Collection.objects.annotate(
            product_count=Count('products')).all()
        instance = CollectionSerializer(query_set, many=True)
        return Response(instance.data)

    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(
        product_count=Count('products')), pk=pk)
    if request.method == 'GET':
        instance = CollectionSerializer(collection)
        return Response(instance.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted becuase it includes one or more products'})
        collection.delete()
        return Response(f"{collection.title} is deleted", status=status.HTTP_204_NO_CONTENT)
