from django import forms
from .models import Account

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