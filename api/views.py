from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# Create your views here.


class MealViewset(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(detail=True, methods=["post"])
    def rate_meal(self, request, pk=None):
        meal = Meal.objects.get(id=pk)
        stars = request.data["stars"]
        username = request.data["username"]
        user = User.objects.get(username=username)
        if "stars" in request.data:
            try:
                rate = Rating.objects.get(user=user.id, meal=meal.id)
                rate.stars = stars
                rate.save()
                serializer = RatingSerializer(rate, many=False)
                json = {"message": "Rating updated", "result": serializer.data}
                return Response(json, status=status.HTTP_200_OK)
            except:
                rate = Rating.objects.create(stars=stars, meal=meal, user=user)
                serializer = RatingSerializer(rate, many=False)
                json = {"message": "Rating created", "result": serializer.data}
                return Response(json, status=status.HTTP_201_CREATED)
        else:
            json = {"message": "You need to provide stars"}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)


class RatingViewset(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
