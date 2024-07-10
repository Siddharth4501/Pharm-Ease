from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='index'),
    path('logoutview/', views.logoutView, name='logoutview'),

    path('dealerform/', views.dealerform, name="dealerform"),
    path('dealerforminsert/', views.dealerforminsert, name="dealerforminsert"),
    path('dealerformupdate/<int:foo>/', views.dealerformupdate, name="dealerformupdate"),
    path('dealerformview/<int:foo>/', views.dealerformview, name="dealerformview"),
    path('dealerformdelete/<int:foo>/', views.dealerformdelete, name="dealerformdelete"),
    path('dealertable/', views.dealertable, name='dealertable'),
    # path('del_Dealer/<int:foo>/',views.del_Dealer,name='del_Dealer'),

    path('medform/', views.medform, name="medform"),
    path('medforminsert/', views.medforminsert, name="medforminsert"),
    path('medformupdate/<int:foo>/', views.medformupdate, name="medformupdate"),
    path('medformview/<int:foo>/', views.medformview, name="medformview"),
    path('medformdelete/<int:foo>/', views.medformdelete, name="medformdelete"),
    path('medtable/', views.medtable, name='medtable'),
    # path('del_Medicine/<int:foo>/',views.del_Medicine,name='del_Medicine'),

    path('empform/', views.empform, name="empform"),
    path('empforminsert/', views.empforminsert, name="empforminsert"),
    path('empformupdate/<int:foo>/', views.empformupdate, name="empformupdate"),
    path('empformview/<int:foo>/', views.empformview, name="empformview"),
    path('empformdelete/<int:foo>/', views.empformdelete, name="empformdelete"),
    path('emptable/', views.emptable, name='emptable'),
    path('del_Employee/<int:foo>/',views.del_Employee,name='del_Employee'),

    # path('custform/', views.custform, name="custform"),
    # path('custforminsert/', views.custforminsert, name="custforminsert"),
    # path('custformupdate/', views.custformupdate, name="custformupdate"),
    # path('custformview/', views.custformview, name="custformview"),
    # path('custformdelete/', views.custformdelete, name="custformdelete"),
    path('custtable/', views.custtable, name='custtable'),
    path('del_Customer/<int:foo>/',views.del_Customer,name='del_Customer'),

    # path('purchaseform/', views.purchaseform, name="purchaseform"),
    # path('purchaseforminsert/', views.purchaseforminsert, name="purchaseforminsert"),
    # path('purchaseformupdate/', views.purchaseformupdate, name="purchaseformupdate"),
    # path('purchaseformview/', views.purchaseformview, name="purchaseformview"),
    # path('purchaseformdelete/', views.purchaseformdelete, name="purchaseformdelete"),
    path('purchasetable/', views.purchasetable, name='purchasetable'),

    path('invoices/new', views.invoice_create, name='invoice_create'),
    path('invoices/delete', views.invoice_delete, name='invoice_delete'),
    path('invoices/', views.invoices, name='invoices'),
    path('invoice/<int:invoice_id>', views.invoice_viewer, name='invoice_viewer'),

    path('AdminLogin/', views.AdminLogin, name='AdminLogin'),
    path('monthly_sales_report/', views.monthly_sales_report, name='monthly_sales_report'),

    path('update_DeliveryStatus/',views.update_DeliveryStatus,name="update_DeliveryStatus"),
    path('orderDelivered/',views.orderDelivered,name="orderDelivered"),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
