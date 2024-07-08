"""
This module contains functions to interact with the
backend and sentiment analyzer
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# def get_request(endpoint, **kwargs):
# Add code for get requests to back end
def get_request(endpoint, **kwargs):
    """
    This function sends a GET request to the backend
    """
    params = ""
    if kwargs:
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    
    if params == "":
        request_url = backend_url+endpoint
    else:
        request_url = backend_url+endpoint+"?"+params

    print(f"GET from {request_url} ")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url,timeout=5)
        return response.json()
    except requests.exceptions.RequestException as err :
        # If any error occurs
        print(f"Network exception occurred {err}")
        return None
# def analyze_review_sentiments(text):
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments

def analyze_review_sentiments(text):
    """
    This function sends a GET request to the sentiment analyzer
    """
    request_url = sentiment_analyzer_url+"/analyze/"+text
    print(f"GET from {request_url} ")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url,timeout=5)
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException  as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None

# def post_review(data_dict):
# Add code for posting review
def post_review(data_dict):
    """
    This function sends a POST request to the backend
    """
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict,timeout=5)
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException :
        print("Network exception occurred")
        return None
