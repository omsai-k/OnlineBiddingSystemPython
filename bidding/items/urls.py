from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('addItem', views.additem, name="addItem"), 
    path('biditem', views.biditem, name="biditem"),  
    path('validate', views.validate, name="validate"),  
    path('item/biditem', views.biditem, name="biditem"), 
    path('addItem/', views.add_item, name='addItem'),  
    path('end_auction/<int:item_id>/', views.end_auction, name='end_auction'),
]
