from django.shortcuts import render
from rest_framework import viewsets
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer

# Create your views here.


class MealViewset(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
