from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 

# Create your models here.
# this whole app is to modify the admin panel

class MyAccountManager(BaseUserManager): #this class defines how users and superusers accounts are created
  def create_user(self, first_name, last_name, username, email, password=None):
    # a user is an account instance with some obligations and editing
    # this method uses the "Account class" to create users

    if not email:
      raise ValueError('An email is required')
    
    if not username:
      raise ValueError('A username is required')


    user = self.model( # creating a user with 4 fields
      email=self.normalize_email(email),
      username=username,
      first_name=first_name,
      last_name=last_name,
      
    )
 
    user.set_password(password) # setting the password sepatelly from the other fields
    
    # after creating a user we save it to the self._db
    user.save(using=self._db)
    return user

  def create_superuser(self, first_name, last_name, username, email, password):
    # a supper user is a user with a mendatory password and all 4 authorazations 
    # this defines obligated fiedls from the superuser to create an account
    super_user = self.create_user( # creating a user with 4 fields
      email = self.normalize_email(email),
      username=username,
      password=password,
      first_name=first_name,
      last_name=last_name,
    )

    super_user.is_admin = True
    super_user.is_staff = True
    super_user.is_superadmin = True
    super_user.is_active = True

    super_user.save(using=self._db)
    return super_user



class Account(AbstractBaseUser): #this class creates users
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=100, unique=True)
  phone_number = models.CharField(max_length=50, blank=True)

  #required
  date_joined= models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now_add=True)
  is_admin = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)

  # the field that you use to login is "email" insted of "username" other than "password"
  USERNAME_FIELD = 'email'
  # fields other than the 'email' and password that should apper to you when creating a superuser
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] 

  # the user manager class that will use this base user class
  objects = MyAccountManager()

  def __str__(self):
    return self.email
  
  def has_perm(self, perm, obj=None): # only an admin account has 'per' permissions 
    return self.is_admin

  def has_module_perms(self, add_label): # any account has 'addlabel' permissions
    return True