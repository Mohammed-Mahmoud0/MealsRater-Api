from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MealViewset, RatingViewset

router = routers.DefaultRouter()
router.register('meals', MealViewset)
router.register('ratings', RatingViewset)

urlpatterns = [
    path('', include(router.urls)),
]
