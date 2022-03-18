from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(max_length=50, unique=True)
  image = models.ImageField(upload_to='photos/category', null=True)
  discription = models.TextField(max_length=255, null=True, blank=True)
  
  class Meta:
    verbose_name_plural = "categories"
    
  def get_url(self):
    return reverse('category', args=[self.slug])

  def __str__(self):
    return self.name