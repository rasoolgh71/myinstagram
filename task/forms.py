from django import forms

class Logininsta(forms.Form):
    username = forms.CharField(max_length=60)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


#class Login_view(forms.Form):
 #   username = forms.CharField(max_length=60)
  #  password = forms.CharField(max_length=32, widget=forms.PasswordInput)