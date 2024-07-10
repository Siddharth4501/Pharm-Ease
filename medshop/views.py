 
from django.shortcuts import render,HttpResponse,redirect
from pharma.models import Medicine
from pharma.models import OrderItem,Payment,MedicineSale
from medshop.models import User_delivery_information
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import json
from django.views.decorators.http import require_POST
from medstore.settings import *
import razorpay
client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))
from time import time
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import re


def Myorders(request):
   payments=Payment.objects.filter(user=request.user,status=True)
   return render(request,'Myorders.html',{'payments':payments})
   
def med_home(request):
   
   medicine=Medicine.objects.all()
   choices=[]
   user=request.user
   for i in medicine:
      choices.append(i.category)
      print(choices)
   choices=set(choices)
   # set made the list elements unique
   print(user)
   search_list=[]
   for i in medicine:
      search_list.append(i.mname)
      print(type(i.mname))
   med_json=json.dumps(search_list)  
   print(search_list)
   payment=Payment.objects.all()
   for i in payment:
      print("esipeaspakz",i.ordered_items.all())
      for j in i.ordered_items.all():
         print("dvsdvsid",j.item)
   return render(request,'med_home.html',{'medicine':medicine,'choices':choices,'search_list':med_json})

@require_http_methods(["GET","POST"])
def med_cart(request):
   if request.method=='POST':
      
      sum=request.POST.get('topay_sum')
      if sum:
         
         user_delivery_email=request.POST.get('user_delivery_email')
         user_delivery_phno=request.POST.get('user_delivery_phno')
         user_delivery_Addres1=request.POST.get('user_delivery_Address1')
         
         user_delivery_city=request.POST.get('user_delivery_city')
         user_delivery_state=request.POST.get('user_delivery_state')
         user_delivery_zip=request.POST.get('user_delivery_zip')
         try:
            Prescription=request.FILES['user_Prescription']
         except KeyError:
            Prescription=None
         if Prescription:
            user_delivery_information=User_delivery_information(delivery_email=user_delivery_email,delivery_phno=user_delivery_phno,delivery_address1=user_delivery_Addres1,delivery_city=user_delivery_city,delivery_state=user_delivery_state,delivery_zip=user_delivery_zip,Prescription=Prescription)
         else:
            user_delivery_information=User_delivery_information(delivery_email=user_delivery_email,delivery_phno=user_delivery_phno,delivery_address1=user_delivery_Addres1,delivery_city=user_delivery_city,delivery_state=user_delivery_state,delivery_zip=user_delivery_zip)
         user_delivery_information.save()
         
         cart=request.POST.get('cart_data')
         cart=json.loads(cart)
         
         print("shivam")
         sum=float(sum)
         user=request.user
         order=None
         amount=int(sum)*100
         currency="INR"
         notes={
            'email':user.email,
            'name':user.username,
         }
         receipt=f"Pharm Ease-{int(time())}"
         order=client.order.create({'receipt':receipt,'currency':currency,'notes':notes,'receipt':receipt,'amount':amount})
         payment=Payment.objects.create(user=user,uniqueid=order.get('id'),order_id=order.get('id'),amount=int(sum),delivery_information=user_delivery_information)
         
         
         
         for i in cart:
            orderitem=OrderItem.objects.create(user=user,item=i['product_name'],count=i['count'])
            payment.ordered_items.add(orderitem)
         
         print(payment)
         
         dict_items={
            'order':order,
            'user':user,
         }
         print(dict_items)
         
      else:
         message.error(request,'Something Went Wrong Please Try Again After Somtime')
         redirect('med_cart')
   
   else:
      order=None
      dict_items={'order':order}
      
         
         
   return render(request,'cart_transact.html',dict_items)

