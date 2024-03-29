from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path('', views.index, name="index"),
    path('wiki/<str:title>', views.content, name="title"),
    path('search/', views.search, name="search"),
    path('create/', views.create, name="create"),
    path('wiki/<str:title>/edit/', views.edit, name="edit"),
    path('random/', views.randomPage, name="random")
]
