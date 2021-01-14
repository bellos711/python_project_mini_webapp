from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *

def admin_login_view(request):
    if 'admin' in request.session:
        return redirect('adminhomepage')
    return render(request, "hamburgerapp/adminlogin.html")

def authenticateadmin(request):
    username=request.POST['username']
    password = request.POST['password']

    user = authenticate(
        username = username,
        password = password
    )

    #user exists
    if user is not None and user.username=="admin":
        login(request,user)
        request.session['admin'] = "admin"
        return redirect('adminhomepage')

    #user nonexistent
    if user is None:
        messages.add_message(request, messages.ERROR, "invalid credentials")
        return redirect('adminloginpage')

def adminhomepageview(request):
    if 'admin' not in request.session:
        return redirect('adminloginpage')
    context = {
        'hamburgers' : HamburgerModel.objects.all()
    }
    return render(request, "hamburgerapp/adminhomepage.html", context)

def logoutadmin(request):
    logout(request)
    request.session.flush()
    return redirect('adminloginpage')

def add_hamburger(request):
    #code to add hamburger order to db
    hamburger = HamburgerModel.objects.create(
        name = request.POST['hamburger'],
        price = request.POST['price'],
        # image = request.POST['image']
    )
    return redirect('adminhomepage')

def delete_hamburger(request, hamburger_id):
    this_hamburger = HamburgerModel.objects.get(id=hamburger_id)
    this_hamburger.delete()
    return redirect('adminhomepage')

def homepage_view(request):
    return render(request, 'hamburgerapp/homepage.html')

def register(request):
    print("Register function", request.POST)
    
    #read post data
    errors = User.objects.basic_validator(request.POST)
    #validate
    if len(errors) > 0:
        print("There are errors")
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        print("No errors")
        #hash pw
        hash_slinging_slasher = bcrypt.hashpw(
            request.POST['password'].encode(), 
            bcrypt.gensalt()
            ).decode()  # create the hash  
        print(f"our hash:  {hash_slinging_slasher}")
        #add user to database
        
        created_user = User.objects.create(
            username = request.POST['username'],
            phone = request.POST['phone'],
            #password = request.POST['password'] #VERY VERY BAD
            password = hash_slinging_slasher
        )
        print('*'*50)
        print("Our newly registered user pass: ", created_user.password)
        print(f"my newly created user's's id is {created_user.id}")
        #set us up in session
        request.session['uuid'] = created_user.id
        return redirect('/') #WATCH OUT FOR THIS REDIRECT

def logout_user(request):
    request.session.flush()
    return redirect('/')

def user_login_view(request):
    if 'uuid' in request.session:
        return redirect('/customer/main/')
    return render(request, "hamburgerapp/userlogin.html")

def login_user(request):
    print(f"our post data is {request.POST}")
    #check password through validator
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        print("There are errors")
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/userlogin/')
    
    else:
        #check email in db
        user_list = User.objects.filter(username=request.POST['username'])
        #setup user in session
        request.session['uuid'] = user_list[0].id
        # never render on a post, always redirect!
        print(f"{user_list[0].username} has logged in")
        return redirect('/customer/main/')

def customer_page(request):
    if 'uuid' not in request.session:
        return redirect('/userlogin/')
    this_user = User.objects.get(id=request.session['uuid'])
    context = {
        'this_user' : this_user,
        'hamburgers' : HamburgerModel.objects.all()
    }
    return render(request, 'hamburgerapp/customermain.html', context)

def place_order(request):
    this_customer = User.objects.get(id=request.session['uuid'])
    user_customer = this_customer
    address = request.POST['address']
    ordered_items = ""
    for hamburger in HamburgerModel.objects.all():
        hamburgerid = hamburger.id
        hamburgername = hamburger.name
        hamburgerprice = hamburger.price
        
        quantity = request.POST.get(str(hamburgerid)," ")
        if quantity !="0" and quantity!=" ":
            # multiplied_quantity = str(float(quantity)*float(hamburgerprice))
            ordered_items = ordered_items + hamburgername + " " + hamburgerprice + ", quantity: " + quantity + ", Total Price:" + str(float(quantity)*float(hamburgerprice)) + "    \n"
    
    this_order = Order(
        user_customer = user_customer,
        address = address,
        ordered_items = ordered_items
    ).save()
    messages.add_message(request,messages.SUCCESS, "Order placed successfully")
    return redirect('/customer/main/')

def customer_orders(request):
    print("in customer_orders")
    this_customer = User.objects.get(id=request.session['uuid'])
    all_ordered_items = this_customer.customer_orders.all()
    context = {
        'this_customer' : this_customer,
        'this_customer_phone' : this_customer.phone,
        'all_customer_orders' : all_ordered_items
    }
    return render(request, "hamburgerapp/customerorders.html", context)

def admin_orders(request):
    orders = Order.objects.all()
    context = {
        'orders' : orders
    }
    return render(request, 'hamburgerapp/adminorders.html', context)

def accept_order(request, order_id):
    this_order = Order.objects.get(id=order_id)
    this_order.status = "Accepted"
    this_order.save()
    return redirect('/adminorders')

def decline_order(request, order_id):
    this_order = Order.objects.get(id=order_id)
    this_order.status = "Declined"
    this_order.save()
    return redirect('/adminorders')