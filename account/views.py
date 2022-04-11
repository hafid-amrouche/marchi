from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .forms import AccountForm
from .models import Account
from marchi.settings import EMAIL_HOST_USER
import random
# Create your views here.


def accounts(request):
  user = auth.get_user(request)
  user_exist = False
  try:
    Account.objects.get(email = user)
    user_exist = True
  except Account.DoesNotExist:
    pass
  if user_exist:
    return redirect(reverse('dashboard'))
  else:
    return redirect(reverse('home'))


def register(request):
  user = auth.get_user(request)
  user_exist = False
  try:
    Account.objects.get(email = user)
    user_exist = True
  except Account.DoesNotExist:
    pass
  if not user_exist:
    if request.method == "GET":
      form = AccountForm()
    
    elif request.method == "POST":
      form = AccountForm(request.POST)
      if form.is_valid():
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        username = form.cleaned_data["email"].split("@")[0] + form.cleaned_data["email"].split("@")[1][0] + str(random.randint(0, 1000))
        user = Account.objects.create_user(
          first_name = first_name,
          last_name = last_name,
          email = email,
          password = password,
          username = username,
        )
        user.phone_number = form.cleaned_data["phone_number"]
        user.save()
        
        # activation link 
        current_site = get_current_site(request)
        mail_subjet = 'Please activate your account'
        message = render_to_string('account/account_verification_email.html', {
          'user' : user,
          'domain' : current_site,
          'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
          'token' : default_token_generator.make_token(user)
        })
        to_email = email
        send_email = EmailMessage(subject=mail_subjet, body=message, from_email=EMAIL_HOST_USER, to=[to_email])
        send_email.send()
        ##
        messages.success(request, "Your account is created. Check your email to activate it")
        return redirect(str(reverse('log-in') + '?command=verification&email=' + to_email))
    context = {
        "form" : form
      }
    return render(request, "account/register.html", context)
  else:
    return redirect(reverse('home'))


def log_in(request):
  user = auth.get_user(request)
  user_exist = False
  try:
    Account.objects.get(email = user)
    user_exist = True
  except Account.DoesNotExist:
    pass
  if not user_exist:
    if request.method=="POST":
      email = request.POST.get("email")
      password = request.POST.get("password")
      line = ""
      user = auth.authenticate(email=email, password=password)
      if user:
        auth.login(request, user)
        messages.success(request, 'You are logged in.')
        return redirect(reverse('dashboard'))
      else:
        try:
          account = Account.objects.get(email=email)
          line = "Either your password is wrong or you didn't activate your account."
          messages.error(request, line)
          return redirect(reverse('log-in'))
        except Account.DoesNotExist:
          line = "Wrong credentials."
          messages.error(request, line)
          return redirect(reverse('log-in'))
    return render(request, "account/log_in.html")
  else:
    return redirect(reverse('home'))

@login_required(login_url = 'log-in')
def log_out(request):
  auth.logout(request)
  messages.success(request, "You are logged out.")
  return redirect(reverse('log-in'))

@login_required(login_url = 'log-in')
def dashboard(request):
  return render(request, 'account/dashboard.html')

def activate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = Account._default_manager.get(pk=uid)

  except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user = None

  if user and default_token_generator.check_token(user, token):
    user.is_active = True
    user.save()
    messages.success(request, 'Your account is active ' + user.first_name.capitalize())
    return redirect(reverse('log-in'))
  else:
    messages.error(request, 'Invalid activation link')
    return redirect(reverse('register'))
  

def forgot_password(request):
  if request.method == "POST":
    email = request.POST.get('email').lower()
    if Account.objects.filter(email=email).exists():
      user = Account.objects.get(email__exact=email)
      current_site = get_current_site(request)
      mail_subjet = 'Reset Password'
      message = render_to_string('account/reset_password_validation_email.html', {
        'user' : user,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user)
      })
      to_email = email
      email_message = EmailMessage(subject=mail_subjet, body=message, from_email=EMAIL_HOST_USER, to=[to_email])
      email_message.send()
      messages.success(request, f'A link is sent to {email} to reset your password')
    else:
      messages.error(request, 'Account does not exist')
    return redirect(reverse('log-in'))
  return render(request, 'account/forgot_password.html')

def reset_password_validation(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = Account._default_manager.get(pk=uid)

  except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user = None

  if user and default_token_generator.check_token(user, token):
    request.session["uid"] = uid
    return redirect(reverse('reset_password'))
  else:
    messages.error(request, 'This link has been expired')
    return redirect(reverse('log-in'))

def reset_password(request):
  uid = request.session.get("uid")
  if request.method == "GET":
    if not uid:
      messages.error(request, 'Error')
      return redirect(reverse('log-in'))
    return render(request, 'account/reset_password.html')
  
  elif request.method == "POST":
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")
    if password == "" :
      messages.error(request, "Password can not be empty")
      return redirect(reverse('reset_password'))
    
    elif password != confirm_password: 
      messages.error(request, "Passwords must match")
      return redirect(reverse('reset_password'))
    
    elif password == confirm_password:
      user = Account._default_manager.get(pk=uid)
      user.set_password(password)
      user.save()
      uid = request.session.get("uid")
      messages.success(request, "password has been updated successfully")
      return redirect(reverse("log-in"))