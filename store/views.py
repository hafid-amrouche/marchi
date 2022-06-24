from django.shortcuts import render, get_object_or_404
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from .models import Product
from category.models import Category
from cart.models import Cart, CartItem

# Create your views here.



def _is_product_in_cart(request, product):
  cart_id = request.session.get("cart_id")
  product_in_cart = False
  try:
    cart = Cart.objects.get(pk=cart_id)
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items :
      if product == item.product:
        product_in_cart = True
        break
  except :
    pass
  return product_in_cart

def store(request):
  products = Product.objects.filter(is_available=True).order_by("-created_date")
  # Pagiator class stores the Product model and number of model instances to show
  # paginator.get_page(2) contains Product Model that should be showed in page 2
  # Now this Paginator also create a url_patterns for each page separatly
  # to see products of page(1) use either the path of this view or this path + "?page=1"
  # all other products are accessed by path = this path + "?page=page_number"
  # it also stores a key value pair in the request.GET of {"page", current_page}
  # and also has few methods like has_other_pages, has_previous, has_next
  
  paginator = Paginator(products, 2)
  page = request.GET.get("page")
  products_of_page = paginator.get_page(page)
  context = {
    "products_count" : products.count(),
    "products" : products_of_page
  }
  return render(request, 'store/store.html', context)

def category(request, category_slug):
  category = get_object_or_404(Category, slug=category_slug)
  #  products = Product.objects.filter(category__slug=category_slug, is_available=True)
  products = Product.objects.filter(category=category, is_available=True).order_by("-created_date")
  products_count = products.count()
  paginator = Paginator(products, 3)
  page = request.GET.get("page")
  products_of_page = paginator.get_page(page)
  context = {
     "products" : products_of_page,
     "products_count" : products_count
   }
  return render (request, 'store/store.html', context)

def product(request, category_slug, slug):
  product = Product.objects.get(slug=slug)
  product_in_cart = _is_product_in_cart(request, product)
  context = {
    "product": product,
    "product_in_cart" : product_in_cart,
  }
  return render(request, 'store/product.html', context)

def search(request):
  if request.GET.get("keyword") != None:
    request.session["keyword"] = request.GET.get("keyword") 
  keyword = request.session.get("keyword")
  if keyword :
    products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(slug=keyword)).order_by("-created_date")
    paginator = Paginator(products, 4)
    page = request.GET.get("page")
    products_of_page = paginator.get_page(page)
    context = {
      "products" : products_of_page ,
      "products_count" : products.count()
    }
  else:
    context = {
      "products_count" :0
    }
  return render(request, 'store/store.html', context)
