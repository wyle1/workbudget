from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.shortcuts import render
from .models import Transaction
from django.shortcuts import render
from .models import Transaction  # adjust to your model name
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # redirect after signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')

@login_required
def home(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)

    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expenses

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
    }
    return render(request, 'home.html', context)