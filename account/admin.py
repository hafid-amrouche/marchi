from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Account, Profile

# Register your models here.

class AccountAdmin(UserAdmin):
  list_display = ("email", "first_name", "last_name", "username", "last_login", "date_joined", "is_active")
  list_display_links = ("email", "first_name", "last_name")
  readonly_fields=["last_login", "date_joined"]
  ordering =('-date_joined',)

  # these 3 parameters must be set and it will make password hideen
  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()

class ProfileAdmin(admin.ModelAdmin):
  list_display = ["thumbnail", "full_name", "country", "state", "city", "zip_code" ]
  
  def thumbnail(self, object):
    try :
      picture_url = object.profile_picture.url
    except :
      picture_url = "/static/images/avatars/avatar2.jpg"

    return format_html(f'<img src="{picture_url}" width="30" style="border-radius:50%;margin-left:42px;">')
  
  thumbnail.short_description = "Profile Picture"
  

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
