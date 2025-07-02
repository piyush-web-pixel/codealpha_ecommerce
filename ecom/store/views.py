from django.shortcuts import render,redirect, get_object_or_404
from . import models
from django.http import HttpResponse 
from django.http import JsonResponse
import time
from . import emailAPI
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Product, Order

import razorpay
from django.conf import settings





from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect
from django.conf import settings



# Create your views here.
def home(request):
    product =models.Product.objects.all()
    print(product)
    return render(request,'home.html',{"product":product})

def men(request):
    product =models.Product.objects.all()

    return render(request,'men.html',{"product":product})


def women(request):
    product =models.Product.objects.all()

    return render(request,'women.html',{"product":product})


# def checkout(request):
#     product =models.Product.objects.all()
#     return render(request,'checkout.html',{'product':product})

def detail(request,slug):
    product = models.Product.objects.get(slug=slug)  
    return render(request,'detail.html',{'product':product})



def address(request):
    return render(request,'address.html')

# def place_order(request):
#     if request.method == 'POST':
#         name = request.POST['full_name']
#         phone = request.POST['phone']
#         email = request.POST.get('email')
#         address = request.POST['address']
#         city = request.POST['city']
#         state = request.POST['state']
#         zip_code = request.POST['zip']
#         notes = request.POST.get('notes')

#         # Save to database or process order logic here...

#         return HttpResponse("Order placed successfully!")
#     return redirect('checkout')




def mobile(request):
    product =models.Product.objects.all()

    return render(request,'mobile.html',{"product":product})





def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            from .models import Product
            product = Product.objects.get(id=product_id)
            cart[str(product_id)] = {
                'name': product.pname,
                'price': float(product.prize),
                'quantity': 1,
                'image': product.image.url if product.image else ''
            }

        request.session['cart'] = cart
        return JsonResponse({'status': 'success', 'message': 'Product added to cart!'})
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'})

def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'cart.html', {'cart': cart, 'total': total})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')





def cart_count(request):
    cart = request.session.get('cart', {})
    return JsonResponse({'count': len(cart)})





def checkout(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    # product = models.Product.objects.get()
    order_amount = 50000  # in paise (₹500.00)
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'

    razorpay_order = client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
        'payment_capture': '1',
    })

    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': order_amount,
        'currency': order_currency,
        

    }
    return render(request, 'checkout.html', context)


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# @csrf_exempt
# def place_order(request):
#     # product = models.Product.objects.get()
#      if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         # now use product_id
#         product = get_object_or_404(Product, id=product_id)
#         Order.objects.create(user=request.user, product=product)
#         return redirect('order_list')  # Redirect to order list page
#      else :
#         return HttpResponseBadRequest("Invalid request method. Please use POST.")
            


@csrf_exempt
def place_order(request):
    # if request.method == 'POST':
    #     product_id = request.POST.get('product_id')
    #     if not product_id:
    #         return HttpResponseBadRequest("Missing product_id")

    #     product = get_object_or_404(Product, id=product_id)
    #     Order.objects.create(user=request.user, product=product)
    #     return redirect('order_list')
    # return HttpResponseBadRequest("Only POST requests are allowed")
    product=models.Product.objects.all()   
    return render(request,'order_success.html',{'product':product})
    # def place_order(request, product_id):
    # product = get_object_or_404(Product, id=product_id)
    # Order.objects.create(user=request.user, product=product)
    # return redirect('order_list')  # Redirect to order list page
    

    

def login(request):
    if request.method=="GET":
        return render(request,"login.html",{"output":""})
    else:
        #recieve data for login
        email=request.POST.get("email")
        password=request.POST.get("password")

        #to match user details in database
        userDetails=models.Register.objects.filter(email=email,password=password,status=1)

        if len(userDetails)>0:
            #to store user details in session
            request.session["sunm"]=userDetails[0].email
            request.session["srole"]=userDetails[0].role
            
            #print(userDetails[0].role) #to get user role
            if userDetails[0].role=="admin":
                return redirect("/myadmin/")
            else:
                return redirect("/userhome/")                
        else:
            return render(request,"login.html",{"output":"Invalid user or verify your account...."})                        


