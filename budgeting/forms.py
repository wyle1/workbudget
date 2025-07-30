from django import forms
from .models import Meal
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction
from .models import WishItem

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'description']

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'calories', 'protein']

class WishForm(forms.ModelForm):
    class Meta:
        model = WishItem
        fields = ['name', 'cost']