from django.db import models
from store.models import Product, Value, Price

# Create your models here.

def _narrow(objects, list):
  single_object = None
  for object in objects :
        if object.value.count() != len(list):
          continue
        else :
          for value in object.value.all():
            if not (value in list):
              break
            single_object= object
            return single_object


class Cart(models.Model):
  cart_id = models.CharField(max_length=2500, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.id)

class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  value = models.ManyToManyField(Value, blank=True)
  is_active = models.BooleanField(default=True)

  def item_price(self):
    values = []
    for value in self.value.all():
      values.append(value)
    price = Price.objects.filter(product=self.product) 
    price = _narrow(price, values)
    price = price.total
    
    return price
    
  def total(self):
    return round(float(self.quantity) * self.item_price(), 2)

  def __str__(self):
    return str(self.product)