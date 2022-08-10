
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


@api_view(['GET'])
def say_hello(request):
    return Response({'body': 'Hello World'})
