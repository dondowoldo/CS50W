from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="created")
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=300)
    imageurl = models.CharField(max_length=300, blank=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="bidder")
    product = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="item")
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} : {self.product.name} : {self.price} : {self.date_created}"

class Comment(models.Model):
    pass
