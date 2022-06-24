from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, reverse
from cart.models import Cart
from functions import get_cart, narrow
from order.models import Order, Payment, OrderProduct
from order.forms import OrderForm
from store.models import Stock
from marchi.settings import EMAIL_HOST_USER
import datetime
import json

# Create your views here.

def place_order(request):
  # in this def an Order instance with is_ordered = False will be created
  # after you pay and it successed you will be POST requested to "payment"
  user = request.user
  if not user.is_authenticated :
    cart_id = request.session.get("cart_id", False)
    cart = get_cart(request, cart_id, Cart)
    cart_items = cart.cartitem_set.filter(is_active = True)
  else :
    cart_items = user.cartitem_set.filter(is_active = True)

  cart_count = cart_items.count()
  if cart_count <= 0:
    return redirect("store")

  if request.method == "POST":
    form = OrderForm(request.POST)
    untaxed_price = request.POST.get("untaxed_price")
    tax = request.POST.get("tax")
    tax_per = request.POST.get("tax_per")
    taxed_price = request.POST.get("taxed_price")
    if form.is_valid():
      year = int(datetime.date.today().strftime('%Y'))
      month = int(datetime.date.today().strftime('%m'))
      day = int(datetime.date.today().strftime('%d'))
      hour = int(datetime.datetime.now().strftime('%H'))
      minute = int(datetime.datetime.now().strftime('%M'))
      second = int(datetime.datetime.now().strftime('%S'))
      time_in_str = f"{second}.{minute}.{hour}.{day}.{month}.{year}"

      request.META.get("REMOTE_ADDR")
      order = Order()
      if user.is_authenticated:
        order.user = user
      order.first_name = form.cleaned_data["first_name"]
      order.last_name = form.cleaned_data["last_name"]
      order.email = form.cleaned_data["email"]
      order.phone = form.cleaned_data["phone"]
      order.address_line_1 = form.cleaned_data["address_line_1"]
      order.address_line_2 = form.cleaned_data["address_line_2"]
      order.country = form.cleaned_data["country"]
      order.state = form.cleaned_data["state"]
      order.city = form.cleaned_data["city"]
      order.zip_code = form.cleaned_data["zip_code"]
      order.order_note = form.cleaned_data["order_note"]
      order.order_total = float(taxed_price)
      order.tax = float(tax)
      order.ip = request.META.get("REMOTE_ADDR")
      order.save()
      order.order_number = time_in_str + str(order.ip)
      order.save()
      context = {
        'order' : order,
        'cart_items' : cart_items,
        'untaxed_price' : untaxed_price,
        'tax_per' : tax_per,
        'tax_total' : tax,
        'taxed_price' : taxed_price,

      }
      return render(request, 'order/payment.html', context)

    else:
      request.session["post_request"] = request.POST
      return redirect("checkout")

def payment(request):
  if request.method == "POST":
    body = json.loads(request.body)
    payment = Payment(
      ip_address = request.META.get('REMOTE_ADDR'),
      payment_id = body["transID"],
      payment_method = body["payment_method"],
      status = body["status"],
      amount_paid = body["amount"],
    )
    if request.user.is_authenticated:
      payment.user = request.user
    payment.save()

    order = Order.objects.get(order_number=body['orderID'], is_ordered=False)
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move cart items to OrderProduct Table 
    # Each product taht was bought must have an OrderProduct Instance 


    if request.user.is_authenticated :
      cart_items = request.user.cartitem_set.all()
    else :
      cart = get_cart(request, request.session.get("cart_id"), Cart)
      cart_items = cart.cartitem_set.all()
      
    for item in cart_items:
      item_price = item.price()
      order_product = OrderProduct(
          order=order,
          payment=payment,
          product=item.product,
          product_price=item_price,
          quantity = item.quantity,
          )
      order_product.save()

      if request.user.is_authenticated:
        order_product.user = request.user

      for value in item.value.all():
        order_product.value.add(value)
      order_product.save()

      # decrease the stock of the product 

      if item.product.has_variant :
        stocks = Stock.objects.filter(product=item.product)
        stock = narrow(stocks, item.value.all())
      else:     
        stock = Stock.objects.get(product=item.product)

      stock.total -= item.quantity
      stock.save()

    # empty the Cart

    # cart_items.delete()

    # send verification email

    to_email = body['email']
    first_name = body['first_name']
    mail_subject = "ORDER RECIEVED"
    message = render_to_string("order/order_recivied_message.html", {
      "first_name" : first_name,
      "order" : order
    })
    print(to_email, first_name)
    send_email = EmailMessage(subject=mail_subject, body=message, from_email=EMAIL_HOST_USER, to=[to_email])
    send_email.send()

    # send back TransID and OrderID back to sendData javascript function
      
    data = {
      "TransID" : payment.payment_id,
      "order_number" : order.order_number,
    }

    return JsonResponse(data)
       
      
  return render(request, 'order/payment.html')

def order_complete(request):
  order_number = request.GET["order_number"]
  payment_id = request.GET["payment_id"]
  try :
    payment = Payment.objects.get(payment_id = payment_id)
    order = Order.objects.get(order_number = order_number, is_ordered=True)
    ordered_products = OrderProduct.objects.filter(order = order, payment=payment)
    context = {
      "order_number" : order_number,
      "payment_id" : payment_id,
      "ordered_products" : ordered_products,
      "order" : order,
      "payment" : payment,
    }
    return render(request, "order/order_complete.html", context)
  
  except(Payment.DoesNotExist, Order.DoesNotExist) :
    return redirect('home')
    