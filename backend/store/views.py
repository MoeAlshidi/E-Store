from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from .filters import ProductFilter
from .models import Collection, OrderItem, Product, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer


# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class= ProductFilter
    search_fields=['title','description']
    ordering_fields=['unit_price','last_update']
    serializer_class=ProductSerializer
    

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'Product cannot be deleted because it has Order Items '})
        return super().destroy(request,*args,**kwargs)
    

# Collection API

class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(
        product_count=Count('products')).all()
    serializer_class=CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(products=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products'})
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])


    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}