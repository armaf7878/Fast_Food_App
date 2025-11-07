from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import RestaurantSerializer
from .models import Restaurant

@api_view(['GET'])
def showall(request):
    restaurants = Restaurant.objects.all().order_by('-restaurant_id')
    serializers = RestaurantSerializer(restaurants, many = True, context = {'request': request})
    return Response({
        'message': 'Danh sách tất cả nhà hàng',
        'data': serializers.data
    }, status= status.HTTP_200_OK)

@parser_classes([MultiPartParser, FormParser])
@api_view(['POST'])
def create(request):
    serializer = RestaurantSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Showall Restaurant',
            'restaurant': serializer.data
        }, status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def update(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except:
        return Response({'error': 'Lỗi không tìm thấy nhà hàng'}, status=status.HTTP_404_NOT_FOUND)
    serializer = RestaurantSerializer(restaurant, data = request.data, partial = True , context = {'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({
        'message': ' Cập nhật nhà hàng thành công',
        'data': serializer.data
    }, status=status.HTTP_200_OK)
    return Response({
        'error': serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(pk = restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({'error':'Không tìm thấy nhà hàng'}, status=status.HTTP_404_NOT_FOUND)
    restaurant.delete()
    return Response({
        'message': 'Xóa nhà hàng thành công'
    }, status= status.HTTP_200_OK)
