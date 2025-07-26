from .models import Transaction
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm

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
def home_view(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = sum(t.amount for t in transactions if t.category == 'Income')
    total_expenses = sum(t.amount for t in transactions if t.category == 'Expense')
    net_balance = total_income - total_expenses

    return render(request, 'home.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
    })

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('home')  # after adding, go back to home page
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})