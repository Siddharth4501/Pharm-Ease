from .models import Dealer
from .models import Employee
from .models import Medicine
from .models import PharmLogin
from .models import Payment,MedicineSale
from django.shortcuts import render,redirect
from django.db import IntegrityError
from django.contrib import messages
from .models import Invoice
from .utils import invoice_data_validator
from .utils import invoice_data_processor

import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Max
import num2words
from django.shortcuts import get_object_or_404
import json
import datetime
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Count
import math
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    if 'pharmuser' not in request.session.keys():
        ispharmuser=False
    else:
        ispharmuser=True
    return render(request, 'pharma/index.html',{'ispharmuser':ispharmuser,})


def dealerform(request):
    pharmuser=False
    dict = {'add': True,}
    return render(request, 'pharma/dealer.html', dict)


def dealerforminsert(request):
    try:
        dealer = Dealer()
        dealer.dname = request.POST['dname']
        dealer.address = request.POST['address']
        dealer.phn_no = request.POST['pno']
        dealer.email = request.POST['email']
        dealer.save()
        ispharmuser=True
    except IntegrityError:
        return render(request, "pharma/new.html")
    return render(request, 'pharma/index.html',{'ispharmuser':ispharmuser})


def dealerformupdate(request, foo):
    try:
        dealer = Dealer.objects.get(pk=foo)
        dealer.dname = request.POST['dname']
        dealer.address = request.POST['address']
        dealer.phn_no = request.POST['pno']
        dealer.email = request.POST['email']
        dealer.save()
        ispharmuser=True
    except IntegrityError:
        return render(request, "pharma/new.html")
    return render(request, 'pharma/index.html',{'ispharmuser':ispharmuser})
    

def dealerformview(request, foo):
    dealer = Dealer.objects.get(pk=foo)
    dict = {'dealer': dealer}
    return render(request, 'pharma/dealer.html', dict)


def dealerformdelete(request, foo):
    dealer = Dealer.objects.get(pk=foo)
    dealer.delete()
    ispharmuser=True
    return render(request, 'pharma/index.html',{'ispharmuser':ispharmuser})


def dealertable(request):
    dealer = Dealer.objects.all()
    dict = {"dealer": dealer}
    return render(request, 'pharma/dealertable.html', dict)


def empform(request):
    dict = {'add': True}
    return render(request, 'pharma/emp.html', dict)


def empforminsert(request):
    try:
        emp = Employee()
        emp.e_id = request.POST['eid']
        emp.fname = request.POST['fname']
        emp.lname = request.POST['lname']
        emp.address = request.POST['address']
        emp.phn_no = request.POST['pno']
        emp.email = request.POST['email']
        emp.sal = request.POST['sal']
        emp.save()
        ispharmuser=True
    except IntegrityError:
        return render(request, "pharma/new.html")
    return render(request, 'pharma/index.html',{'ispharmuser':ispharmuser})


def empformupdate(request, foo):
    try:
        emp = Employee.objects.get(pk=foo)
        emp.e_id = request.POST['eid']
        emp.fname = request.POST['fname']
        emp.lname = request.POST['lname']
        emp.address = request.POST['address']
        emp.phn_no = request.POST['pno']
        emp.email = request.POST['email']
        emp.sal = request.POST['sal']
        emp.save()
        ispharmuser=True
    except IntegrityError:
        return render(request, "pharma/new.html")
    return render(request, 'pharma/index.html',{'ispharmuser':ispharmuser})


def empformview(request,foo):
    emp = Employee.objects.get(pk=foo)   
    dict = {'emp': emp}
    return render(request, 'pharma/emp.html', dict)


def empformdelete(request, foo):
    emp = Employee.objects.get(pk=foo)
    emp.delete()
    ispharmuser=True
    return render(request, 'pharma/index.html',{'ispharmuser':ispharmuser})


def emptable(request):
    emp = Employee.objects.all()
    dict = {"emp": emp}
    return render(request, 'pharma/emptable.html', dict)


# def custform(request):
#     dict = {'add': True}
#     return render(request, 'pharma/cust.html', dict)


# def custforminsert(request):
#     try:
#         cust = Customer()
#         cust.fname = request.POST['fname']
#         cust.lname = request.POST['lname']
#         cust.address = request.POST['address']
#         cust.phn_no = request.POST['pno']
#         cust.email = request.POST['email']
#         cust.save()
#     except IntegrityError:
#         return render(request, "pharma/new.html")
#     return render(request, 'pharma/index.html')


