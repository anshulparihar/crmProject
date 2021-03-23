from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm

from django import forms

from .models import *

from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        

class ProductForm(ModelForm):
    class Meta: 
        model = Product
        fields = "__all__"

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name']
        error_messages={
               'password2': 'Please enter your name'
                }

class userCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['user']