from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=64)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="listings", blank=True, null=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watch_list")
    owner = models.ForeignKey(User, on_delete=CASCADE, related_name="listings")
    is_active = models.BooleanField()

    def __str__(self) -> str:
        return self.title

class Bid(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=CASCADE, related_name="bids")

class Comments(models.Model):
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="comments")
    creator = models.ForeignKey(User, on_delete=CASCADE, related_name="comments")
