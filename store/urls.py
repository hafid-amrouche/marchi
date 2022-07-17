from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name='store'),
    path("search/", views.search, name="search"),
    path("<slug:category_slug>/", views.category, name="category" ),
    path("<slug:category_slug>/<slug:product_slug>/", views.product, name="product" ),
    path("submit-review/<int:product_id>", views.submit_review, name="submit_review"),
]

