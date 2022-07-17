from django import template

register = template.Library()

def range_dtl(value1, value2):
  return range(value1, value2)

register.filter('range', range_dtl)
