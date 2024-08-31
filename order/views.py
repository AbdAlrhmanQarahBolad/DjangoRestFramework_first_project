from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework import status
from .models import *
from .serializers import *
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    user = request.user
    orders= Order.objects.filter(user=user)
    serializer = OrderSerializer(orders,many=True)
    return Response({"my orders":serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders= Order.objects.all()
    serializer = OrderSerializer(orders,many=True)
    return Response({"orders":serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request,pk):
    order= get_object_or_404(Order,id=pk)
    serializer = OrderSerializer(order,many=False)
    return Response({"order":serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def process_order(request,pk):
    order= get_object_or_404(Order,id=pk)
    order.order_status = request.data['status']
    order.save()

    serializer = OrderSerializer(order,many=False)
    return Response({"order":serializer.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request,pk):
    order= get_object_or_404(Order,id=pk)
    order.delete()
    return Response({"details":"order deleted successfully"})





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    data = request.data
    user = request.user
    order_items = data['order_Items']
    if order_items and len(order_items)==0 :
        return Response({"error":"No order recived"},status=status.HTTP_400_BAD_REQUEST)
    else :
        total_amount = sum(item['price']* item['quantity'] for item in order_items)
        order = Order.objects.create(
            user = user ,
            city = data['city'],
            zip_code = data['zip_code'],
            phone_no = data['phone_no'],
            country = data['country'],
            street = data['street'],
            state = data['state'],

            total_amount = total_amount
        )

        for i in order_items:
            product = Product.objects.get(id=i['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order ,
                name = product.name ,
                quantity = i['quantity'],
                price = i['price'],

            )
            product.stock -= item.quantity
            product.save()
        serializer = OrderSerializer(order,many=False)
        return Response(serializer.data)