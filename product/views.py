from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from .filters import ProductsFilter
from .models import Product, Review
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg

# Create your views here.

@api_view(['GET'])
def get_all_products(request):
    filterset = ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    paginator = PageNumberPagination()
    paginator.page_size = 12
    #products = Product.objects.all()
    queryset = paginator.paginate_queryset(filterset.qs,request)
    serializer = ProductSerializer(queryset,many=True)
    #print(products)
    return Response({"products":serializer.data, "per page": 2 , "count": count})


@api_view(['GET'])
def get_by_id_product(request,pk):
    product = get_object_or_404(Product,id=pk)
    serializer = ProductSerializer(product,many=False)
    return Response({"product":serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)

    if serializer.is_valid():
        product = Product.objects.create(**data,user=request.user)
        res = ProductSerializer(product, many=False)

        return Response({"product":res.data})
    else :
        return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_product(request,pk):
    product  = get_object_or_404(Product,id=pk)
    
    if product.user != request.user:
        return Response({"error":"sorry you cant update this product"},
                        status=status.HTTP_403_FORBIDDEN)
    product.name = request.data['name']
    product.brand = request.data['brand']
    product.price = request.data['price']
    product.category = request.data['category']
    product.stock = request.data['stock']
    product.ratings = request.data['ratings']
    product.description = request.data['description']
    product.save()
    serializer = ProductSerializer(product,many=False)

    return Response({"product":serializer.data})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_product(request,pk):
    product  = get_object_or_404(Product,id=pk)
    
    if product.user != request.user:
        return Response({"error":"sorry you cant update this product"},
                        status=status.HTTP_403_FORBIDDEN)
    
    product.delete()

    return Response({"details":"Deleted succesfully"},status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)
    data = request.data
    review = product.reviews.filter(user = user)

    

    if data['rating'] <=0 or data['rating']>10:
        return Response({"error":"please select between 1 to 5 only"},status=status.HTTP_400_BAD_REQUEST)
    elif review.exists():
        new_review = {"rating":data["rating"],'comment':data['comment']}
        review.update(**new_review)
        
        rating = product.reviews.aggregate(avg_rating = Avg('rating'))
        product.ratings = rating['avg_rating']
        product.save()
        return Response({"details":"product review updated"})
    else :
        Review.objects.create(
            user=user,
            product=product,
            rating=data['rating'],
            comment = data['comment']
        )
        rating = product.reviews.aggregate(avg_rating = Avg('rating'))
        product.ratings = rating['avg_rating']
        product.save()

        return Response({"details":"product review created"})
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)

    review = product.reviews.filter(user=user)

    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_rating=Avg('rating'))
        if rating['avg_rating'] is None :
            rating['avg_rating'] = 0
        product.ratings = rating['avg_rating']
        product.save()
        return Response({"details":"product review deleted"})

    else :
        return Response({"error":"Review not found"},status=status.HTTP_404_NOT_FOUND)