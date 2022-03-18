from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name='store'),
    path("<slug:category_slug>", views.category, name="category" ),
    path("<slug:category_slug>/<slug:slug>", views.ProductView.as_view(), name="product" ),
]