def signup(request):
   if request.method=='POST':
      username=request.POST['signup_username']
      email=request.POST['signup_email']
      password=request.POST['signup_password']
      
      if (
         len(username)<5
         or len(username)>50
         or re.match("^[^a-zA-Z]*$",username)
      ):
         messages.error(request,"Usenmane is not acceptable,try another")
         return redirect('med_home')
         # return render(request,'med_home.html',{'error_username':error_username})
      
      if(
         not email.endswith('@gmail.com')
         or not any(char.isdigit() for char in email)
      ):
         messages.error(request,"Email must be of type @gmail.com only and it must contain at least one digit")
         return redirect('/med_home')
      
      if (
         len(password)<8
         or len(password)>16
         or not any(char.isdigit() for char in password)
         or not any(char.isupper() for char in password)
         or not any(char.islower() for char in password)
         or not any(char in '!@#$%^&*()_+' for char in password)
      ): 
         error_msg='''Password does not meet the requirements, Please try again!!!
         Note-Length of password must be greater then or equal to 8 and less then 16
         There must be one Upper case and one Lower Case Character
         There must be one special symbol in it'''
         messages.error(request,error_msg)
         return redirect('med_home')
         # return render(request,'med_home.html',{'error_password':error_password})
      myuser=User.objects.create_user(username,email,password)
      myuser.save()
      messages.success(request,"Signup Successful")
      return redirect('med_home')
   else:
      messages.error(request,"Something went wrong")
      return redirect('med_home')
      # return HttpResponse(" NOT FOUND")
   return render(request,'med_home.html')

def Login(request):
   
   if request.method =='POST':

      loginusername=request.POST.get('login_username')
      loginpassword=request.POST.get('login_password')

      user=authenticate(request,username=loginusername,password=loginpassword)
      print(user)
      if user is not None:

         login(request,user)
         
         
         messages.success(request,"Successfully Logged In")
         return redirect('med_home')
      else:
         
         messages.error(request,"Username or Password is incorrect")
         return redirect('med_home')
   return render(request,'med_home.html')

def logOUT(request):
   logout(request)
   
   messages.success(request,"Successfully Logged Out")
   return redirect('med_home')

@csrf_exempt
def thanks(request):
   if request.method=='POST':
      data=request.POST
      
      print(data)
      try:
         client.utility.verify_payment_signature(data)
         razorpay_order_id=data['razorpay_order_id']
         razorpay_payment_id=data['razorpay_payment_id']
         payment=Payment.objects.get(order_id=razorpay_order_id)
         payment.payment_id=razorpay_payment_id
         payment.status=True
         
         print("hello")
         if Payment.objects.filter(payment_id=razorpay_payment_id).exists():
            print("test0") 
            context={}
         else:
            payment.save()
            
            Medicinesale_record=MedicineSale()
            print("test1")
            for i in payment.ordered_items.all():
               medicine_item=Medicine.objects.get(mname=i.item)
               
               print(i)
               if MedicineSale.objects.all():
                  try:
                     Medicine_prevpresent = MedicineSale.objects.get(medicine=medicine_item)
                  except ObjectDoesNotExist:
                     Medicine_prevpresent = None  
                  if Medicine_prevpresent:
                     print("test2")
                     Medicine_prevpresent.quantity_sold+=i.count
                     Medicine_prevpresent.save()
                     print("test3")
                  else:
                     Medicinesale_record.medicine=medicine_item
                     print("test4")
                     Medicinesale_record.quantity_sold=i.count
                     Medicinesale_record.save()
                     print("test5")
               else:
                  Medicinesale_record.medicine=medicine_item
                  print("test6")
                  Medicinesale_record.quantity_sold=i.count
                  Medicinesale_record.save()
               print("test7")
               if medicine_item.med_remaining_stock>=1 and medicine_item.med_remaining_stock>=i.count:
                  medicine_item.med_remaining_stock-=i.count 
                  medicine_item.save()
            print("test8")   
            payment_success=True
            print(payment)
            context={'payment_success':payment_success,}
            print("test9")
         print("test10")
         
         
         return render(request,'thanks.html',context)
      except:
         return HttpResponse("Invalid Payment Details")
   return render(request,'thanks.html')
   
def Productpage(request):
   if request.method=='POST':
      medname=request.POST.get('medname')
      medicine_item=Medicine.objects.get(mname=medname)
      med_particular_category=Medicine.objects.filter(category=medicine_item.category)
      medicine=Medicine.objects.all()
      search_list=[]
      for i in medicine:
         search_list.append(i.mname)
         print(type(i.mname))
      med_json=json.dumps(search_list)  
      print(search_list)
      print("hmm",med_particular_category)
      dict_meditem={
         'medicine_item':medicine_item,
         'search_list':med_json,
         'med_particular_category':med_particular_category,
      }
   else:
      medicine_item=None
      medicine=Medicine.objects.all()
      search_list=[]
      for i in medicine:
         search_list.append(i.mname)
         print(type(i.mname))
      med_json=json.dumps(search_list)  
      print(search_list)
      dict_meditem={
         'medicine_item':medicine_item,
         'search_list':med_json,
      }
   return render(request,'Productpage.html',dict_meditem)


