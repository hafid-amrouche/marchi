from .models import Cart

def cart(request): # gives the ability to define dicts and all templates have access to it
  if 'admin' in request.path:
    return {}
  cart_items_quantity = 0
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
