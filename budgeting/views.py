from .models import Transaction
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.shortcuts import render
from .models import Meal
from .forms import MealForm
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction, WorkEntry, WishItem
from .forms import WishForm
from django.db.models import Sum
from decimal import Decimal

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

@login_required
def home_view(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = transactions.filter(category='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(category='Expense').aggregate(Sum('amount'))['amount__sum'] or 0

    net_budget = total_income - total_expenses  # 👈 Use only this



    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_budget': net_budget,  # 👈 Use for both logic and display
    }

    return render(request, 'home.html', context)

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

@login_required
def meals_view(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect('meals')  # redirect to clear the form
    else:
        form = MealForm()

    meals = Meal.objects.filter(user=request.user).order_by('-date')
    total_calories = sum(meal.calories for meal in meals)
    total_protein = sum(meal.protein for meal in meals)

    return render(request, 'meals.html', {
        'form': form,
        'meals': meals,
        'total_calories': total_calories,
        'total_protein': total_protein
    })

@login_required
def wish_list_view(request):
    wish_list = WishItem.objects.filter(user=request.user)
    form = WishForm(request.POST or None)

    # Get budget summary from transactions
    transactions = Transaction.objects.filter(user=request.user)
    total_income = transactions.filter(category='Income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_expenses = transactions.filter(category='Expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    net_budget = total_income - total_expenses
    eighty_percent_budget = net_budget * Decimal('0.8')
  

    # Handle form submission
    if request.method == 'POST' and form.is_valid():
        wish = form.save(commit=False)
        wish.user = request.user
        wish.save()
        return redirect('wish_list')

    context = {
        'wish_list': wish_list,
        'form': form,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_budget': net_budget,
        'eighty_percent_budget': eighty_percent_budget,
    }
    return render(request, 'wish_list.html', context)