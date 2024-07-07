"""
Django app admin module
"""
# from .models import related models
from django.contrib import admin
from .models import CarMake, CarModel
# Register your models here.

# CarModelInline class
admin.site.register(CarMake)
admin.site.register(CarModel)
# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
