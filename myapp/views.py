from django.shortcuts import render, redirect
from urllib import request
from django.views import View
from . models import Product, Customer, Cart
from django.db.models import Count
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q


def logout_view(request):
    logout(request)
    return redirect('login')

# Create your views here.
def home(request):
    return render(request, "app/home.html")
def about(request):
    return render(request, "app/about.html")
def contact(request):
    return render(request, "app/contact.html")
#Category page for showing different types of product according to their category
class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())
    
#for category title
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())

#for showing product details
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())
    
#User Registration
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistrationform.html", locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registration Complete.")
            return redirect('login')
        else:
            messages.warning(request, "Ofs! Please try again.")
        return render(request, "app/customerregistrationform.html", locals())
#
#profile view    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            division = form.cleaned_data['division']
            zipcode = form.cleaned_data['zipcode']
            reg=Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, division=division, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile is created.")
        else:
            messages.warning(request, "Ofs! Invalid Input Data.")
        return render(request, 'app/profile.html', locals())
    
#address view
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

#update address
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.division = form.cleaned_data['division']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile data is Updated successfully.")
        else:
            messages.warning(request, "ofs! Invalid Input data.")
        return redirect('address')
    
#add to cart view
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for i in cart:
        value = i.quantity * i.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', locals())

#Quantity increment decrement using Ajax
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for i in cart:
            value = i.quantity * i.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for i in cart:
            value = i.quantity * i.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for i in cart:
            value = i.quantity * i.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)