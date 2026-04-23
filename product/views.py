from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Product, Review
from .serializers import Productserializer, Reviewserializer
from .filtters import ProductsFilter
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

# Create your views here.


@api_view(['GET'])
def get_all_products(request):
    filterset = ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id'))

    respage = 2
    paginator = PageNumberPagination()
    paginator.page_size = respage
    #products =Product.objects.all()
    querysite = paginator.paginate_queryset(filterset.qs, request)
    serializer = Productserializer(querysite, many=True)
    #print(products)
    return Response ({"products":serializer.data})
@api_view(['GET'])
def get_id_products(request,pk):
    products = get_object_or_404(Product,id=pk)
    serializer = Productserializer(products, many=False)
    print(products)
    return Response ({"product":serializer.data})

########################################

@api_view(['POST'])

@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = Productserializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data,user=request.user)
        res = Productserializer(product, many=False)
        return Response({"product":res.data})
    else:
        return Response(serializer.errors)
    
########################################
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response({"error": "You are not the owner of this product"}, status=status.HTTP_403_FORBIDDEN)
    
    product.name = request.data["name"]
    product.description = request.data["description"]
    product.price = request.data["price"]  
    product.brand = request.data["brand"]
    product.category = request.data["category"]
    product.ratings = request.data["ratings"]
    product.stock = request.data["stock"] 
    product.save()
    serializer = Productserializer(product, many=False)
    return Response({"product": serializer.data})

###############################################################
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response({"error": "You are not the owner of this product"}, status=status.HTTP_403_FORBIDDEN)
    
    product.delete()
    return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)
    data = request.data
    user_review = product.reviews.filter(user=user)
    if data['rating'] <= 0 or data['rating'] > 10:
        return Response({"error": "Rating must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)
    
    elif user_review.exists():
        new_review = {"rating": data['rating'], "comment": data['comment']}
        user_review.update(**new_review)
        
        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({"message": "Review updated successfully"}, status=status.HTTP_200_OK)
    else:
        Review.objects.create(user=user,
                              product=product,
                              rating=data['rating'],
                              comment=data['comment'])
        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
        product.ratings = rating['avg_ratings']
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)
   
    review = product.reviews.filter(user=user)
   
 
    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0
            product.ratings = rating['avg_ratings']
            product.save()
            return Response({'details':'Product review deleted'})
    else:
        return Response({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)

