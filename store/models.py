from django.db import models
from django.shortcuts import reverse
from category.models import Category

# Create your models here.

class Product(models.Model):
  name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=200, unique=True)
  description = models.TextField(max_length=300, blank=True)
  price = models.FloatField()
  off_price = models.FloatField(default=0.0)
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