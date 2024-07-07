"""
Django app models module
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


User = get_user_model()
class CarMake(models.Model):
    """
    Car Make class
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return str(self.name)
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    """
    Car Model class
    """
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(default=0)
    name = models.CharField( max_length=50)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
            ('SUV', 'SUV'),
            ('WAGON', 'Wagon'),
            ('SPORT', 'Sport'),
            ('OTHER', 'Other')
    ]

    type = models.CharField( max_length=50, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(_('year'), validators=[
        MinValueValidator(2015),
        MaxValueValidator(2023)])

    def __str__(self):
        return str(self.name)
