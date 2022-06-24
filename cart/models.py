from django.db import models
from store.models import Product, Value, Price
from account.models import Account
from functions import narrow
# Create your models here.

class Cart(models.Model):
  cart_id = models.CharField(max_length=2500, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.id)

class CartItem(models.Model):
  user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
  quantity = models.IntegerField()
  value = models.ManyToManyField(Value, blank=True)
  is_active = models.BooleanField(default=True)
    
  def total(self):
    item_price = self.price()
    return round(float(self.quantity) * item_price, 2)

  def __str__(self):
    return str(self.product)

  def price(self):
    if self.product.has_variant :
      values = []
      for value in self.value.all():
        values.append(value)
      price = Price.objects.filter(product=self.product) 
      price = narrow(price, values)
      price = price.total
    else :
      price = self.product.price
    return price