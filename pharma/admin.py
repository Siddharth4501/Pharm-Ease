from django.contrib import admin
from .models import Dealer
from .models import Employee

from .models import Medicine
from .models import Invoice,Payment,OrderItem,PharmLogin,MedicineSale

# Register your models here.


admin.site.register(Dealer)
admin.site.register(Employee)
admin.site.register(Medicine)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Invoice)
admin.site.register(PharmLogin)
admin.site.register(MedicineSale)
