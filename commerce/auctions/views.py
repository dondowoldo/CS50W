from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListing, PlaceBid, PostComment, SelectCategory
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Bid, Category, Comment


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

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():            
            complete_form = form.save(commit=False)       ## saves form but doesnt commit to db. Allows us to populate creator field with currently logged in
            complete_form.creator = request.user
            complete_form.save()
            messages.success(request, "Listing successfully created!")
            return HttpResponseRedirect(reverse("listing", args=[complete_form.id]))
        else:
            messages.error(request, "An error has occured.")
            return render(request, "auctions/create.html",{
                "form": form
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
    comments = Comment.objects.filter(listing=listing).order_by("-timestamp")
    bids = Bid.objects.filter(item__id=listing_id)
    bidcount = len(bids)        ## Check how many bidders so far on particular item

    ## If no bids , starting price in considered top price
    if not bids:
        maxprice = None
        maxbidder = None
    else:
        maxprice_set = max_bidder(bids)
        maxbidder = maxprice_set.first().bidder
        maxprice = maxprice_set.first().price
    
    if request.method=="POST":
        if request.POST.get("place_bid"):
            offer = PlaceBid(maxprice, listing, request.POST)
            if offer.is_valid():
                completebid = offer.save(commit=False)
                completebid.bidder = request.user
                completebid.item = listing
                completebid.save()
                messages.success(request, ("Your bid for " + listing.name + " was successful."))
                return HttpResponseRedirect(reverse("listing", args=[listing.id]))
            else:
                messages.error(request, ("Your bid was unsuccessful."))
                return render(request, "auctions/listing.html", {
                    "comment_form": PostComment(),
                    "comments": comments,
                    "offer": offer,
                    "listing": listing,
                    "bids": bids,
                    "maxprice": maxprice,
                    "bidcount": bidcount,
                    "maxbidder": maxbidder,
                    "categories": categories
                    })
        if request.POST.get("sub_comment"):
            comment = PostComment(request.POST)
            if comment.is_valid():
                completecomment = comment.save(commit=False)
                completecomment.user = request.user
                completecomment.listing = listing
                completecomment.save()
                return HttpResponseRedirect(reverse("listing", args=[listing.id]))
            else:
                return render(request, "auctions/listing.html", {
                    "comment_form": PostComment(request.POST),
                    "comments": comments,
                    "offer": offer,
                    "listing": listing,
                    "bids": bids,
                    "maxprice": maxprice,
                    "bidcount": bidcount,
                    "maxbidder": maxbidder,
                    "categories": categories,
                    })

        if request.POST.get("close_bid"):
            listing.active = False
            listing.save()
            messages.info(request, ("Your auction for " + listing.name + " has been closed."))
            return HttpResponseRedirect(reverse("index"))
        
        if request.POST.get("watch_item"):
            listing.watchlist.add(request.user)
            messages.info(request, (listing.name + " has been added to your Watchlist."))
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))
        
        if request.POST.get("unwatch_item"):
            listing.watchlist.remove(request.user)
            messages.warning(request, (listing.name + " has been removed from your Watchlist."))
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))
    else:
        return render(request, "auctions/listing.html", {
            "comment_form": PostComment(),
            "offer": PlaceBid(maxprice, listing),
            "comments": comments,
            "listing": listing,
            "bids": bids,
            "maxprice": maxprice,
            "bidcount": bidcount,
            "maxbidder": maxbidder,
            "categories": categories,
            })
        
def closed_view(request):
    closed_listings = Listing.objects.filter(active=False)
    return render(request, "auctions/closed.html", {
        "closed_listings": closed_listings
    })

def watchlist(request):
    watchlist = Listing.objects.filter(watchlist__id = request.user.id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def category_view(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
        })

def category_filter(request,category):
    filtered_listings = Listing.objects.filter(category__name=category)

    return render(request, "auctions/category.html", {
        "filtered_listings": filtered_listings,
        "category": category
        })
