from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

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


admin.site.register(Account, AccountAdmin)
# admin.site.register(ProfilePicture)
