from django.db import models
from django.conf import settings
from django.utils import timezone
from medshop.models import User_delivery_information
# Create your models here.
class Dealer(models.Model):
    dname = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phn_no = models.BigIntegerField(unique=True)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.email


class Employee(models.Model):
    e_id = models.IntegerField(unique=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=50) 
    sal = models.CharField(max_length=20)
    phn_no = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.email

class Medicine(models.Model):
    CATEGORY_CHOICES=(
        ('Protein Power and Drinks','Protein Power and Drinks'),
        ('Personal Care','Personal Care'),
        ('Baby Care','Baby Care'),
    )
    m_id  = models.IntegerField(unique=True)
    mname = models.CharField(max_length=500)
    category=models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    dname = models.CharField(max_length=50)
    desc  = models.CharField(max_length=100000)
    keybenefits=models.CharField(max_length=100000,default="essential for health")
    dirofuse=models.CharField(max_length=100000,default="as directed by the physician")
    ingredients=models.CharField(max_length=100000,default="sodium,potassium,e.t.c")
    med_mfg=models.DateField()
    med_exp=models.DateField()
    med_mrp=models.IntegerField()
    med_stock=models.IntegerField()
    med_perpack_price = models.IntegerField(editable=False)
    med_remaining_stock = models.IntegerField()
    med_costprice=models.IntegerField()
    prescription_required=models.BooleanField(default=False)
    med_img=models.ImageField(upload_to='static/pic')
    
    def save(self, *args, **kwargs):
        
        self.med_perpack_price = self.calc() 

        super().save(*args,**kwargs)

    def calc(self):
        
        return self.med_mrp//self.med_stock
    
    def __str__(self):
        return self.mname



class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False)
    item=models.CharField(max_length=1001)
    count=models.IntegerField()

    def __str__(self):
        return self.item

class Payment(models.Model):
    uniqueid=models.CharField(max_length=1000,primary_key=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False)
    order_id=models.CharField(max_length=50,null=False)
    payment_id=models.CharField(max_length=100)
    datetime=models.DateTimeField(default=timezone.now)
    delivery_information=models.ForeignKey(User_delivery_information,on_delete=models.CASCADE,null=False,default="Unknown")
    ordered_items=models.ManyToManyField(OrderItem)
    amount=models.IntegerField(default=0)
    status=models.BooleanField(default=False)
    delivery_status=models.CharField(max_length=255,default='received')

    def __str__(self):
        return self.uniqueid

class Invoice(models.Model):
    user=models.CharField(max_length=1000)
    invoice_number = models.IntegerField()
    invoice_date = models.DateField()
    invoice_customer = models.CharField(max_length=1000)   
    invoice_json = models.TextField()
    inventory_reflected = models.BooleanField(default=True)
    books_reflected = models.BooleanField(default=True)
    def __str__(self):
        return str(self.invoice_number) + " | " + str(self.invoice_date)

class PharmLogin(models.Model):
    Pharm_ID=models.CharField(max_length=1000)
    Pharm_Password=models.CharField(max_length=1000)
    

class MedicineSale(models.Model):
    medicine=models.ForeignKey(Medicine,on_delete=models.CASCADE)
    quantity_sold=models.PositiveIntegerField()
    sale_date=models.DateField(auto_now_add=True)