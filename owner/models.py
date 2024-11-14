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
    vehicle_charges = models.FloatField(default=0)
    
    
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
    discount  = models.FloatField(default=0)
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
    
    
class Cash_transition(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    order_master = models.ForeignKey(order_master,on_delete=models.PROTECT,null=True)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
class Phonepe_number(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    phonepe_name = models.CharField(max_length=100)
    phonepe_number = models.IntegerField()
    status = models.IntegerField(default=1)
class Phonepe_transition(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    phonepe_number = models.ForeignKey(Phonepe_number,on_delete=models.PROTECT,null=True)
    order_master = models.ForeignKey(order_master,on_delete=models.PROTECT,null=True)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)