def register(request):
    if request.method=="GET":    
        return render(request,"register.html",{"output":""})
    else:
        #to recieve from data
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        #to insert record in database
        p=models.Register(name=name,email=email,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role="user",info=time.asctime())
        p.save()

        #to send mail using api
        emailAPI.sendMail(email,password)

        return render(request,"register.html",{"output":"User register successfully. Please verify your account using the link sent to your email.and then login...."})  




def verify(request):
    vemail=request.GET.get("vemail")
    models.Register.objects.filter(email=vemail).update(status=1)        
    return redirect("/login/")



def forget_p(request):
   return render(request, 'forget_p.html')

def about(request):
   return render(request, 'about.html')

def user_about(request):
   return render(request, 'user_about.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.contrib.auth.decorators import login_required

# @login_required
# def place_order(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     Order.objects.create(user=request.user, product=product)
#     return redirect('order_list')  # Redirect to order list page



@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
    return redirect('order_list')


def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'order_list.html', {'orders': orders})


def userhome(request):
    product =models.Product.objects.all()
    return render(request,"userhome.html",{'product':product})



def user_men(request):
    product =models.Product.objects.all()

    return render(request,'user_men.html',{"product":product})


def user_women(request):
    product =models.Product.objects.all()
    return render(request,'user_women.html',{"product":product})


def user_mobile(request):
    product =models.Product.objects.all()

    return render(request,'user_mobile.html',{"product":product})



# def profile_view(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'profile.html', {'orders': orders})


def profile(request):


    if "sunm" not in request.session:
        return redirect("/login/")

    # Get logged-in user's email from session
    email = request.session["sunm"]

    # Fetch the user data from the database
    profile = models.Register.objects.get(email=email)

    # Pass user data to the template
    return render(request, "profile.html", {"profile": profile})





def profile(request):
    if "sunm" not in request.session:
        return redirect("/login/")

    email = request.session["sunm"]
    profile = models.Register.objects.get(email=email)

    if request.method == "POST":
        # Update user fields from form data
        profile.name = request.POST.get("name")
        profile.password = request.POST.get("password")
        # Add more fields as needed
        profile.save()
        return render(request, "profile.html", {"profile": profile, "msg": "Profile updated successfully!"})
    
    return render(request, "profile.html", {"profile":profile})


   

def edit_profile(request):
    if "sunm" not in request.session:
        return redirect("/login/")

    email = request.session["sunm"]
    profile = models.Register.objects.get(email=email)

    if request.method == "POST":
        # Update user fields from form data
        profile.name = request.POST.get("name")
        # profile.password = request.POST.get("password")
        profile.mobile = request.POST.get("mobile")
        profile.address = request.POST.get("address")
        profile.city = request.POST.get("city")
        profile.gender = request.POST.get("gender")
        

        # Add more fields as needed
        profile.save()
        return render(request, "edit_profile.html", {"profile": profile, "msg": "Profile updated successfully!"})
    
    return render(request, "edit_profile.html", {"profile":profile})




def my_order(request):

    # profile=models.Register.objects.all()

    # orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_order.html')



def contact(request):
    if request.method=="GET":    
        return render(request,"contact.html",{"output":""})
    else:
        #to recieve from data
        name=request.POST.get("name")
        email=request.POST.get("email")

        mobile=request.POST.get("mobile")
        address=request.POST.get("address")


        #to insert record in database
        p=models.Contact(name=name,email=email,mobile=mobile,address=address,info=time.asctime())
        p.save()

        #to send mail using api


        return render(request,"contact.html",{"output":"your message send successfully...."})  
    






def manage_order(request):

    #to fetch user details
    userDetails=models.Product.objects.all()

    return render(request,"my_order.html",{"userDetails":userDetails,"sunm":request.session["sunm"]})



def remove_from_order(request, product_id):
    order = request.session.get('order', {})
    if str(product_id) in order:
        del order[str(product_id)]
        request.session['order'] = order
    return redirect('view_order')


def view_order(request):
    order = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in order.values())
    return render(request, 'my_order.html', {'order': order, 'total': total})


