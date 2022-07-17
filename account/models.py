from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from PIL import Image
import os

# Create your models here.
# this whole app is to modify the admin panel

class MyAccountManager(BaseUserManager): #this class defines how users and superusers accounts are created
  def create_user(self, first_name, last_name, username, email , password=None):
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
  first_name = models.CharField(max_length=50,)
  last_name = models.CharField(max_length=50,)
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

  def full_name(self):
    return self.first_name.capitalize() + " " + self.last_name.capitalize()

  def __str__(self):
    return self.email
  
  def has_perm(self, perm, obj=None): # only an admin account has 'per' permissions 
    return self.is_admin

  def has_module_perms(self, add_label): # any account has 'addlabel' permissions
    return True


class Profile(models.Model):
  
  countries_list = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
  countries = []
  for country in countries_list:
    countries.append([country, country])
  user = models.OneToOneField(Account, on_delete=models.CASCADE)
  address_line_1 = models.CharField(max_length=100, null=True, blank=True)
  address_line_2 = models.CharField(max_length=100, null=True, blank=True)
  profile_picture = models.ImageField(blank=True, null=True, upload_to='userprofile/')
  country = models.CharField(max_length=50, choices=countries, null=True, blank=True)
  state = models.CharField(max_length=50, null=True, blank=True)
  city = models.CharField(max_length=50, null=True, blank=True)
  zip_code = models.CharField(max_length=10, null=True, blank=True)


  def __str__(self):
    return self.user.full_name()

  def full_name(self):
    return self.user.full_name()

  def full_address(self):
    return str(self.address_line_1).capitalize() + ", " + str(self.address_line_2)