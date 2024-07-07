# from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel
from django.contrib import admin
# Register your models here.

# CarModelInline class
admin.site.register(CarMake)
admin.site.register(CarModel)
# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
