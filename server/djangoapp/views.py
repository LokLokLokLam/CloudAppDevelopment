from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer, CarModel, CarMake
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealers_by_state, get_dealers_by_id, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/5d07c517-6f41-4086-99bf-4e0204e5a497/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        #dealerships = get_dealers_by_state(url, "Texas")
        # Concat all dealer's short name
        #dealer_names = ', '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        #return render(request, 'djangoapp/index.html', context)
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url_dealer = "https://au-syd.functions.appdomain.cloud/api/v1/web/5d07c517-6f41-4086-99bf-4e0204e5a497/dealership-package/get-dealership.json"
        dealerships = get_dealers_by_id(url_dealer, dealer_id)
        print("*******Dealerships*******")
        print(dealerships[0].full_name)
        context['dealer_fullname'] = dealerships[0].full_name

        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/5d07c517-6f41-4086-99bf-4e0204e5a497/dealership-package/get-review.json"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews_detail'] = reviews
        context['dealer_id'] = dealer_id
        #review_join = ', '.join([review.review + " (" + review.sentiment + ")" for review in reviews])
        #return HttpResponse(review_join)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    user = request.user
    print(user)
    if user is not None:
        if request.method == "GET":
            context = {}
            url_dealer = "https://au-syd.functions.appdomain.cloud/api/v1/web/5d07c517-6f41-4086-99bf-4e0204e5a497/dealership-package/get-dealership.json"
            dealerships = get_dealers_by_id(url_dealer, dealer_id)
            context['dealer_fullname'] = dealerships[0].full_name
            car_model = CarModel.objects.filter(dealerId = dealer_id)
            context['cars'] = car_model
            context['dealer_id'] = dealer_id
            return render(request, 'djangoapp/add_review.html', context)

        elif request.method == "POST":
            review = {}
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = "This is a great car dealer"
            review["id"] = 0
            review["name"] = "this is name"
            review["purchase"] = True
            review["purchase_date"] = "06/08/2021"
            review["car_make"] = "This is car make"
            review["car_model"] = "This is car_model"
            review["car_year"] = 2019

            json_payload = {}
            json_payload['review'] = review

            url = "https://au-syd.functions.appdomain.cloud/api/v1/web/5d07c517-6f41-4086-99bf-4e0204e5a497/dealership-package/post-review.json"
            result = post_request(url, json_payload, dealerId=dealer_id)
            print("***Post Review Result: ***")
            print(result)
            return redirect("djangoapp:index")
    return redirect("djangoapp:index")

