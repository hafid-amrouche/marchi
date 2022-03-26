from msilib.schema import Error
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, reverse
from .models import Cart, CartItem
from store.models import Product, Variation, Value

# Create your views here.

def _get_cart_id(request, cart_id):
  try :
    cart = Cart.objects.get(id=cart_id)
  
  except :
    cart = Cart.objects.create()
    request.session["cart_id"] = cart.id
    cart_id = request.session["cart_id"] 

  cart = Cart.objects.get(id=cart_id)
  return Cart.objects.get(id=cart_id)

def add_to_cart(request, pri, pk): 
  if request.method == "POST" :
    product = Product.objects.get(pk=pk)
    cart_id = request.session.get("cart_id", False)
    cart = _get_cart_id(request, cart_id)

    variation = dict()
    for variant_key, variant_value in request.POST.items():
      if variant_key == 'csrfmiddlewaretoken':
        continue
      variation[variant_key] = variant_value
    values = set()
    for variant, value in variation.items() :
      values.add(Value.objects.get(name=value, variation = Variation.objects.get(category=variant, product=product)))
    
    cart_items = CartItem.objects.filter(cart=cart, product=product)
    if pri == "add": 
      # real_cart_item = _narrow(cart_item, values,)
      for cart_item in cart_items:
        if set(cart_item.value.all()) == values:
          cart_item.quantity += 1
          cart_item.save()
          return redirect(reverse('cart'))
      cart_item = CartItem.objects.create(cart=cart, product=product,quantity=1)
      cart_item.value.set(values)


    # print(cart_item.value.objects.all()[0].name)
    elif pri == 'minus' :
      for cart_item in cart_items:
        if set(cart_item.value.all()) == values: 
          cart_item.quantity -= 1
          cart_item.save() 
      
    elif pri == 'del' :
      for cart_item in cart_items:
        if set(cart_item.value.all()) == values: 
          cart_item.delete()

    return redirect(reverse('cart'))
  else:
    raise Http404


def cart(request):
  cart_id = request.session.get("cart_id")
  cart = Cart.objects.get(pk=cart_id)
  cart_items = cart.cartitem_set.filter(is_active=True)
  total_price = 0.0
  for item in cart_items :
    total_price += item.total()
  
  total_price = round(total_price, 2)
  tax = round(total_price * 0.02, 2)
  taxed_price = tax + total_price
  taxed_price = round(taxed_price, 2)
  tax = str(tax) + "(2%)"
  # for item in cart_items:
  #   for value in item.value.all():
  #     print(value.name)
  context = {
    'cart_items': cart_items,
    'total_price' : total_price,
    'tax' : tax,
    "taxed_price" : taxed_price,
  }
  return render(request, 'cart/cart.html', context)
