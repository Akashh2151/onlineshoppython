from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
import urllib
import urllib.request
import urllib.parse
import json
from django.conf import settings

from mainapp.models import Category, Product, Cart, OrdersItems, Orders

from mainapp.forms import CategoryForm






def about(request):
    return render(request,"about.html")

def contactus(request):
    return render(request,"contactus.html")

def customer(request):
    return render(request,"customer.html")

def index(request,id=0):
    if id==0:
        prods=Product.objects.all()
    else:
        prods = Product.objects.filter(ProductCategory=id)
    return render(request,"index.html",{"cats":Category.objects.all(),"prods":prods})

def login2(request):
    if "next" in request.GET:
        request.session["next"]=request.GET["next"]
    if request.method=="POST":
        tp=request.POST["type"];
        if tp=="signup":
            #print(request.POST)
            name = request.POST["name"];
            email = request.POST["email"];
            mobile = request.POST["mobile"];
            pass1 = request.POST["pass"];
            secq = request.POST["secq"];
            seca = request.POST["seca"];
            resp = request.POST["g-recaptcha-response"];

            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': resp
            }
            data = urllib.parse.urlencode(values).encode() # replace space with +
            req = urllib.request.Request(url, data=data) # Creates Request class object
            response = urllib.request.urlopen(req) # send request to URL with Data and get response
            # Response comes in form of JSON [JavaScript Object Notation]
            # { "success":true,"key":"value,....}
            result = json.loads(response.read().decode())
            # json.loads ==> reads JSON Data in Response and convert into dictionary

            if result['success']:
                user=User.objects.create_user(email,email,pass1) # (username,emailid,password)
                user.profile.mobile=mobile
                user.profile.secq = secq
                user.profile.seca=seca
                user.save()

                subject = 'welcome to Online Shop'
                message = f'Hi {user.username}, thank you for registering in Online Shop.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                #send_mail(subject, message, email_from, recipient_list)

                messages.info(request,"You have been registered successfully. Now you can login")
            else:
                messages.info(request, "Invalid captcha")
        elif tp == "login":
            user1 = request.POST["user"]
            pass1 = request.POST["pass2"]
            print(request.POST)
            user=authenticate(request,username=user1,password=pass1)
            print(user)
            if user is not None:
                login(request, user)
                if user.is_superuser==1:
                    return redirect("/admin2")
                else:
                    if request.session.get("next","")!="":
                        rp=request.session.get("next","")
                        request.session.pop("next")
                        return redirect(rp)
                    else:
                        return redirect("/index")
            else:
                messages.info(request, "Login Failed.. try again")

        return redirect("/login2")


    return render(request,"login.html")

def check_email(request):
    flag="false"
    #if function is called via JS/jQuery. such request is called as AjAX Request
    if request.is_ajax():
        email=request.GET["email"]
        try:
            User.objects.get_by_natural_key(email) # Get User class object based on UserName
        except User.DoesNotExist:
            flag="true"

    return HttpResponse(flag)

def customer(request):
    return render(request,"customer.html")

def logout2(request):
    logout(request)
    return redirect("/login2")

def changepass(request):
    if request.method=="POST":
        pass1=request.POST["pass1"]
        pass2 = request.POST["pass2"]
        user=request.user
        if user.check_password(pass1):
            user.set_password(pass2)
            user.save()
            update_session_auth_hash(request,user)
            #Django maintains unique hash value for each user
            #Hash value is derived from User info [username,password,....]
            messages.info(request, "Your Password Changed Successfully")
            return redirect("/changepass")
        else:
            messages.info(request, "Wrong Old Password Try again...")
            return redirect("/changepass")
    else:
        return render(request,"change_pass.html")

def admin2(request):
    return render(request,"admin.html")


