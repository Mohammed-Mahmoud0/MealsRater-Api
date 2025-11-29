from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum

# Create your models here.


class Meal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def num_of_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        return len(ratings)

    def avg_rating(self):
        ratings = Rating.objects.filter(meal=self)
        # note that there is 2 methods to calculate the total
        # 1st method is using a for loop
        # 2nd method is using aggregate function(this is more efficient cuz it does it in the database level)
        # total = sum([rating.stars for rating in ratings])
        total = ratings.aggregate(Sum("stars"))["stars__sum"]
        if total is None:
            return 0
        return total / len(ratings)

    def __str__(self):
        return self.title


class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.meal.title

    class Meta:
        unique_together = (("user", "meal"),)
        indexes = [
            models.Index(fields=["user", "meal"]),
        ]