# def custformupdate(request, foo):
#     try:
#         cust = Customer.objects.get(pk=foo)
#         cust.fname = request.POST['fname']
#         cust.lname = request.POST['lname']
#         cust.address = request.POST['address']
#         cust.phn_no = request.POST['pno']
#         cust.email = request.POST['email']
#         cust.save()
#     except IntegrityError:
#         return render(request, "pharma/new.html")
#     return render(request, 'pharma/index.html')


# def custformview(request):
#     cust = Customer.objects.get(pk=foo)
#     dict = {'cust': cust}
#     return render(request, 'pharma/cust.html', dict)


# def custformdelete(request, foo):
#     cust = Customer.objects.get(pk=foo)
#     cust.delete()
#     return render(request, 'pharma/index.html')


def custtable(request):
    cust = MedicineSale.objects.all()
    dict = {"cust": cust}
    return render(request, 'pharma/custtable.html', dict)


def medform(request):
    dict = {'add': True}
    return render(request, 'pharma/med.html', dict)


def medforminsert(request):
    try:
        med = Medicine()
        med.m_id = request.POST['mid']
        med.mname = request.POST['mname']
        med.dname = request.POST['dname']
        med.med_mrp = request.POST['Medicine_MRP']
        med.med_mrp=int(med.med_mrp)
        med.med_costprice = request.POST['Medicine_CP']
        med.med_costprice=int(med.med_costprice)
        med.med_stock = request.POST['stock']
        med.med_stock=int(med.med_stock)
        med.med_remaining_stock = request.POST['remstock']
        med.med_remaining_stock=int(med.med_remaining_stock)
        med.desc = request.POST['desc']
        med.keybenefits = request.POST['Key_Benefits']
        med.dirofuse = request.POST['Direction_Of_Use']
        med.ingredients = request.POST['Ingredients']
        med.med_img = request.FILES['medimg']
        med.med_mfg = request.POST['med_mfg']
        med.med_exp = request.POST['med_exp']
        med.category = request.POST['category']
        med.save()
        ispharmuser=True
    except IntegrityError:
        return render(request, "pharma/new.html")
    return render(request, 'pharma/index.html',{'ispharmuser':ispharmuser})


def medformupdate(request, foo):
    try:
        med = Medicine.objects.get(pk=foo)
        
        med.m_id = request.POST['mid']
        med.mname = request.POST['mname']
        med.dname = request.POST['dname']
        med.med_mrp = request.POST['Medicine_MRP']
        med.med_mrp=int(med.med_mrp)
        med.med_costprice = request.POST['Medicine_CP']
        med.med_costprice=int(med.med_costprice)
        med.med_stock = request.POST['stock']
        med.med_stock=int(med.med_stock)
        med.med_remaining_stock = request.POST['remstock']
        med.med_remaining_stock=int(med.med_remaining_stock)
        med.desc = request.POST['desc']
        med.keybenefits = request.POST['Key_Benefits']
        med.dirofuse = request.POST['Direction_Of_Use']
        med.ingredients = request.POST['Ingredients']
        med_updated_img = request.POST.get('medimg')
        if med_updated_img:
            med.med_img=request.FILES('medimg')
        else:
            med.med_img=med.med_img
        med.med_mfg = request.POST['med_mfg']
        med.med_exp = request.POST['med_exp']
        med.category = request.POST['category']
        med.save()
        ispharmuser=True
    except IntegrityError:
        return render(request, "pharma/new.html")
    return render(request, 'pharma/index.html',{'ispharmuser':ispharmuser})


def medformview(request, foo):
    med = Medicine.objects.get(pk=foo)
    dict = {'med': med}
    return render(request, 'pharma/med.html', dict)


def medformdelete(request, foo):
    med = Medicine.objects.get(pk=foo)
    med.delete()
    return render(request, 'pharma/index.html')


def medtable(request):
    med = Medicine.objects.all()
    dict = {"med": med}
    return render(request, 'pharma/medtable.html', dict)


# def purchaseform(request):
#     dict = {'add': True}
#     return render(request, 'pharma/purchase.html', dict)


