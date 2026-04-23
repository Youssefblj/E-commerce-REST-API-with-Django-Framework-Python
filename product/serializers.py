from rest_framework import serializers
from .models import Product, Review

class Productserializer (serializers.ModelSerializer):
    
    review = serializers.SerializerMethodField(method_name='get_review',read_only=True)
    
    class Meta:
        model = Product
        fields = "__all__"
        
    def get_review(self, obj):
        reviews = obj.reviews.all()
        serializer = Reviewserializer(reviews, many=True)
        return serializer.data
        

class Reviewserializer (serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = "__all__"
        