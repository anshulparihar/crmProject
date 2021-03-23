from django.shortcuts import render,redirect

from django.http import HttpResponse

from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from .models import *

from .forms import *

from .filters import *

from .decorators import *
# Create your views here.

@unauthenticated_user
def registerPage(request):
    form  = CreateUserForm()
    if(request.method == "POST"):
        form = CreateUserForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name= 'customer')
            user.groups.add(group)
            Customer.objects.create(user=user,name = username,email = email,phone = '')

            messages.success(request,'Account has been created for '+ username)
            
            return redirect('login')
    context = {'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username,password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.info(request, 'Invalid Username or Password')
            # return render(request,'accounts/login.html',context)

    context = {}
    return render(request,'accounts/login.html',context)

def logoutPage(request):
    logout(request)
    context = {}
    return redirect('login')

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_order = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context = {'orders':orders, 'customers':customers,'total_order':total_order,'delivered':delivered, 'pending':pending, 'total_customers':total_customers}
    return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context = {'orders':orders,'total_order':total_order,'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def product(request):
    products = Product.objects.all()
    total_product = products.count()
    context = {'products':products,'total_product':total_product}
    return render(request, 'accounts/products.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):

    customer = Customer.objects.get(id=pk) 
    orders = customer.order_set.all()
    total_order = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)

    orders = myFilter.qs
    # print(myFilter)

    context = {'customer':customer,'orders':orders,'total_order':total_order,'myFilter':myFilter}
    return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form  = OrderForm()

    if(request.method == 'POST'):
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrderCustomer(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra = 5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset = Order.objects.none(),instance= customer)
    #form  = OrderForm(initial={'customer':customer})

    if(request.method == 'POST'):
        formset = OrderFormSet(request.POST,instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form':formset}
    return render(request, 'accounts/placeOrder.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance= order)
    if(request.method == 'POST'):
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    context = {'order':order}
    if(request.method == "POST"):
        order.delete()
        return redirect('/')
    return render(request,'accounts/deleteOrder.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):

    form = CustomerForm()

    if (request.method == "POST"):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/create_Customer.html',context)

##Create Update Customer
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if (request.method == "POST"):
            form = CustomerForm(request.POST,instance=customer)
            if form.is_valid():
                form.save()
                return redirect('/')
    context = {'form':form}
    return render(request,'accounts/create_Customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request,pk):
    customer = Customer.objects.get(id=pk)
    
    context = {'customer':customer}
    if(request.method == "POST"):
        customer.delete()
        return redirect('/')
    return render(request,'accounts/deleteCustomer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
    form = ProductForm(initial="")
    if (request.method == "POST"):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    context = {'form':form}
    return render(request,'accounts/product_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
# @admin_only
def updateProduct(request,pk):
    product = Product.objects.get(id = pk)
    form = ProductForm(instance=product)
    if (request.method == "POST"):
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    context = {'form':form}
    return render(request,'accounts/product_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request,pk):
    product = Product.objects.get(id = pk)
    context= {'product':product}
    if(request.method == "POST"):
        product.delete()
        return redirect('/products/')
    return render(request,'accounts/deleteProduct.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form  = userCustomerForm(instance=customer)
    if request.method == 'POST':
        form = userCustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    print(form)
    context = {'form':form}
    return render(request,'accounts/accountSettings.html',context)