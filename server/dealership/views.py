from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import Dealer, Review


@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password required"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"error": "User already exists"},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password
    )

    return JsonResponse({
        "message": "User registered successfully",
        "username": user.username
    }, status=201)


@csrf_exempt
def loginuser(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    username = data.get("username")
    password = data.get("password")

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is None:
        return JsonResponse(
            {"error": "Invalid credentials"},
            status=401
        )

    login(request, user)

    return JsonResponse({
        "message": "Login successful",
        "username": user.username
    })


@csrf_exempt
def logoutuser(request):
    logout(request)

    return JsonResponse({
        "message": "Logout successful",
        "userName": ""
    })


def getalldealers(request):
    dealers = Dealer.objects.all()

    data = []

    for dealer in dealers:
        data.append({
            "id": dealer.id,
            "name": dealer.name,
            "address": dealer.address,
            "city": dealer.city,
            "state": dealer.state,
            "zip_code": dealer.zip_code,
            "full_name": dealer.full_name,
            "st": dealer.st,
        })

    return JsonResponse(data, safe=False)


def getdealerbyid(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"error": "Dealer not found"},
            status=404
        )

    return JsonResponse({
        "id": dealer.id,
        "name": dealer.name,
        "address": dealer.address,
        "city": dealer.city,
        "state": dealer.state,
        "zip_code": dealer.zip_code,
        "full_name": dealer.full_name,
        "st": dealer.st,
    })


def getdealersbyState(request, state):
    dealers = Dealer.objects.filter(
        state__iexact=state
    )

    data = []

    for dealer in dealers:
        data.append({
            "id": dealer.id,
            "name": dealer.name,
            "address": dealer.address,
            "city": dealer.city,
            "state": dealer.state,
            "zip_code": dealer.zip_code,
            "full_name": dealer.full_name,
            "st": dealer.st,
        })

    return JsonResponse(data, safe=False)


@login_required
def getdealerreviews(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"error": "Dealer not found"},
            status=404
        )

    reviews = Review.objects.filter(
        dealer=dealer
    )

    data = []

    for review in reviews:
        data.append({
            "id": review.id,
            "dealer": dealer.id,
            "user": review.user.username,
            "review": review.review,
            "sentiment": review.sentiment,
            "created_at": review.created_at,
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required
def submit(request, dealer_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    review_text = data.get("review")

    if not review_text:
        return JsonResponse(
            {"error": "Review required"},
            status=400
        )

    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"error": "Dealer not found"},
            status=404
        )

    review = Review.objects.create(
        dealer=dealer,
        user=request.user,
        review=review_text,
        sentiment=analyze_sentiment(review_text)
    )

    return JsonResponse({
        "message": "Review submitted successfully",
        "review": review.review,
        "sentiment": review.sentiment
    }, status=201)


def analyze_sentiment(text):
    positive_words = [
        "good",
        "great",
        "excellent",
        "fantastic",
        "amazing",
        "helpful",
        "friendly",
        "best"
    ]

    negative_words = [
        "bad",
        "poor",
        "terrible",
        "awful",
        "worst",
        "slow",
        "rude"
    ]

    text = text.lower()

    positive = sum(
        word in text for word in positive_words
    )

    negative = sum(
        word in text for word in negative_words
    )

    if positive > negative:
        return "positive"

    elif negative > positive:
        return "negative"

    return "neutral"


@csrf_exempt
def analyzereview(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    try:
        data = json.loads(request.body)
        review = data.get("review", "")
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    return JsonResponse({
        "review": review,
        "sentiment": analyze_sentiment(review)
    })


def getallcarmakes(request):
    car_makes = [
        "Acura",
        "Audi",
        "BMW",
        "Chevrolet",
        "Ford",
        "Honda",
        "Hyundai",
        "Kia",
        "Mercedes-Benz",
        "Nissan",
        "Toyota",
    ]

    return JsonResponse(
        car_makes,
        safe=False
    )


def analyze_review_get(request, review):
    return JsonResponse({
        "review": review,
        "sentiment": analyze_sentiment(review)
    })