# Category related views
def prodcat(request):
    form = CategoryForm()
    data = {"cats": "","msg":"","form":form,"btntext":"Save"}
    if request.method=="POST":
        btntext = request.POST["btn"]
        print(btntext)
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            if btntext=="Save":
                form.save()
                data["msg"]="Category Record is Saved"
            else:
                print(form)
                cid=request.session.get("cid",0)
                print(cid)
                cat=Category.objects.filter(id=cid)[0]
                cat.CategoryName=form.cleaned_data["CategoryName"]
                cat.CategoryImage = form.cleaned_data["CategoryImage"]
                cat.save() # if record is exists then update it
                data["msg"] = "Category Record is Updated"
            data["form"]=form

    cats=Category.objects.all()
    data["cats"]=cats
    return render(request, "category.html", data)

def eprodcat(request,id=0):
    data = {"cats": "", "msg": "", "form": "", "btntext": "Update"}
    cat = Category.objects.filter(id=id)[0]
    request.session["cid"]=id
    data["form"]=CategoryForm(instance=cat)
    cats=Category.objects.all()
    data["cats"]=cats
    data["photo"]="/media/"+cat.CategoryImage.name
    return render(request, "category.html", data)

def dprodcat(request,id=0):
    cat=Category.objects.filter(id=id)[0]
    cat.delete() # Remove object from List as well as from database
    return redirect(to=prodcat)


# Product related views
def products(request):
    prods = Product.objects.all()
    return render(request, "productlist.html", {"prods":prods})

def addproduct(request,id=0):
    data = {"msg":"","btntext":"Save"}
    if request.method=="POST":
        btntext = request.POST["btn"]
        if btntext=="Save":
            prod=Product()
            prod.ProductName=request.POST["name"]
            prod.ProductDescription = request.POST["desc"]
            prod.ProductCategory = request.POST["category"]
            prod.ProductPrice = request.POST["price"]
            prod.ProductQty = request.POST["qty"]
            myfile=request.FILES["file"]
            fs=FileSystemStorage()
            print(myfile.name)
            fn=fs.save(myfile.name,myfile)
            fname=fs.url(fn)
            prod.ProductImage=fname
            prod.save()
            data["msg"]="Product Record is Saved"
        else:
            pid=request.session.get("cid",0);
            prod=Product.objects.filter(id=pid)[0]
            prod.ProductName = request.POST["name"]
            prod.ProductDescription = request.POST["desc"]
            prod.ProductCategory = request.POST["category"]
            prod.ProductPrice = request.POST["price"]
            prod.ProductQty = request.POST["qty"]
            if "file" in request.FILES:
                myfile = request.FILES["file"]
                fs = FileSystemStorage()
                fn = fs.save(myfile.name, myfile)
                fname = fs.url(fn)
                prod.ProductImage = fname
            prod.save() # if record is exists then update it
            data["msg"] = "Product Record is Updated"
    if id==0:
        data["prod"]=Product()
    else:
        data["prod"] = Product.objects.filter(id=id)[0]
        request.session["cid"]=id
        data["btntext"]= "Update"

    data["cats"]=Category.objects.all()
    print("Size of Category: ",len(data["cats"]))

    return render(request,"addproduct.html",data)


def delproduct(request,id=0):
    prod=Product.objects.filter(id=id)[0]
    prod.delete() # Remove object from List as well as from database
    return redirect(to=products) # calls to function

@login_required(login_url="/login2")
def showcart(request):
    carts = Cart.objects.filter(UserName=request.user.username)
    sum1 = Cart.objects.filter(UserName=request.user.username).aggregate(Sum('ProductTotal'))
    # sum1 is an object whose value we can get using get function
    return render(request, "cart.html", {"carts": carts, "sum1": sum1.get('ProductTotal__sum', 0.00)})

@login_required(login_url="/login2")
def addtocart(request,id=0):
    prod = Product.objects.filter(id=id)[0]
    cart = Cart()
    cart.ProductID=prod.id
    cart.ProductName =prod.ProductName
    cart.ProductPrice = prod.ProductPrice
    cart.ProductQty = 1
    cart.ProductTotal=prod.ProductPrice
    cart.ProductImage=prod.ProductImage
    cart.UserName=request.user.username
    cart.save()
    return redirect("/showcart")

