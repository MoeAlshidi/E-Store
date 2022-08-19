

from decimal import Decimal
from pyexpat import model
import re
from .models import Cart, CartItem, Product, Collection, Review
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory',
                  'unit_price', 'price_with_tax',  'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(0.05)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','name','description','date']

    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField()

    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity*cart_item.product.unit_price
    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_price']



class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField()

    def get_total_price(self,cart:Cart):
        return sum([item.quantity*item.product.unit_price for item in cart.items.all()])
    class Meta:
        model=Cart
        fields=['id','items','total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    def validate_Product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No Product with the same ID is found')
        return value
    #Adding None Duplicate Items To The Cart
    def save(self, **kwargs):
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        cart_id=self.context['cart_id']
        try:
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance=cart_item 
        except CartItem.DoesNotExist:
          self.instance=  CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']


class UpdateCartItemSerializer(serializers.ModelField):
    class Meta:
        model=CartItem
        fields=['quantity']

