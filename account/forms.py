from django import forms
from django.http import HttpRequest
from .models import Account, Profile 


class AccountForm(forms.ModelForm):
  attrs = {
    "placeholder" : "Enter a password"
  }
  confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))
  password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))

  class Meta:
    model = Account
    fields = ["first_name", "last_name", "email", "phone_number", "password",]

  def __init__(self, *args, **kwargs):
    super(AccountForm, self).__init__(*args, **kwargs)
    self.fields["first_name"].widget.attrs["placeholder"] = "Enter Your First Name"
    self.fields["last_name"].widget.attrs["placeholder"] = "Enter Your Last Name" 
    self.fields["email"].widget.attrs["placeholder"] = "Enter Your Email" 
    self.fields["phone_number"].widget.attrs["placeholder"] = "Enter Your Phone Number"  
    for field_key, field_value in self.fields.items():
      field_value.widget.attrs["class"] = "form-control"
      field_value.required = True
    
  def clean(self):
    cleaned_data = self.cleaned_data
    password = cleaned_data["password"]
    confirm_password = cleaned_data["confirm_password"]
    email = cleaned_data["email"]
    
    try:
      Account.objects.get(email = email)
      self.add_error("email", "This email is already used")
    except Account.DoesNotExist:
      pass
    if len(password) > 0 :
      if password != confirm_password :
        self.add_error("confirm_password", "")
        self.add_error("password", "Passwords do not match.")
    return cleaned_data

class UserForm(forms.ModelForm):
  class Meta:
    model = Account
    fields = ["first_name", "last_name", "phone_number", "email"]
  
  def __init__(self,  *args, **kwargs):
    super(UserForm, self).__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = "form-control"

    
class UserProfileForm(forms.ModelForm):   
  profile_picture = forms.ImageField(required=False, widget=forms.FileInput, error_messages={
    "invalid":("Image files only")
  })   

  class Meta:
    model = Profile
    fields = ["profile_picture", "address_line_1", "address_line_2", "country", "state", "city", "zip_code"]

  def __init__(self, *args, **kwargs):
    super(UserProfileForm, self).__init__(*args, **kwargs)
    for field in self.fields.values():
      field.required = False
      if field == self.fields["country"] :
        field.widget.attrs['class'] = "form-select"
        field.widget.attrs['aria-label'] = "Default select example"
        continue
      field.widget.attrs['class'] = "form-control"

