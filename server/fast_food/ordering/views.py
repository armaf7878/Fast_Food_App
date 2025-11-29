from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order
from accounts.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    request.data['user'] = request.user.user_id
    serializer = OrderSerializer(data=request.data)
    
    if serializer.is_valid():
        order = serializer.save()
        return Response({
            "message": "Tạo đơn hàng thành công",
            "order_id": order.order_id
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending(request):
    if request.user.role != "staff":
        return Response({"detail": "Bạn không phải staff"}, status=403)

    orders = Order.objects.filter(status="pending", staff__isnull=True)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cooking(request):
    if request.user.role != "staff":
        return Response({"detail": "Bạn không phải staff"}, status=403)

    orders = Order.objects.filter(status="cooking", staff_id=request.user.user_id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_staff(request, order_id):
    print(request.user.role)
    if request.user.role != "staff":
        return Response({"detail": "Bạn không phải staff"}, status=403)

    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({"detail": "Đơn hàng không tồn tại"}, status=404)

    if order.staff is not None:
        return Response({"detail": "Đơn hàng đã có staff nhận"}, status=400)

    if order.status != "pending":
        return Response({"detail": "Chỉ đơn pending mới nhận"}, status=400)

    order.staff = request.user
    order.status = "cooking"
    order.save()

    return Response({"message": "Nhận đơn thành công!"})

def get_available_shipper():
    return User.objects.filter(role="shipper", is_online=True, is_busy=False).first()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ready(request, order_id):
    if request.user.role != "staff":
        return Response({"detail": "Bạn không phải staff"}, status=403)

    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({"detail": "Đơn hàng không tồn tại"}, status=404)

    if order.staff != request.user:
        return Response({"detail": "Không phải staff phụ trách đơn này"}, status=403)

    if order.status != "cooking":
        return Response({"detail": "Chỉ đơn cooking mới báo hoàn tất chuẩn bị"}, status=400)

    shipper = get_available_shipper()
    if not shipper:
        return Response({"detail": "Không có shipper rảnh"}, status=400)

    shipper.is_busy = True
    shipper.save()

    

    order.shipper = shipper
    order.status = "delivering"
    order.save()

    return Response({
        "message": "Đã gán shipper và chuyển đơn sang delivering",
        "shipper_id": shipper.user_id
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def waiting_Deliver(request):

    if request.user.role != "shipper":
        return Response({"detail": "Bạn không phải shipper"}, status=403)

    orders = Order.objects.filter(shipper=request.user, status="delivering")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finish_order(request, order_id):
    if request.user.role != "shipper":
        return Response({"detail": "Bạn không phải shipper"}, status=403)

    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({"detail": "Đơn hàng không tồn tại"}, status=404)

    if order.shipper != request.user:
        return Response({"detail": "Bạn không phải shipper xử lý đơn này"}, status=403)

    if order.status != "delivering":
        return Response({"detail": "Đơn chưa ở trạng thái delivering"}, status=400)

    order.status = "finish"
    order.save()

    shipper = request.user
    shipper.is_busy = False
    shipper.save()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"order_{order_id}",
        {"type": "order_finished"}
    )

    return Response({"message": "Giao hàng thành công!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orderlist_client(request):

    orders = Order.objects.filter(user_id=request.user.user_id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)