from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('med_home/',views.med_home,name='med_home'),
    path('med_cart/',views.med_cart,name='med_cart'),
    path('Login/',views.Login,name='Login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logOUT,name="logout"),
    path('Myorders/',views.Myorders,name="Myorders"),
    path('thanks/',views.thanks,name="thanks"),
    path('productpage/',views.Productpage,name="productpage"),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)