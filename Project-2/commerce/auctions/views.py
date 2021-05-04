from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from decimal import Decimal
from django.db.models import Max
from django.contrib.auth.decorators import login_required


def index(request):
    # fetch all the active listings
    active_listings = Listing.objects.all().filter(is_active=True)

    # create list of tuples of all the listings
    listings = [(
        listing.id,
        listing.title,
        '{0:.2f}'.format(
            listing.bids.aggregate(
                Max('price'))['price__max'] if listing.bids.all() else listing.starting_bid),
        listing.description, listing.image_url)
        for listing in active_listings]

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


@login_required
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
def create_listing(request):
    if request.method == "POST":
        # fetch form data from request
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = Decimal(request.POST["starting_bid"])
        image_url = request.POST["image_url"]
        raw_category = request.POST["category"]

        # clean up category data
        if not raw_category:
            raw_category = "Uncategorized"
        category = Category.objects.filter(title=raw_category)
        if category.count() < 1:
            Category.objects.create(title=raw_category)
        category = Category.objects.get(title=raw_category)

        owner = User.objects.get(username=request.user.username)

        # create listing
        Listing.objects.create(
            title=title, description=description,
            starting_bid=starting_bid,
            image_url=image_url, category=category,
            owner=owner, is_active=True)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")


def listing(request, listing_id, msg=''):
    # stage data to send to listing page
    listing = Listing.objects.get(id=listing_id)
    comments = [(c.title, c.body, c.creator.username) for c in listing.comments.all()]

    return render(request, "auctions/listing.html", {
        "listing_id": listing_id,
        "title": listing.title,
        "price": '{0:.2f}'.format(
            listing.bids.aggregate(
                Max('price'))['price__max'] if listing.bids.all() else listing.starting_bid),
        "description": listing.description,
        "image_url": listing.image_url,
        "category": listing.category.title,
        "is_watched": listing.watchers.all().first() is not None and listing.watchers.get(username=request.user.username),
        "is_owner": listing.owner.username == request.user.username,
        "is_high_bidder": None if listing.bids.all().count() <= 0 else listing.bids.order_by('price').last().bidder.username == request.user.username,
        "bid_count": listing.bids.all().count(),
        "is_active": listing.is_active,
        "comments": comments,
        "owner_name": listing.owner.username,
        "message": msg
    })


@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        item = Listing.objects.get(id=listing_id)
        bidder = User.objects.get(username=request.user.username)
        bid_amount = Decimal(request.POST["bid_amount"]) if request.POST["bid_amount"] else item.starting_bid

        if item.bids.all().count() > 0:
            # there are bids, so check to see if new bid
            # is higher than existing bids
            if item.bids.order_by('price').last().price < bid_amount:
                Bid.objects.create(
                    price=bid_amount,
                    listing=item,
                    bidder=bidder)
            else:
                # new bid is too low
                return listing(request, listing_id, "Bid amount too low.")
        else:
            # no bids yet, ensure new bid is at least starting bid
            if bid_amount >= item.starting_bid:
                Bid.objects.create(
                    price=bid_amount,
                    listing=item,
                    bidder=bidder)
            else:
                return listing(request, listing_id, "Bid amount too low.")
    return listing(request, listing_id)


def categories(request):
    # fetch all categories
    cats = [c.title for c in Category.objects.all()]
    return render(request, "auctions/categories.html", {
        "categories": cats
    })


def category(request, category_title):
    # fetch category and build list of all items in category
    cat = Category.objects.get(title=category_title)
    listings = [(l.id, l.title) for l in cat.listings.all() if l.is_active]
    return render(request, "auctions/category.html", {
        "category": category_title,
        "listings": listings
    })


@login_required
def watchlist(request, username):
    # fetch user and build list of all items in watchlist
    user = User.objects.get(username=username)
    listings = [(l.id, l.title) for l in user.watch_list.all()]
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required
def submit_comment(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    creator = User.objects.get(username=request.user.username)
    if request.method == "POST":
        # create comment
        Comments.objects.create(
            title=request.POST["title"],
            body=request.POST["body"],
            listing=item,
            creator=creator)
    return listing(request, listing_id)


@login_required
def watch_item(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    watcher = User.objects.get(username=request.user.username)
    item.watchers.add(watcher)
    return watchlist(request, request.user.username)


@login_required
def stop_watching(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    watcher = User.objects.get(username=request.user.username)
    item.watchers.remove(watcher)
    return watchlist(request, request.user.username)