# def purchaseforminsert(request):
#     try:
#         purchase = Purchase()
#         purchase.pname = request.POST['pname']
#         purchase.fname = request.POST['fname']
#         purchase.lname = request.POST['lname']
#         purchase.qty = request.POST['qty']
#         purchase.phn_no = request.POST['pno']
#         purchase.price = request.POST['price']
#         a = (int(purchase.price)) * (int(purchase.qty))
#         purchase.total = a
#         purchase.save()
#     except IntegrityError:
#         return render(request, "pharma/new.html")
#     return render(request, 'pharma/index.html')


# def purchaseformupdate(request, foo):
#     try:
#         purchase = Purchase.objects.get(pk=foo)
#         purchase.pname = request.POST['pname']
#         purchase.fname = request.POST['fname']
#         purchase.lname = request.POST['lname']
#         purchase.qty = request.POST['qty']
#         purchase.phn_no = request.POST['pno']
#         purchase.price = request.POST['price']
#         a = (int(purchase.price)) * (int(purchase.qty))
#         purchase.total = a
#         purchase.save()
#     except IntegrityError:
#         return render(request, "pharma/new.html")
#     return render(request, 'pharma/index.html')


# def purchaseformview(request, foo):
#     purchase = Purchase.objects.get(pk=foo)
#     dict = {'purchase': purchase}
#     return render(request, 'pharma/purchase.html', dict)


# def purchaseformdelete(request, foo):
#     purchase = Purchase.objects.get(pk=foo)
#     purchase.delete()
#     return render(request, 'pharma/index.html')


# def purchasetable(request):
#     purchase = Purchase.objects.all()
#     dict = {"purchase": purchase}
#     return render(request, 'pharma/purchasetable.html', dict)

def purchasetable(request):
    purchase = Payment.objects.filter(status=True)
    purchase_at_responsive = Payment.objects.filter(status=True)
    purchase=reversed(purchase)
    purchase_at_responsive=reversed(purchase_at_responsive)
    dict1 = {"purchase": purchase,'purchase_at_responsive':purchase_at_responsive}
    return render(request, 'pharma/purchasetable.html', dict1)

def del_Customer(request,foo):
    print(foo)
    foo=int(foo)
    dItem=Customer.objects.get(pk=foo)
    if dItem:
        dItem.delete()
    else:
        pass
    return redirect('custtable')

def del_Dealer(request,foo):
    print(foo)
    foo=int(foo)
    dItem=Dealer.objects.get(pk=foo)
    if dItem:
        dItem.delete()
    else:
        pass
    return redirect('dealertable')

def del_Medicine(request,foo):
    print(foo)
    foo=int(foo)
    dItem=Medicine.objects.get(pk=foo)
    if dItem:
        dItem.delete()
    else:
        pass
    return redirect('dealertable')

def del_Employee(request,foo):
    print(foo)
    foo=int(foo)
    dItem=Employee.objects.get(pk=foo)
    if dItem:
        dItem.delete()
    else:
        pass
    return redirect('emptable')

