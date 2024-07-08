"""
This module contains views for the djangoapp application
"""
# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime
import json
import logging
import requests
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from .models import  CarModel, User
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    """
    This view handles login requests
    """
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    """
    This view handles logout requests
    """
      # Check if the user is authenticated
    if request.user.is_authenticated:
        # Log the user out
        logout(request)
        # Return a JSON response indicating success
        return JsonResponse({"status": "Logged out"})

    # If the user is not authenticated, return a different response
    return JsonResponse({"status": "User not logged in"}, status=400)


# Create a `registration` view to handle sign up request
# @csrf_exempt
def registration(request):
    """
    This view handles registration requests
    """
    context = {}

    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exists = False
    email_exists = False

    try:
        User.objects.get(username=username)
        username_exists = True
    except requests.exceptions.RequestException :
        logger.debug(_(f"{username} is a new user"))

    if username_exists:
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)

    data = {"userName": username, "error": "User already exists"}
    return JsonResponse(data, status=400)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...
def get_dealerships(request, state="All"):
    """
    This view handles fetching dealerships from the database microservice
    """
    if state != "All":
        endpoint = "/fetchDealers/"+state
    else:
        endpoint = "/fetchDealers"

    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})
# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request,dealer_id):
    """
    This view handles fetching reviews of a dealer from the database microservice
    """
    # if dealer id has been provided
    if dealer_id:
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})

    return JsonResponse({"status":400,"message":"Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request,dealer_id):
    """
    This view handles fetching details of a dealer from the database microservice
    """
    if dealer_id:
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})

    return JsonResponse({"status":400,"message":"Bad Request"})
# Create a `add_review` view to submit a review
# def add_review(request):
def add_review(request):
    """
    This view handles posting reviews to the database microservice
    """
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status":200})
        except requests.exceptions.RequestException :
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})

def get_cars(request):
    """
    This view handles fetching cars from the database microservice
    """
    initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})

    return JsonResponse({"CarModels":cars})
