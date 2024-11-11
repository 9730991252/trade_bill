from django.db import models
from sunil.models import *
# Create your models here.
class office_employee(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    status = models.IntegerField(default=1)

class Item_category(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    shears = models.FloatField(default=0)
    status = models.IntegerField(default=1)


    
class Stock_item(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    item_category = models.ForeignKey(Item_category,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    item_name_english = models.CharField(max_length=100)
    item_name_marathi = models.CharField(max_length=100)
    qty = models.IntegerField()
    stock_qty = models.IntegerField(null=True)
    weight = models.IntegerField()
    purchase_amount = models.FloatField(null=True)
    stock_weight = models.IntegerField()
    vehicle_number = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)
    stock_status = models.IntegerField(default=1)
    party_name = models.CharField(max_length=200, null=True)
    status = models.IntegerField(default=1)
    
    
class Customer(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200 , null=True)
    mobile = models.IntegerField()

class Cart(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,null=True)
    stock_item = models.ForeignKey(Stock_item,on_delete=models.PROTECT,null=True)
    prise = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    
     
    
class order_master(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,default=True, null=True)
    hamali  = models.FloatField()
    tolai  = models.FloatField()
    aadat  = models.FloatField()
    shears = models.FloatField()
    eater  = models.FloatField()
    total  = models.FloatField()
    order_filter=models.IntegerField(default=True)
    date=models.DateField(auto_now_add=True,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    
class Order_detail(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,default=True, null=True)
    stock_item = models.ForeignKey(Stock_item,on_delete=models.PROTECT,default=True, null=True)
    prise=models.FloatField(default=0)
    qty = models.IntegerField(default=1) 
    order_filter=models.IntegerField(default=True)
    weight=models.IntegerField(default=True)
    date=models.DateField(auto_now_add=True,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)

class Item_weight_detail(models.Model):
    cart_id = models.CharField(max_length=100,null=True)
    weight = models.IntegerField()
    order_detail = models.ForeignKey(Order_detail,on_delete=models.PROTECT,null=True)