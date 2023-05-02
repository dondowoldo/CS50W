from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("closed", views.closed_view, name="closed"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.category_view, name="categories"),
    path("category/<str:category>", views.category_filter, name="category")
]
