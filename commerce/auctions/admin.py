from django.contrib import admin
from .models import User, Listing, Bid, Comment

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = "id", "username", "first_name", "last_name", "email","date_joined", "is_staff"

class ListingAdmin(admin.ModelAdmin):
    list_display = "id", "creator", "name", "price", "date_created"

class BidAdmin(admin.ModelAdmin):
    list_display = "user", "product", "price", "date_created"

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)