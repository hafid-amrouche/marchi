from .models import Cart
from django.contrib import auth

def cart(request): # gives the ability to define dicts and all templates have access to it
  cart_items_quantity = 0
  if request.user.is_authenticated:
    user = auth.get_user(request)
    for item in user.cartitem_set.filter(is_active=True):
      cart_items_quantity += item.quantity
  else:
    try :
      cart_id = request.session.get('cart_id')
      cart = Cart.objects.get(id=cart_id)
      cart_items = cart.cartitem_set.filter(is_active=True)
      for item in cart_items:
        cart_items_quantity += item.quantity
        
    except Cart.DoesNotExist:
      pass
  context ={
    "cart_items_quantity" : cart_items_quantity
  }
  return context
