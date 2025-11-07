from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import FoodSerializer

@api_view(['GET'])
def showall(request):
    return JsonResponse({'NAME': 'showall'})

@api_view(['POST'])
def create(request):
    serializer = FoodSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Tạo món thành công',
            'food' : serializer.data
        }, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete(request, food_id):
    return JsonResponse({'err': 'create'})

@api_view(['PATCH'])
def update(request, food_id):
    return JsonResponse({'err': 'UPDATE'})
