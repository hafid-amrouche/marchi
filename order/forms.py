from django import forms
from .models import Order

class OrderForm(forms.ModelForm):

  class Meta:
    model = Order
    # exclude = ["upadated_at", "created_at", "is_ordered", "ip", "status", "id"]
    fields = ["first_name", "last_name", "phone", "email", "address_line_1", "address_line_2", "country", "state", "city", "zip_code", "order_note"]
    labels ={
        "first_name" : "First Name*",
        "last_name" : "Last Name*",
        "email" : "Email*",
        "phone" : "Phone Number*",
        "address_line_1" : "Address Line 1*",
        "country" : "Country*",
        "state" : "State*",
        "city" : "City*",
        "zip_code" : "Zip Code*",
        "order_note" : "Any Comments ?",
    }

  def __init__(self, *args, **kwargs):
      super(OrderForm, self).__init__(*args, **kwargs)
      self.fields["first_name"].widget.attrs["class"] = "form-control"
      self.fields["last_name"].widget.attrs["class"] = "form-control"
      self.fields["email"].widget.attrs["class"] = "form-control"
      self.fields["phone"].widget.attrs["class"] = "form-control"
      self.fields["address_line_1"].widget.attrs["class"] = "form-control"
      self.fields["address_line_2"].widget.attrs["class"] = "form-control"
      self.fields["address_line_2"].required = False
      self.fields["country"].widget.attrs["class"] = "form-select"
      self.fields["city"].widget.attrs["class"] = "form-control"
      self.fields["state"].widget.attrs["class"] = "form-control"
      self.fields["zip_code"].widget.attrs["class"] = "form-control"
      self.fields["order_note"].widget.attrs["class"] = "form-control"
      self.fields["order_note"].widget.attrs["rows"] = 3
      