@login_required(login_url="/login2")
def cartdelete(request,id=0):
    cart=Cart.objects.filter(id=id)[0]
    cart.delete() # Remove object from List as well as from database
    return redirect(to=showcart) # calls to function

@login_required(login_url="/login2")
def cartupdate(request):
    id=request.GET["cid"]
    q=request.GET["q"]
    cart=Cart.objects.filter(id=id)[0]
    cart.ProductQty=int(q)
    cart.ProductTotal=cart.ProductPrice*cart.ProductQty
    cart.save()
    return redirect(to=showcart) # calls to function

@login_required(login_url="/login2")
def checkout(request):
    queryString = "?cmd=_cart"
    queryString += "&upload=1"
    queryString += "&charset=utf-8"
    queryString += "&currency_code=USD"
    queryString += "&business=rupeshbengade4871@gmail.com"
    queryString += "&return=http://localhost:8000/neworder?u=" + request.user.username
    queryString += "&notify_url=''"

    carts = Cart.objects.filter(UserName=request.user.username)
    i = 1
    for cart in carts:
        queryString += "&item_number_" + str(i) + "=" + str(cart.ProductID)
        queryString += "&item_name_" + str(i) + "=" + cart.ProductName
        queryString += "&amount_" + str(i) + "=" + str(cart.ProductPrice)
        queryString += "&quantity_" + str(i) + "=" + str(cart.ProductQty)
        i+=1
    url = "https://www.sandbox.paypal.com/cgi-bin/webscr" + queryString;

    return HttpResponseRedirect(url)


@login_required(login_url="/login2")
def showorders(request):
    ords = Orders.objects.filter(UserName=request.user.username)
    sum1 = Orders.objects.filter(UserName=request.user.username).aggregate(Sum('OrderTotal'))
    return render(request, "orders2.html", {"ords": ords, "sum1": sum1.get('OrderTotal__sum', 0.00)})

#@login_required(login_url="/login2")
def neworder(request):
    u=request.GET["u"]
    carts = Cart.objects.filter(UserName=u)
    sum1 = Cart.objects.filter(UserName=u).aggregate(Sum('ProductTotal'))
    ototal=sum1.get('ProductTotal__sum', 0.00)


    ord = Orders()
    ord.UserName=u
    ord.OrderTotal=ototal
    ord.Status="Paid"
    ord.save()
    oid=ord.id

    for cart in carts:
        ot=OrdersItems()
        ot.OrderId=oid
        ot.ProductID=cart.ProductID
        ot.ProductName=cart.ProductName
        ot.ProductPrice=cart.ProductPrice
        ot.ProductQty=cart.ProductQty
        ot.ProductTotal=cart.ProductTotal
        ot.save()
    # delete cart items
    carts.delete()
    return redirect("/showorders")

@login_required(login_url="/login2")
def cancelorder(request,id=0):
    ord=Orders.objects.filter(id=id)[0]
    ord.delete() # Remove object from List as well as from database
    return redirect(to=showorders) # calls to function

@login_required(login_url="/login2")
def showordersdetails(request,id=0):
    ord = Orders.objects.filter(id=id)[0]
    oitems=OrdersItems.objects.filter(OrderId=id)
    return render(request, "ordersdetails.html", {"ord": ord, "oitems": oitems})


#admin
@login_required(login_url="/login2")
def showorders2(request):
    pstatus=""
    if "pstatus" in request.GET:
        pstatus=request.GET["pstatus"]
        ords = Orders.objects.filter(Status=pstatus)
        sum1 = Orders.objects.filter(Status=pstatus).aggregate(Sum('OrderTotal'))
    else:
        ords = Orders.objects.all()
        sum1 = Orders.objects.all().aggregate(Sum('OrderTotal'))
    return render(request, "orders3.html", {"ords": ords, "pstatus":pstatus,"sum1": sum1.get('OrderTotal__sum', 0.00)})

@login_required(login_url="/login2")
def dispatchorders2(request,id=0):
    ord = Orders.objects.filter(id=id)[0]
    ord.Status="Dispatched"
    ord.save()
    return redirect(to=showorders2)  # calls to function
