from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Customer
from django import forms
from django.shortcuts import get_object_or_404, redirect


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'customers/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('customer_entry')
    else:
        form = AuthenticationForm()
    return render(request, 'customers/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def customer_entry(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_entry')
    else:
        form = CustomerForm()
    customers = Customer.objects.all()
    return render(request, 'customers/customer_entry.html', {'form': form, 'customers': customers})

def delete_customer(request, pk):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
    return redirect('customer_entry')