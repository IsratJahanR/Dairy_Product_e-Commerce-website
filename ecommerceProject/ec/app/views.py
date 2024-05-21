from django.db.models import Count
from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import Product,Cart,Customer,Wishlist,Payment,OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm, PasswordChangeForm,ProductForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'app/login1.html')

# def LogoutPage(request):
 #   logout(request)
 #   return redirect('login')


def home(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    products=Product.objects.all()
    return render(request, "app/home.html",locals())

def bkash(request):
    if request.method == 'GET':
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        totalamount=0
        for p in cart_items:
            totalamount +=p.quantity*p.product.discounted_price
        totalamount+=40
    return render(request, "app/bkash.html",locals())


def about(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())


def contact(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html",locals())

@login_required
def ChangePassword(request):
    return render(request, "app/changepassword.html")


class CategoryView(View):
    
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
    
        return render(request, "app/category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(
            category=product[0].category).values('title')
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
 
        return render(request, "app/category.html", locals())


class ProductDetails(View):
    def get(self, request, pk):

        product = Product.objects.get(pk=pk)

        if request.user.is_authenticated:
           wishlist =Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
 
        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, "app/customerregistration.html", locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Successfully")
        else:
            messages.warning(request, "Invalid Data")

        totalitem = 0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
   
        return render(request, 'app/customerregistration.html', locals())
    

def adminhome(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('adminhome')
    return render(request,'app/adminhome.html',{'productForm':productForm})


class MyPasswordChangeForm(PasswordChangeForm):
    pass
    # old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus':'True',#'autocomplete':'current-password','class':'form-control'}))
    # new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autofocus':'True',#'autocomplete':'current-password','class':'form-control'}))
    # new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autofocus':'True',#'autocomplete':'current-password','class':'form-control'}))


class MyPasswordResetForm(PasswordChangeForm):
    pass


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
   
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality,
                           mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Save Successfully")
        else:
            messages.warning(request, "Invalid Data")
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/address.html', locals())


class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))

        return render(request, 'app/updateaddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)

            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Update Successfully")
        else:
            messages.warning(request, "Invalid Data")
            totalitem = 0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
    
        return redirect("address")

def show_wishlist(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    user=request.user
    wishlist = Wishlist.objects.filter(user=user)
    return render(request, 'app/wishlist.html', locals())

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.filter(user=user,product=product)
            if cart:
                pass
            else :
                Cart(user=user, product=product).save()
            return redirect("/cart")
        return redirect("/cart")
    else:messages.warning(request, "Please Login or Register")



def show_cart(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount+=value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
       # print(prod_id)
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
       # print(prod_id)
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, "app/home.html",locals())

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user,product=product).save()
        
        data={
           'message': 'Added to Wishlist'
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        
        data={
           'message': 'Removed from Wishlist'
        }
        return JsonResponse(data)

    
def checkout(request): 
    if request.method == 'GET':
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        totalamount=0
        for p in cart_items:
            totalamount +=p.quantity*p.product.discounted_price
        totalamount+=40
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    products=Product.objects.all()
    return render(request,'app/checkout.html', locals())
    
def paymentdone(request):
     return render(request,'app/paymentdone.html', locals())  


### Admin Part:


def adminhome(request):
    return render(request, "app/adminhome.html")

def allproduct(request):
    products=Product.objects.all()
    return render(request,'app/allproduct.html',locals())

def allcustomer(request):
    products=Customer.objects.all()
    return render(request,'app/allcustomer.html',locals())

def addproduct_view(request):
   form = ProductForm
   if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
           
            print(form)
            
        else:
            messages.warning(request, "Invalid Data")
   else:
        form = ProductForm()
   context = {'form':form}
   return render(request,'app/addproduct.html',context)

def delete_product_view(request,pk):
    add = Product.objects.get(pk=pk)
    add.delete()
    return redirect("allproduct")

class update_product_view(View):
    def get(self, request, pk):
        add = Product.objects.get(pk=pk)
        form = ProductForm(instance=add)
        return render(request, 'app/updateaddress.html', locals())

    def post(self, request, pk):
        form = ProductForm(request.POST)
        if form.is_valid():
            add = Product.objects.get(pk=pk)
            add.title = form.cleaned_data['title']
            add.selling_price = form.cleaned_data['selling_price']
            add.discounted_price = form.cleaned_data['discounted_price']
            add.description = form.cleaned_data['description']
            add.composition = form.cleaned_data['composition']
            add.prodapp = form.cleaned_data['prodapp']
            add.category = form.cleaned_data['category']
            add.product_image = form.cleaned_data['product_image']
            add.save()
            messages.success(request, "Update Successfully")
        else:
            messages.warning(request, "Invalid Data")
    
        return redirect("allproduct")

def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))

        return render(request, 'app/updateaddress.html', locals())

def search_view(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    # whatever user write in search box we get in query
    query = request.GET['search']
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request,'app/search.html',locals())
 
