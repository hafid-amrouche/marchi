from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name='store'),
    path("search/", views.search, name="search"),
    path("<slug:category_slug>/", views.category, name="category" ),
    path("<slug:category_slug>/<slug:slug>/", views.product, name="product" ),
]

