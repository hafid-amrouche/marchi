from django.contrib import auth


def get_cart(request, cart_id, cart):
  try :
    cart = cart.objects.get(id=cart_id)
  
  except :
    cart = cart.objects.create()
    request.session["cart_id"] = cart.id

  return cart

def narrow(objects, list):
  # this funtion is used in case you need to get one result where one of the fields is a ManyToManyField
  # and you need to get one result that has one specific list of instances of that field no more no less
  # filter the objects and store them in a variable and pass it to objects
  # create a list of all objects you want to use it to filter your result more and pass it to list
  # change "value" with the ManyToMany field containing the objects you want to use it to filter your result more
  single_object = None
  for object in objects:
    if object.value.count() != len(list):
      continue
    else :
      for value in object.value.all():
        if not (value in list):
          break
      else:
        single_object = object
  return single_object
  