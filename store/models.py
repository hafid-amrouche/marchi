from distutils.command.upload import upload
from itertools import product
from queue import Empty
from django.db import models
from django.shortcuts import reverse
from category.models import Category

# Create your models here.

class Product(models.Model):
  name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=200, unique=True)
  description = models.TextField(max_length=300, blank=True)
  off_price = models.FloatField(default=0.0)
  price = models.FloatField(default=0.0)
  has_variant = models.BooleanField(default=False)
  stock = models.IntegerField()
  image = models.ImageField(upload_to='photos/products')
  is_available = models.BooleanField(default=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)
  

  def get_url(self):
    return reverse('product', args=[self.category.slug, self.slug])

  def out_of_stock(self):
    return self.stock <= 0

  def __str__(self):
    return self.name

  def price_from_variants(self):
    values = set()
    for variation in self.variations.all():
      values.add(variation.values.all()[0])
    price = Price.objects.filter(product=self)
    for price in price.all():
      if values == set(price.value.all()):
          price = price.total
          return price

class Variation(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variations", null=True)
  category = models.CharField(max_length=50)
  has_images = models.BooleanField(default=False)

  def __str__(self):
    return str(self.category)

class Value(models.Model):
  variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name="values")
  name = models.CharField(max_length=50)
  image = models.ImageField(upload_to="photos/values", null=True, blank=True)

  def __str__(self):
    return str(self.name)

class Price(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
  value = models.ManyToManyField(Value)
  total = models.FloatField()

  def __str__(self):
    return str(self.product) + " " + "$ " + str(self.total)