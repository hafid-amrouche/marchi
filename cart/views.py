from django.contrib import auth
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, reverse
from .models import Cart, CartItem
from store.models import Product, Variation, Value
from order.forms import OrderForm
from functions import get_cart
# Create your views here.



def add_to_cart(request, pri, pk): 
  if request.method == "POST" :
    product = Product.objects.get(pk=pk)
    variation = dict()
    for variant_key, variant_value in request.POST.items():
      if variant_key == 'csrfmiddlewaretoken':
        continue
      variation[variant_key] = variant_value
    values = set()
    for variant, value in variation.items() :
      values.add(Value.objects.get(name=value, variation = Variation.objects.get(category=variant, product=product)))

    
    if request.user.is_authenticated :
      user = auth.get_user(request)
      cart_items = CartItem.objects.filter(user=user, product=product)
    else:
      cart_id = request.session.get("cart_id", False)
      cart = get_cart(request, cart_id, Cart)
      cart_items = CartItem.objects.filter(cart=cart, product=product)

    if pri == "add": 
      # real_cart_item = narrow(cart_item, values,)
      for cart_item in cart_items:
        if set(cart_item.value.all()) == values:
          cart_item.quantity += 1
          cart_item.save()
          return redirect(reverse('cart'))
      if request.user.is_authenticated:
        cart_item = CartItem.objects.create(user=user, product=product,quantity=1)
      else:
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


def cart_and_checkout(request):
  # responsible of showing informations about the cart items
  # if it's the cart page it will create a Cart instance redirect you the checkout page
  # if you are in the checkout page fill the form and it will POST request you to the place oreder page

  user_exists = request.user.is_authenticated
  if not user_exists:
    cart_id = request.session.get("cart_id")
    if not cart_id:
      cart = Cart.objects.create()
      cart_id = cart.id
      request.session["cart_id"] = cart_id
    try :
      cart = Cart.objects.get(pk=cart_id)
    except Cart.DoesNotExist:
      cart = Cart.objects.create()
      request.session["cart_id"] = cart.id
      cart_id = cart.id
    cart_items = cart.cartitem_set.filter(is_active=True)
  else:
    user = auth.get_user(request)
    cart_items = user.cartitem_set.filter(is_active=True)
  untaxed_price= 0.0
  for item in cart_items :
    untaxed_price += item.total()
  
  untaxed_price = round(untaxed_price, 2)
  tax_per = 0.02
  tax_total = round(untaxed_price * tax_per, 2)
  taxed_price = round(tax_total + untaxed_price, 2)
  # for item in cart_items:
  #   for value in item.value.all():
  #     print(value.name)
  context = {
    'cart_items': cart_items,
    'untaxed_price' : untaxed_price,
    'tax_total' : tax_total,
    'tax_per' : tax_per,
    "taxed_price" : taxed_price,
  }
  if request.path == reverse('cart'):
    return render(request, 'cart/cart.html', context)
  elif request.path == reverse('checkout'):
    post_request = request.session.get("post_request")
    if post_request:
      context['form'] = OrderForm(post_request)
      request.session.pop("post_request")
    else:
      context['form'] = OrderForm()
    return render(request, 'cart/checkout.html', context)