def invoice_create(request):
    context = {}
    context['default_invoice_number'] = Invoice.objects.filter(user=request.user).aggregate(Max('invoice_number'))['invoice_number__max']
    
    if not context['default_invoice_number']:
        context['default_invoice_number'] = 1
    else:
        context['default_invoice_number'] += 1

    context['default_invoice_date'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

    if request.method == 'POST':
        print("POST received - Invoice Data")

        invoice_data = request.POST

        validation_error = invoice_data_validator(invoice_data)
        if validation_error:
            context["error_message"] = validation_error
            return render(request, 'pharma/invoice_create.html', context)

        
        print("Valid Invoice Data")

        invoice_data_processed = invoice_data_processor(invoice_data)
        
        invoice_data_processed_json = json.dumps(invoice_data_processed)
        new_invoice = Invoice(user=request.user,
                              invoice_customer=invoice_data['customer-name'],
                              invoice_number=int(invoice_data['invoice-number']),
                              invoice_date=datetime.datetime.strptime(invoice_data['invoice-date'], '%Y-%m-%d'),
                              invoice_json=invoice_data_processed_json)
                              
        new_invoice.save()
        print("INVOICE SAVED")

        


        return redirect('invoice_viewer', invoice_id=new_invoice.id)

    return render(request, 'pharma/invoice_create.html', context)


def invoices(request):
    context = {}
    context['invoices'] = Invoice.objects.all().order_by('-id')
    return render(request, 'pharma/invoices.html', context)


def invoice_viewer(request, invoice_id):
    invoice_obj = get_object_or_404(Invoice, id=invoice_id)
    
    user_profile =request.user

    context = {}
    context['invoice'] = invoice_obj
    context['invoice_data'] = json.loads(invoice_obj.invoice_json)
    print(context['invoice_data'])
    context['currency'] = "₹"
    context['total_in_words'] = num2words.num2words(int(context['invoice_data']['invoice_total_amt_with_gst']), lang='en_IN').title()
    context['user_profile'] = user_profile
    return render(request, 'pharma/invoice_printer.html', context)



def invoice_delete(request):
    if request.method == "POST":
        invoice_id = request.POST["invoice_id"]
        invoice_obj = get_object_or_404(Invoice,id=invoice_id)
        
        invoice_obj.delete()
    return redirect('invoices')

def AdminLogin(request):
    
    if request.method=='POST':
        PharmId=request.POST.get('PharmId')
        PharmPassword=request.POST.get('PharmPassword')
        print(PharmId,"dkd",PharmPassword)
        pharm_login=PharmLogin.objects.all()
        for i in pharm_login:
            if(i.Pharm_ID==PharmId and i.Pharm_Password==PharmPassword):
                print(pharm_login)
                request.session['pharmuser']="gooku"
                print(request.session['pharmuser'])
                messages.success(request,"Successfully logged in")
                return redirect('index')
            else:
                send_mail(
                    'Alert!!!',
                    'Someone tried to login but enterted wrong details',
                    'settings.EMAIL_HOST_USER',
                    [''],//admin email id 
                    fail_silently=False
                    )
                messages.error(request,'Password Or Pharmacy ID is wrong')
                return redirect('AdminLogin')
    return render(request,'pharma/AdminLogin.html')

def logoutView(request):
    
    if 'pharmuser' in request.session.keys():
        del request.session['pharmuser']
    
    return redirect("AdminLogin")





def monthly_sales_report(request):
    
    today = timezone.now()
    current_year = today.year
    
    monthly_sales_by_medicine = []
    
    for medicine in Medicine.objects.all():
        medicine_sales_data = {'medicine': medicine, 'monthly_sales': []}
        
        
        for month in range(1, 13):
            monthly_sales = MedicineSale.objects.filter(medicine=medicine, sale_date__year=current_year, sale_date__month=month)
            total_sales_for_month = monthly_sales.aggregate(total_sales_for_month=Sum('quantity_sold'))['total_sales_for_month']
            medicine_sales_data['monthly_sales'].append({'month': month, 'total_sales': total_sales_for_month,'singleeoq':"N/A"})

        total_quantity_sold = MedicineSale.objects.filter(medicine=medicine, sale_date__year=current_year).aggregate(total_quantity_sold=Sum('quantity_sold'))['total_quantity_sold'] or 0
        demand_rate = total_quantity_sold / 12 
        Ordering_Costs=302.5
        Holding_Costs=102.5
        eoq =round(math.sqrt((2 * demand_rate * Ordering_Costs) / Holding_Costs)) 
        medicine_sales_data['monthly_sales'].append({'eoq': eoq,'singleeoq':"A"}),
        monthly_sales_by_medicine.append(medicine_sales_data)
        print(monthly_sales_by_medicine)
    
    return render(request, 'pharma/monthly_sales_report.html', {'monthly_sales_by_medicine': monthly_sales_by_medicine})


def update_DeliveryStatus(request):
   payments=Payment.objects.filter(status=True)
   return render(request,'pharma/update_DeliveryStatus.html',{'payments':payments})

def orderDelivered(request):
    if request.method=='POST':
        unqid=request.POST.get('update_delivery_status')
        payment=Payment.objects.get(uniqueid=unqid)
        payment.delivery_status='Delivered'
        # email_to_tell=payment.delivery_information.delivery_email
        payment.save()
        payments=Payment.objects.filter(status=True)
        send_mail(

            'Wowwwww!!!!',
            'Your order has been delivered,thankyou for choosing us',
            'settings.EMAIL_HOST_USER',
            [''],//coustomer email id
            fail_silently=False
        )
        if payment.delivery_status=='Delivered':
            order_status='Delivered'

    return render(request,'pharma/update_DeliveryStatus.html',{'order_status':order_status,'payments':payments})
