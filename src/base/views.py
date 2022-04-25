from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from .serializers import UserSerializer
from .serializers import UserSerializerWithToken
from .serializers import ItemSerializer
from .serializers import OrderSerializer
from .serializers import DiscountSerializer

from .models import Item, Order, OrderItem, ShippingAddress, DiscountCode

from django.http import JsonResponse

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.db.models import Q

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Search':'/search/<str:pk>',
        'Item Detail':'/get-item/<str:pk>',
        'Create Item':'/create-item',
        'Update Item':'/update-item/<str:pk>',
        'Delete Item':'/delete-item/<str:pk>',
    }
    return Response(api_urls)


"""
Item Functions
"""

@api_view(['GET'])
def getItems(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    items = Item.objects.filter(
        Q(topic__icontains=query) | 
        Q(item_name__icontains=query) |
        Q(description__icontains=query)
    )
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getItem(request, pk):
    curItem = Item.objects.get(id=pk)
    serializer = ItemSerializer(curItem, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createItem(request):
    item = Item.objects.create(
        item_name = 'Sample Name',
        price = 0,
        quantity = 0,
        description = ''
    )
    serializer = ItemSerializer(item, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateItem(request, pk):
    data = request.data
    updateItem = Item.objects.get(id=pk)

    updateItem.item_name = data['name']
    updateItem.topic = data['topic']
    updateItem.quantity = data['stock']
    updateItem.description = data['description']
    updateItem.price = data['price']
    updateItem.save()

    serializer = ItemSerializer(updateItem, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def updateImage(request):
    data = request.data
    product_id = data['product_id']
    product = Item.objects.get(id=product_id)
    product.image = request.FILES.get('image')
    product.save()
    return Response('Image was uploaded')

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteItem(request, pk):
    curItem = Item.objects.get(id=pk)
    curItem.delete()
    return Response("Item Deleted!")


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createDiscount(request):
    discount = DiscountCode.objects.create(
        name = 'Sample',
        discount = 0.0,
    )
    serializer = DiscountSerializer(discount, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateDiscount(request, pk):
    data = request.data
    updateDiscount = DiscountCode.objects.get(id=pk)

    updateDiscount.name = data['name']
    updateDiscount.discount = data['discount']

    updateDiscount.save()

    serializer = DiscountSerializer(updateDiscount, many=False)

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteDiscount(request, pk):
    curDiscount = DiscountCode.objects.get(id=pk)
    curDiscount.delete()
    return Response("Item Deleted!")


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getDiscounts(request):
    curDiscount = DiscountCode.objects.all()
    serializer = DiscountSerializer(curDiscount, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getDiscount(request, pk):
    curDiscount = DiscountCode.objects.get(id=pk)
    serializer = DiscountSerializer(curDiscount, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def confirmDiscount(request, pk):
    try:
        curDiscount = DiscountCode.objects.get(name=pk)
        serializer = DiscountSerializer(curDiscount, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'This Discount Code does not exist!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
"""
User Functions
"""

@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    curUser = User.objects.get(id=pk)
    serializer = UserSerializer(instance=curUser, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userToDelete = User.objects.get(id=pk)
    userToDelete.delete()
    return Response('User was deleted') 


"""
Order Functions
"""

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # (1) Create Order
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )
        # (2) Create Shipping Address
        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postal'],
            country = data['shippingAddress']['country'],
        )
        # (3) Create Order Items and set order to orderItem relationship
        for i in orderItems:
            product = Item.objects.get(id=i['product'])

            item = OrderItem.objects.create(
                item=product,
                order=order,
                name=product.item_name,
                quantity=i['qty'],
                price=i['price'],
                image = product.image,
            )

            # (4) Update Item quantity

            product.quantity -= item.quantity
            product.save()

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    try:
        order = Order.objects.get(id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail':'You are not authorized to see this order'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return  Response({'detail':'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)
