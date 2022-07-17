import shutil
from queue import Empty
from django.db import models
from django.shortcuts import reverse
from pkg_resources import require
from category.models import Category
from account.models import Account
from django.db.models import Avg

# Create your models here.

class Product(models.Model):
  name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=200, unique=True)
  description = models.TextField(max_length=300, blank=True)
  off_price = models.FloatField(default=0.0)
  price = models.FloatField(default=0.0)
  image = models.ImageField(upload_to='photos/products')
  is_available = models.BooleanField(default=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)
  

  def get_url(self):
    return reverse('product', args=[self.category.slug, self.slug])

  def stock(self):
    amount = 0
    for stock in self.stocks.all():
      amount += stock.total
    return amount

  def out_of_stock(self):
    return self.stock() <= 0

  def __str__(self):
    return self.name

  def price_from_variants(self):
    # returns the price that should be displayed on the product page
    values = set()
    for variation in self.variations.all():
      values.add(variation.values.all()[0])
    price = Price.objects.filter(product=self)
    for price in price.all():
      if values == set(price.value.all()):
          price = price.total
          return price

  def average_rating(self):
    ratings = ReviewRating.objects.filter(product=self, status=True)
    number_of_rates = ratings.count()
    avg = ratings.aggregate(Avg('rating'))
    if avg['rating__avg']:
      return round(float(avg['rating__avg']), 1)
    else:
      return 0.0
  
  def number_of_ratings(self):
    ratings = ReviewRating.objects.filter(product=self, status=True)
    return ratings.count()

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

class Stock(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
  value = models.ManyToManyField(Value, blank=True)
  total = models.IntegerField()

  def __str__(self):
    return str(self.product) + " " + str(self.total) + " unit"

class ReviewRating(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user = models.ForeignKey(Account, on_delete=models.CASCADE)
  subject = models.CharField(max_length=100, blank=True)
  review = models.TextField(max_length=500, blank=True)
  rating = models.IntegerField()
  ip = models.CharField(max_length=20, blank=True)
  status = models.BooleanField(default=True)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  def __str__(self):
    return self.subject

class Gallery(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  image = models.ImageField(upload_to = "stores/products/", max_length=255)

  class Meta:
    verbose_name_plural = "galleries"
  
  def __str__(self):
    return self.product.name
  