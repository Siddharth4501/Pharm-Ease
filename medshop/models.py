from django.db import models
from django.conf import settings
# from datetime import datetime
from django.utils import timezone

# Create your models here.
class User_delivery_information(models.Model):
    
    delivery_email=models.EmailField(max_length=50,null=False)
    delivery_phno=models.IntegerField(default=0,null=False)
    delivery_address1=models.CharField(max_length=250,null=False)
    Prescription=models.ImageField(upload_to='static/prescriptions',default=None,null=True,blank=True)
    delivery_city=models.CharField(max_length=50,null=False)
    delivery_state=models.CharField(max_length=50,null=False)
    delivery_zip=models.IntegerField(null=False)
    


