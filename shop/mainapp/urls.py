from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('index/<int:id>',views.index),
    path('index',views.index),
    path('login2',views.login2),
    path('check_email',views.check_email),
    path('about',views.about),
    path('contactus',views.contactus),
    path('customer',views.customer),
    path('logout2',views.logout2),
    path('changepass',views.changepass),
    path('admin2',views.admin2),
    path('prodcat', views.prodcat),
    path('eprodcat/<int:id>', views.eprodcat),
    path('dprodcat/<int:id>', views.dprodcat),

    path('products', views.products),
    path('addproduct', views.addproduct),
    path('addproduct/<int:id>', views.addproduct),
    path('delproduct/<int:id>', views.delproduct),

    path('showcart', views.showcart),
    path('addtocart/<int:id>', views.addtocart),
    path('cartdelete/<int:id>', views.cartdelete),
    path('cartupdate', views.cartupdate),

    path('checkout', views.checkout),
    path('neworder', views.neworder),
    path('showorders', views.showorders),
    path('cancelorder/<int:id>', views.cancelorder),
    path('showorderdetails/<int:id>', views.showordersdetails),

    path('showorders2', views.showorders2),
    path('dispatchorders2/<int:id>', views.dispatchorders2),





]