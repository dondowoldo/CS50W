from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    watchlist = models.ManyToManyField(User, blank=True, related_name="watching")
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="created")
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(max_length=155)
    imageurl = models.URLField(max_length=300, blank=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    category = models.ManyToManyField(Category, blank=True, related_name="category")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="bidder")
    item = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="item")
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    price = models.FloatField(blank=True)
    
    def __str__(self):
        return f"{self.bidder.username} : {self.item.name} : {self.price} : {self.date_created}"


class Comment(models.Model):
    comment = models.TextField(max_length=300, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user")
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="listing")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.comment
