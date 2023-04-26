from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListing, PlaceBid
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Category


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    submitted = False
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():            
            complete_form = form.save(commit=False)       ## saves form but doesnt commit to db. Allows us to populate creator field with currently logged in
            complete_form.creator = request.user
            complete_form.save()
            submitted = True
            return render(request, "auctions/create.html", {
                "submitted": submitted
            })
    else:
        form = CreateListing()  
        return render(request,"auctions/create.html", {
            "form": form,
        })


## Helper function to get the highest bidder. Returns a Bid object with highest amount bid on the item
## Access bidder id by "maxbid.first().bidder.id" // price by "maxbid.first().price"

def max_bidder(all_bids):
    bids = []
    for bid in all_bids:
        bids.append(bid.price)
    maxprice = max(bids)
    maxbid = all_bids.filter(price=maxprice)
    return maxbid       

## Helper function to list all categories of particular item passed in from listing_view function
def list_categories(listing):
    if listing:
        categories = []
        listing = listing.category.all()
        for category in listing:
            categories.append(category)
        return categories
    else:
        return None


def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    categories = list_categories(listing)
    bids = Bid.objects.filter(item__id=listing_id)
    bidcount = len(bids)        ## Check how many bidders so far on particular item
    bidarea = PlaceBid()
    
    ## If no bids , starting price in considered top price
    if not bids:
        maxprice = listing.price
        maxbidder = None
    else:
        maxprice_set = max_bidder(bids)
        maxbidder = maxprice_set.first().bidder
        maxprice = maxprice_set.first().price
    
    
    return render(request,"auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "maxprice": maxprice,
        "bidcount": bidcount,
        "maxbidder": maxbidder,
        "categories": categories,
        "bidarea": bidarea
    })