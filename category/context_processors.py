from multiprocessing import context
from .models import Category

def categories(request):
  # gives the ability to define and all templates have access to it
  categories = Category.objects.all()
  context = {"categories" : categories}
  return context
