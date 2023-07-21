from django.conf.urls import url
from ProductApp import views

urlpatterns = [
    url(r'^products/create/$', views.create_product, name='create_product'),
    url(r'^products/$', views.get_products, name='get_products'),
]