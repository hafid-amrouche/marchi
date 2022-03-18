from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Product
from category.models import Category

# Create your views here.

def store(request):

  context = {
    "products" : Product.objects.filter(is_available=True)
  }
  return render(request, 'store/store.html', context)

def category(request, category_slug):
  #  products = Product.objects.filter(category__slug=category_slug, is_available=True)
  category = get_object_or_404(Category, slug=category_slug)
  products = Product.objects.filter(category=category, is_available=True)
  context = {
     "products" : products,
   }
  return render (request, 'store/store.html', context)

class ProductView(DetailView):
  template_name = 'store/product.html'
  model = Product
  context_object_name = 'product'