def manageuserstatus(request):
    #to get status data from url
    s=request.GET.get("s")
    product_id=int(request.GET.get("product_id"))

    if s=="active":
        models.Product.objects.filter(product_id=product_id).update(status=1)
    elif s=="inactive":
        models.Product.objects.filter(product_id=product_id).update(status=0)    
    else:
        models.Product.objects.filter(product_id=product_id).delete()

    return redirect("/manage_order/")

    # return render(request, 'profile.html')
# new addition today 

# def my_orders(request):
#     orders = Order.objects.filter(user=request.user).order_by("-created_at")
#     return render(request, "my_orders.html", {"orders": orders})

# def order_success(request):
#     return render(request, "order_success.html")



# # views.py
# @csrf_exempt
# def payment_success(request):
#     if request.method == "POST":
#         data = request.POST
#         razorpay_order_id = data.get("razorpay_order_id")
#         razorpay_payment_id = data.get("razorpay_payment_id")

#         # Update order
#         try:
#             order = Order.objects.get(razorpay_order_id=razorpay_order_id)
#             order.razorpay_payment_id = razorpay_payment_id
#             order.payment_status = "Paid"
#             order.save()
#             return redirect("order_success")
#         except Order.DoesNotExist:
#             return HttpResponse("Order not found", status=404)

#     return HttpResponse("Invalid request", status=400)



# # models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=255)
#     amount = models.FloatField()
#     razorpay_order_id = models.CharField(max_length=100)
#     razorpay_payment_id = models.CharField(max_length=100)
#     payment_status = models.CharField(max_length=20, default="Pending")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product_name} - {self.user.username}"

# # views.py
# import razorpay
# from django.conf import settings
# from .models import Order
# from django.views.decorators.csrf import csrf_exempt

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# def initiate_payment(request, product_id):
 
#     product = models.Product.objects.get(id=product_id)
#     amount = int(product.price * 100)

#     data = {
#         "amount": amount,
#         "currency": "INR",
#         "receipt": f"receipt_{product.id}",
#     }

#     razorpay_order = client.order.create(data=data)

#     # Save order in DB with "Pending" status
#     order = Order.objects.create(
#         user=request.user,
#         product_name=product.pname,
#         amount=amount / 100,
#         razorpay_order_id=razorpay_order["id"],
#         payment_status="Pending"
#     )

#     context = {
#         "order": order,
#         "product": product,
#         "razorpay_key": settings.RAZORPAY_KEY_ID,
#     }

#     return render(request, "checkout.html", context)








def cpuser(request):
    if request.method=="GET":
        return render(request,"cpuser.html",{"sunm":request.session["sunm"],"output":""})
    else:
        #to get data from form
        email=request.session["sunm"]
        opassword=request.POST.get("opassword")
        npassword=request.POST.get("npassword")
        cnpassword=request.POST.get("cnpassword")
        
        #to check old password is valid or not
        userDetails=models.Register.objects.filter(email=email,password=opassword)
        if len(userDetails)>0:
            if npassword==cnpassword:
                models.Register.objects.filter(email=email).update(password=cnpassword)
                return render(request,"cpuser.html",{"sunm":request.session["sunm"],"output":"Password changes successfully...."})    
            else:    
                return render(request,"cpuser.html",{"sunm":request.session["sunm"],"output":"New & Confirm new password mismatch...."})                
        else:
            return render(request,"cpuser.html",{"sunm":request.session["sunm"],"output":"Invalid old password , please try again...."})




def epuser(request):
    email=request.session["sunm"]
    userDetails=models.Register.objects.filter(email=email)

    m,f="",""
    if userDetails[0].gender=="male":
        m="checked"
    else:        
        f="checked"

    if request.method=="GET":
        return render(request,"epuser.html",{"sunm":email,"user":userDetails[0],"output":"","m":m,"f":f})
    else:
        #to get edited content
        name=request.POST.get("name")
        email=request.POST.get("email")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        #to update data in database
        models.Register.objects.filter(email=email).update(name=name,mobile=mobile,address=address,city=city,gender=gender)

        return redirect("/epuser/")


