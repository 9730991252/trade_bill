from django.db import models
from sunil.models import *
# Create your models here.
class office_employee(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    status = models.IntegerField(default=1)


    
class Item(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    marathi_name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)    

    
class Purchase_cart(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    item = models.ForeignKey(Item,on_delete=models.PROTECT,null=True)
    prise = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    
class Farmer(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200 , null=True)
    mobile = models.IntegerField()
    
class Purchase_order_master(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    farmer = models.ForeignKey(Farmer,on_delete=models.PROTECT,default=True, null=True)
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
    paid_status = models.IntegerField(default=0)
    
class Purchase_order_detail(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    item = models.ForeignKey(Item,on_delete=models.PROTECT,default=True, null=True)
    prise=models.FloatField(default=0)
    qty = models.IntegerField(default=1) 
    order_filter=models.IntegerField(default=True)
    weight=models.IntegerField(default=True)
    date=models.DateField(auto_now_add=True,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    stock_status = models.IntegerField(default=1)

class Customer(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200 , null=True)
    mobile = models.IntegerField()
    
class Sell_order_master(models.Model):
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
    paid_status = models.IntegerField(default=0)
    
    
class Sell_order_detail(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    order_master = models.ForeignKey(Sell_order_master,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    item = models.ForeignKey(Item,on_delete=models.PROTECT,default=True, null=True)
    order_master = models.ForeignKey(Sell_order_master,on_delete=models.PROTECT,null=True)
    prise=models.FloatField(default=0)
    qty = models.IntegerField(default=1) 
    order_filter=models.IntegerField(default=True)
    weight=models.IntegerField(default=True)
    date=models.DateField(auto_now_add=True,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    stock_status = models.IntegerField(default=1)
    
class Sell_cart(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    item = models.ForeignKey(Item,on_delete=models.PROTECT,null=True)
    prise = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    
class Sell_item_weight_detail(models.Model):
    cart_id = models.CharField(max_length=100,null=True)
    weight = models.IntegerField()
    Order_detail = models.ForeignKey(Sell_order_detail,on_delete=models.PROTECT,null=True)

class Purchase_item_weight_detail(models.Model):
    cart_id = models.CharField(max_length=100,null=True)
    weight = models.IntegerField()
    Order_detail = models.ForeignKey(Purchase_order_detail,on_delete=models.PROTECT,null=True)
    
class Farmer_purchase_payment_transaction(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.PROTECT, null=True)
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    amount = models.FloatField()
    bank_number = models.IntegerField(null=True)
    phonepe_number = models.IntegerField(null=True)
    payment_type = models.CharField(max_length=100)
    date = models.DateField()
    added_date = models.DateTimeField(auto_now_add=True)
    
class Customer_sell_payment_transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True)
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    amount = models.FloatField()
    bank_number = models.IntegerField(null=True)
    phonepe_number = models.IntegerField(null=True)
    payment_type = models.CharField(max_length=100)
    date = models.DateField()
    added_date = models.DateTimeField(auto_now_add=True)