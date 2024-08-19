from django.shortcuts import render
from urllib import request
from django.views import View
from . models import Product
from django.db.models import Count
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages


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
        else:
            messages.warning(request, "Ofs! Please try again.")
        return render(request, "app/customerregistrationform.html", locals())

#profile view    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        return render(request, 'app/profile.html', locals())